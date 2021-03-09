# Department email functions
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template


# Support request email
def supportRequestEmail(subject, from_email, to_email, data, type):
    msg_txt = get_template('emails/support_request.txt')
    msg_html = get_template('emails/support_request.html')
    d = {
        'name': data['name'],
        'email': data['email'],
        'type': type,
        'subject': data['subject'],
        'message': data['message'],
    }
    content_txt = msg_txt.render(d)
    content_html = msg_html.render(d)
    message = EmailMultiAlternatives(subject, content_txt, from_email, to_email)
    message.attach_alternative(content_html, "text/html")
    message.send()
