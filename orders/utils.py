from django.core.mail import send_mail
from django.template.loader import render_to_string

def send_receipt_email(user, items, total_price, payment_method):
    subject = "Your Order Receipt"
    message = render_to_string("emails/receipt_email.html", {
        "user": user,
        "items": items,
        "total_price": total_price,
        "payment_method": payment_method,
    })

    send_mail(
        subject,
        message,
        None,
        [user.email],
        fail_silently=False,
    )
