# RSP email load_functions
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template

# Email comment to PI
def piCommentEmail(subject, from_email, to_email, data):
    msg_txt = get_template('emails/status_change.txt')
    msg_html = get_template('emails/status_change.html')
    d = {
        'title': data['proj_title'],
        'pi': data['pi_name'],
        'rsp_id': data['proj_identifier'],
        'committee': data['status_type'],
        'commented_by': data['modified_by_user'],
        'date': data['status_change_date'],
        'comments': data['status_comment']
    }
    content_txt = msg_txt.render(d)
    content_html = msg_html.render(d)
    message = EmailMultiAlternatives(subject, content_txt, from_email, to_email)
    message.attach_alternative(content_html, "text/html")
    message.send()

# Email status notification to PI
def piStatusEmail(subject, from_email, to_email, data):
    msg_txt = get_template('emails/status_change.txt')
    msg_html = get_template('emails/status_change.html')
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

# Email notification for committee
def committeeStatusEmail(subject, from_email, to_email, data):
    msg_txt = get_template('emails/status_change.txt')
    msg_html = get_template('emails/status_change.html')
    d = {
        'title': data['proj_title'],
        'pi': data['pi_name'],
        'rsp_id': data['proj_identifier'],
        'committee': data['status_type'],
        'url': ''
    }
    content_txt = msg_txt.render(d)
    content_html = msg_html.render(d)
    message = EmailMultiAlternatives(subject, content_txt, from_email, to_email)
    message.attach_alternative(content_html, "text/html")
    message.send()

# Email overall approval to OSP
def ospApprovalEmail(subject, from_email, to_email, data):
    msg_txt = get_template('emails/status_change.txt')
    msg_html = get_template('emails/status_change.html')
    pi_name = data['proj_last_name'] + ', ' + data['proj_first_name']
    d = {
        'title': data['proj_title'],
        'pi': pi_name,
        'location': data['proj_loc'],
        'rsp_id': data['proj_identifier'],
        'irb': data['IRBnet_id'],
        'itp': data['proj_itp_id'],
        'overall_status': data['overall_status'][3],
        'date': ''
    }
    content_txt = msg_txt.render(d)
    content_html = msg_html.render(d)
    message = EmailMultiAlternatives(subject, content_txt, from_email, to_email)
    message.attach_alternative(content_html, "text/html")
    message.send()
