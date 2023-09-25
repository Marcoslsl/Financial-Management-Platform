from typing import List
from decouple import config
from django.http import HttpRequest
from django.core.mail import send_mail as send_email_django


def send_mail(
    request: HttpRequest, subject: str, message: str, emails_to_send: List[str]
):
    send_email_django(
        subject,
        message,
        config("EMAIL_HOST_USER"),
        emails_to_send,
        fail_silently=False,
    )

    return {
        "message": "success",
        "content": {
            "subject": subject,
            "message": message,
            "from_email": config("EMAIL_HOST_USER"),
            "recipient_list": emails_to_send,
        },
    }
