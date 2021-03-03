# Department email functions
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template


# Support request email
def supportRequestEmail(subject, from_email, to_email, data):
    msg_txt = get_template('emails/support_request.txt')
    d = {
        'name': data['name'],
        'email': data['email'],
        'department': data['department'],
        'subject': data['subject'],
        'message': data['message'],
    }
    content_txt = msg_txt.render(d)
    message = EmailMultiAlternatives(subject, content_txt, from_email, to_email)
    message.send()
