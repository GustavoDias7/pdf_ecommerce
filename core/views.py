from django.shortcuts import render, redirect
from .models import Product, User
from .forms import UserForm, LoginForm, CreditCardForm, BoletoForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from calendar import monthrange
from datetime import datetime


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
def checkout(request, product_id):
    template_name = "pages/checkout.html"
    context = {}

    try:
        product = Product.objects.get(pk=product_id)
        context["product"] = product
    except:
        return redirect("product", id=product_id)

    if request.method == "POST":
        POST = request.POST.copy()

        if "payment_format" in POST:
            context["payment_format"] = POST["payment_format"]

            if POST["payment_format"] == "credit_card":
                if "expiry" in POST and POST["expiry"] != "":
                    splitted_date = POST["expiry"].split("/")
                    year = int(splitted_date[1])
                    month = int(splitted_date[0])
                    day = monthrange(year, month)[1]  # last day of the month
                    POST["expiry"] = f"{month}/{day}/{year}"

                cc_form = CreditCardForm(POST)

                if cc_form.is_valid():
                    request.session["credit_card"] = {
                        "card_number": cc_form["card_number"].value(),
                        "card_name": cc_form["card_name"].value(),
                        "expiry": cc_form["expiry"].value(),
                        "cvv": cc_form["cvv"].value(),
                        "installments": cc_form["installments"].value(),
                        "date": str(datetime.now()),
                    }

                context["form"] = cc_form

            elif POST["payment_format"] == "boleto":
                boleto_form = BoletoForm(POST)

                if boleto_form.is_valid():
                    pass

                context["form"] = boleto_form

    return render(
        request,
        template_name,
        context,
    )
