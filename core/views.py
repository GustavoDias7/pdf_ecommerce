from django.shortcuts import render, redirect
from .models import Product, User
from .forms import UserForm, LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password


# Create your views here.
def home(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "pages/index.html", context)


# Create your views here.
def product(request, id):
    product = Product.objects.get(pk=id)
    context = {"product": product}
    return render(request, "pages/product.html", context)


def signin(request):
    if request.method == "POST":
        print(request.POST)
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect("/profile/")
            else:
                context = {"login_error": "E-mail or password was incorrect."}
                return render(request, "pages/signin.html", context)
        else:
            context = {"errors": login_form.errors, "login_form": login_form}
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
                print("Bad password: ", e)
                user_form.add_error("password", e)

        if confirm_password != password and confirm_password != "":
            user_form.add_error("confirm_password", "Password is not equal")

        if user_form.is_valid():
            # user = User.objects.create_user(
            #     username=username,
            #     email=email,
            #     password=password,
            # )
            # user.save()
            print(f"User '{username}' was created")
        else:
            context = {"errors": user_form.errors}
            return render(request, "pages/signup.html", context)

    return render(request, "pages/signup.html")


@login_required
def profile(request):
    return render(request, "pages/profile.html")
