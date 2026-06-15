"""Branded transactional email helper.

Renders a matching pair of templates — ``emails/<name>.txt`` (plain-text) and
``emails/<name>.html`` (branded) — and sends them as a single multipart message.
Clients that can't render HTML fall back to the text part.
"""
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_html_email(subject, to, template, context=None):
    """Render emails/<template>.{txt,html} and send as multipart.

    ``to`` may be a single address or a list. ``from`` is DEFAULT_FROM_EMAIL.
    """
    context = context or {}
    recipients = [to] if isinstance(to, str) else list(to)
    text_body = render_to_string(f"emails/{template}.txt", context)
    html_body = render_to_string(f"emails/{template}.html", context)
    message = EmailMultiAlternatives(subject, text_body, None, recipients)
    message.attach_alternative(html_body, "text/html")
    message.send()
