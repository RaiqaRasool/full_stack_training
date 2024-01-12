from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from django_6pm import settings
from django_6pm.celery import app


@app.task()
def send_html_email(subject, template_name, context, receipients_list):
    html_content = render_to_string(template_name, context)

    email = EmailMessage(
        subject,
        html_content,
        settings.EMAIL_HOST_USER,
        receipients_list,
    )
    email.content_subtype = "html"

    email.send()
    print("Sent email to: ", receipients_list)
