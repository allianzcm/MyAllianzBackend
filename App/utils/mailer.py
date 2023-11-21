from django.core.mail import send_mail 

def mailer(msg):
    subject = 'Test Email'
    from_email = 'urben.fotso@allianz.com'
    recipient_list = ['fotsopires10@gmail.com']
    send_mail(subject, msg, from_email, recipient_list)