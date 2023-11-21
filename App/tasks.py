from django_q.tasks import async_task
from App.utils.mailer import mailer



def send(msg):
    async_task(mailer , msg)