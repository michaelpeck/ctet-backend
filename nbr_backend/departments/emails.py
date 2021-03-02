# Department email functions
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template


# Support request email
def supportRequestEmail(subject, from_email, to_email, data):
    msg_txt = get_template('emails/support_request.txt')
    msg_html = get_template('emails/support_request.html')
    d = {
        'title': data['proj_title'],
        'pi': data['pi_name'],
        'rsp_id': data['proj_identifier'],
        'committee': data['status_type'],
        'new_status': data['status'],
        'commented_by': data['modified_by_user'],
        'date': data['status_change_date'],
        'comments': data['status_comment']
    }
    content_txt = msg_txt.render(d)
    content_html = msg_html.render(d)
    message = EmailMultiAlternatives(subject, content_txt, from_email, to_email)
    message.attach_alternative(content_html, "text/html")
    message.send()
