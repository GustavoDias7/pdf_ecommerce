from django.shortcuts import render, redirect
from .models import Product, User, Order
from .forms import UserForm, LoginForm, ContactForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.conf import settings
import stripe
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

stripe.api_key = settings.STRIPE_SECRET_KEY

def test(request):
    return render(request, "pages/test.html")

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
            # create username using first and last name
            username = create_username(
                user_form.data.get("first_name", ""), 
                user_form.data.get("last_name", "")
            )

            user = User.objects.create_user(
                username=username,
                email=user_form.data.get("email", ""),
                first_name=user_form.data.get("first_name", ""),
                last_name=user_form.data.get("last_name", ""),
                password=password,
            )
            user.save()

            user = authenticate(email=user_form.data.get("email", ""), password=password)

            if user is not None:
                login(request, user)
                return redirect("profile")
        else:
            context = {"form": user_form}
            return render(request, "pages/signup.html", context)

    return render(request, "pages/signup.html")


def create_username(fn, ln):
    random_number = get_random_string(length=6, allowed_chars='0123456789')
    return f"{fn[:2]}{ln[:2]}{random_number}".upper()

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