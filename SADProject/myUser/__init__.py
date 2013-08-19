from django.contrib.auth.models import Group
from django.core.mail import EmailMessage

def inform_admin(subject, message):
    inform_group('A',subject,message)

def inform_warehouse_manager(subject, message):
    inform_group('S',subject,message)

def inform_purchase_agent(subject, message):
    inform_group('B',subject,message)

def inform_trustee(subject,message):
    inform_group('T',subject,message)

def inform_user(user, message, subject):
    if user==None:
        return
    sendMail([user.email],subject,message)
def inform_group(group,subject,message):
    users = Group.objects.get(name=group).user_set.all()
    to_list = []
    for user in users:
        to_list.append(user.email)
    sendMail(emails=to_list,subject=subject,message=message)
def sendMail(emails,subject,message):
    msg = EmailMessage(subject=subject,from_email="admin@mehranik.com",to=emails,body=message)
    msg.content_subtype = "html"
    msg.send()