from django.shortcuts import render, redirect
from .models import Product, User, Order
from .forms import UserForm, LoginForm, ContactForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.password_validation import validate_password
from django.conf import settings
import stripe
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import HttpResponse


stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        # Save an order in your database, marked as 'awaiting payment'
        create_order(session)

        # Check if the order is already paid (for example, from a card payment)
        #
        # A delayed notification payment will have an `unpaid` status, as
        # you're still waiting for funds to be transferred from the customer's
        # account.
        if session.payment_status == "paid":
            # Fulfill the purchase
            fulfill_order(session)
            send_ebook(session)

    elif event["type"] == "checkout.session.async_payment_succeeded":
        session = event["data"]["object"]

        # Fulfill the purchase
        fulfill_order(session)
        send_ebook(session)

    elif event["type"] == "checkout.session.async_payment_failed":
        session = event["data"]["object"]

        failed_order(session)
        # Send an email to the customer asking them to retry their order
        email_failed_payment(session)

    # Passed signature verification
    return HttpResponse(status=200)


def create_order(session):
    try:
        user = User.objects.get(email=session.customer_email)
        new_order = Order.objects.create(
            user_id=user.id,
            product_id=int(session.metadata.product_id),
            payment_status="w",
            discount=0,
            unit_price=session.amount_total,
            session_id=session.id,
        )
        new_order.save()
    except Exception as e:
        print(e)

def fulfill_order(session):
    try:
        order = Order.objects.get(session_id=session.id)
        order.payment_status = session.payment_status[0]
        order.save()
    except Exception as e:
        print(e)

def failed_order(session):
    try:
        order = Order.objects.get(session_id=session.id)
        order.payment_status = "u"
        order.save()
    except Exception as e:
        print(e)

def email_failed_payment(session):
    send_mail(
        subject=f"Subject: Failed Payment",
        from_email="from@example.com",
        recipient_list=[session.customer_email],
        fail_silently=False,
        message= f"Message: Failed Payment",
    )

def send_ebook(session):
    try:
        product_id = session.metadata.product_id
        product = Product.objects.get(id=product_id)

        rendered = render_to_string("emails/ebook.html", {"product": product})

        send_mail(
            subject=f"Subject: E-book ${product.name}",
            from_email="from@example.com",
            recipient_list=[session.customer_email],
            fail_silently=False,
            message= f"Message: E-book ${product.name}",
            html_message=rendered
        )
    except Exception as e:
        print(e)


def home(request):
    products = Product.objects.filter(archived=False)[:4]
    context = {"products": products}
    return render(request, "pages/index.html", context)


def product(request, id):
    host = request.META.get("HTTP_HOST")
    scheme = request.scheme
    url = f"{scheme}://{host}"

    try:
        product = Product.objects.filter(archived=False).get(pk=id)
        context = {"product": product}
    except:
        context = {"error": "Desculpe, o produto solicitado não existe."}

    if request.method == "POST":
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        "price": f"{product.stripe_price_id}",
                        "quantity": 1,
                    },
                ],
                mode="payment",
                success_url=f"{url}/success",
                cancel_url=f"{url}/cancel",
                customer_email=request.user.email,
                metadata={"product_id": product.id},
            )

            return redirect(checkout_session.url, code=303)
        except Exception as e:
            print(e)

    return render(request, "pages/product.html", context)


def products(request):
    try:
        products = Product.objects.filter(archived=False)[:6]
        products_count = Product.objects.filter(archived=False).count()
        context = {
            "products": products,
            "products_count": products_count,
        }
    except:
        context = {"error": "Desculpe, o produto solicitado não existe."}

    return render(request, "pages/products.html", context)


def signin(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            email = request.POST.get("email", "")
            password = request.POST.get("password", "")

            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect("profile")
            else:
                login_form.add_error(None, "E-mail or password was incorrect.")
                context = {"form": login_form}
                return render(request, "pages/signin.html", context)
        else:
            context = {"form": login_form}
            return render(request, "pages/signin.html", context)

    return render(request, "pages/signin.html")


def signup(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        username = request.POST.get("username", "")
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if password != "":
            try:
                validate_password(password, user=None, password_validators=None)
            except Exception as e:
                user_form.add_error("password", e)

        if confirm_password != password and confirm_password != "":
            user_form.add_error("confirm_password", "Password is not equal")

        if user_form.is_valid():
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
            user.save()

            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect("profile")
        else:
            context = {"form": user_form}
            return render(request, "pages/signup.html", context)

    return render(request, "pages/signup.html")


def contact(request):
    context = {"email_modal": False}

    if request.method == "POST":
        contact_form = ContactForm(request.POST)

        if contact_form.is_valid():
            try:
                send_mail(
                    subject=contact_form.data.get("subject", ""),
                    from_email=contact_form.data.get("email", ""),
                    recipient_list=["admin@mail.com"],
                    fail_silently=False,
                    message=contact_form.data.get("message", ""),
                )
                context = {"email_modal": True}
            except Exception as e:
                context = {"email_error_message": "Seu email não foi enviado!"}
                print(e)
        else:
            context = {"form": contact_form}

    return render(request, "pages/contact.html", context)


def logout_view(request):
    logout(request)
    return redirect("signin")


@login_required
def profile(request):
    return render(request, "pages/profile.html")


@login_required
def account(request):
    return render(request, "pages/account.html")


@login_required
def orders(request):
    try:
        orders = Order.objects.filter(user_id=request.user.id)
        context = {"orders": orders}
    except:
        context = {"error": "Desculpe, o pedido solicitado não existe."}

    return render(request, "pages/orders.html", context)


@login_required
def success(request):
    return render(request, "pages/success.html")


@login_required
def cancel(request):
    return render(request, "pages/cancel.html")