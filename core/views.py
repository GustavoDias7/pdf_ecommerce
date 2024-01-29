from django.shortcuts import render, redirect
from .models import Product, User
from .forms import UserForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.
def home(request):
    products = Product.objects.filter(id__in=(1, 2, 3, 4))
    context = {"products": products}
    return render(request, "pages/index.html", context)


# Create your views here.
def product(request, id):
    try:
        product = Product.objects.get(pk=id)
        context = {"product": product}
    except:
        context = {"error": "Desculpe, o produto solicitado não existe."}

    if request.method == "POST":
        try:
            URL = "http://127.0.0.1:8000"
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        "price": f"{product.stripe_price_id}",
                        "quantity": 1,
                    },
                ],
                mode="payment",
                success_url=f"{URL}/success",
                cancel_url=f"{URL}/cancel",
                customer_email=request.user.email,
            )

            return redirect(checkout_session.url, code=303)
        except Exception as e:
            print(e)

    return render(request, "pages/product.html", context)


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
    return render(request, "pages/orders.html")


@login_required
def payment(request):
    return render(request, "pages/payment.html")


@login_required
def success(request):
    return render(request, "pages/success.html")


@login_required
def cancel(request):
    return render(request, "pages/cancel.html")
