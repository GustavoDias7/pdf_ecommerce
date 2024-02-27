from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.core import validators
from django.utils.translation import gettext_lazy as _
import re
from django.utils import timezone
from django.core.mail import send_mail
from gdstorage.storage import GoogleDriveStorage
from urllib.parse import urlparse
from urllib.parse import parse_qs


# Define Google Drive Storage
gd_storage = GoogleDriveStorage()


class Product(models.Model):
    name = models.CharField(max_length=30)
    price = models.IntegerField()
    stripe_price_id = models.CharField(max_length=35, null=True, blank=True)
    description = models.TextField(max_length=400)
    image = models.ImageField(upload_to="images/", storage=gd_storage, null=True)
    pdf = models.FileField(upload_to="pdfs/", storage=gd_storage, null=True)
    archived = models.BooleanField(default=False)
    discount = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
    )
    
    def get_image(self):
        parsed_url = urlparse(self.image.url)
        image_id = parse_qs(parsed_url.query)['id'][0]
        return f"https://drive.google.com/thumbnail?id={image_id}&sz=w1000"

    def __str__(self):
        return f"{self.name}"


class Order(models.Model):
    session_id = models.CharField(max_length=70)
    product = models.ForeignKey("Product", on_delete=models.RESTRICT)
    user = models.ForeignKey("User", on_delete=models.RESTRICT)
    payment_status = models.CharField(
        max_length=1, choices=list(settings.PAYMENT_STATUS.items())
    )
    date = models.DateTimeField(auto_now=True)
    unit_price = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    discount = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
    )

    def get_image(self):
        parsed_url = urlparse(self.product.image.url)
        image_id = parse_qs(parsed_url.query)['id'][0]
        return f"https://drive.google.com/thumbnail?id={image_id}&sz=w1000"

    def __str__(self):
        return f"Order {self.id}"

class UserManager(BaseUserManager):
    def _create_user(
        self, username, email, password, is_staff, is_superuser, **extra_fields
    ):
        now = timezone.now()
        if not username:
            raise ValueError(_("The given username must be set"))
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(
            username, email, password, False, False, **extra_fields
        )

    def create_superuser(self, username, email, password, **extra_fields):
        user = self._create_user(username, email, password, True, True, **extra_fields)
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _("username"),
        max_length=15,
        unique=True,
        help_text=_(
            "Required. 15 characters or fewer. Letters, numbers and @/./+/-/_ characters"
        ),
        validators=[
            validators.RegexValidator(
                re.compile("^[a-zA-Z0-9_.-]+$"), _("Enter a valid username."), _("invalid")
            )
        ],
    )

    first_name = models.CharField(_("first name"), max_length=30, validators=[MinLengthValidator(3)])

    last_name = models.CharField(_("last name"), max_length=30, validators=[MinLengthValidator(3)])

    email = models.EmailField(_("email address"), max_length=255, unique=True)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. Unselect this instead of deleting accounts."
        ),
    )

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    is_trusty = models.BooleanField(
        _("trusty"),
        default=False,
        help_text=_("Designates whether this user has confirmed his account."),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "password"]

    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])
