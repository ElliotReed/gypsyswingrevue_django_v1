from decouple import config
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string

api_key = config("MAILCHIMP_API_KEY")
server = config("MAILCHIMP_DATA_CENTER")
list_id = config("MAILCHIMP_LIST_ID")

contact_recieving_email = config("CONTACT_RECIEVING_EMAIL")


def add_subscriber(request, email):
    mailchimp = Client()
    mailchimp.set_config(
        {
            "api_key": api_key,
            "server": server,
        }
    )

    member_info = {
        "email_address": email,
        "status": "subscribed",
    }

    try:
        response = mailchimp.lists.add_list_member(list_id, member_info)
        email = response["email_address"]
    except ApiClientError as error:
        return messages.error(request, "Sorry, something went wrong...")

    return messages.success(
        request, f"{email} has been added to my newsletter. Thank you!"
    )


def send_contact_form(request):
    body = request.POST
    name = body.get("name")
    sender_message = body.get("message")
    sender_email = body.get("email")

    msg_html = render_to_string(
        "core/email.html",
        {"message": {"message": sender_message, "name": name, "sender": sender_email}},
    )

    try:
        send_mail(
            f"A new message from {name}",
            sender_message,
            sender_email,
            [contact_recieving_email],
            html_message=msg_html,
        )
    except:
        messages.error(request, "Sorry, something went wrong...")

    return messages.success(
        request, "Your message has been sent, I'll contact you shortly."
    )
