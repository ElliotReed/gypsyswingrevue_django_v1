from decouple import config

from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


contact_from_email = config("CONTACT_FROM_EMAIL")
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


def send_contact_form(data):
    name = data["name"]
    sender_message = data["message"]
    sender_email = data["email"]

    body = (
        "<div style='font-family: Arial, Helvetica, sans-serif; font-size: 15px; color: #222;'>"
        f"<p><strong>{name}</strong> ({sender_email})</p>"
        f"<p>{sender_message.replace(chr(10), '<br>')}</p>"
        "</div>"
    )

    email = EmailMessage(
        subject="Gypsy Swing Revue contact message",
        body=body,
        from_email=contact_from_email,
        to=[contact_recieving_email],
        reply_to=[sender_email],
    )
    email.content_subtype = "html"
    email.send()
