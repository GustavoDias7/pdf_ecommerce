# from django.contrib import admin
from django.urls import path, include
from core import views, webhooks
# from django.conf import settings
# from django.conf.urls.static import static
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("", views.test, name="test"),
    # path("products/", views.products, name="products"),
    # path("product/<int:id>/", views.product, name="product"),
    # path("signin/", views.signin, name="signin"),
    # path("signup/", views.signup, name="signup"),
    # path("logout/", views.logout_view, name="logout"),
    # path("account/", views.account, name="account"),
    # path("account/profile/", views.profile, name="profile"),
    # path("account/orders/", views.orders, name="orders"),
    # path("success/", views.success, name="success"),
    # path("cancel/", views.cancel, name="cancel"),
    # path("contact/", views.contact, name="contact"),
    # path("stripe-webhook/", webhooks.webhook_stripe, name="stripe_webhook"),
    # path("api/", include("api.urls")),
]
# Serving the media files in development mode
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# else:
#     urlpatterns += staticfiles_urlpatterns()
