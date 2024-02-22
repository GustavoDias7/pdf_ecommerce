from .models import Product, User, Order
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.conf import settings
from django.core.mail import send_mail

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def webhook_stripe(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None


    print("payload", payload)
    print("sig_header", sig_header)

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except ValueError as e:
        # Invalid payload
        print("ValueError:", e)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        print("SignatureVerificationError:", e)
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
            subject=f"Subject: E-book {product.name}",
            from_email="from@example.com",
            recipient_list=[session.customer_email],
            fail_silently=False,
            message= f"Message: E-book {product.name}",
            html_message=rendered
        )
    except Exception as e:
        print(e)