from imaplib import IMAP4

from django.contrib.auth.models import User, check_password
from django.contrib.auth.backends import ModelBackend
import imaplib
class MyBackend(ModelBackend):
    


    def authenticate(self, username=None, password=None):
        #M = IMAP4('imap.ce.sharif.edu')


        try:
            user = User.objects.get(username = username)  #(settings.ADMIN_LOGIN == username)

            if 1==1:
                return user
            M.login(username,password)


        except User.DoesNotExist:
              return None
        except:
            M.logout()
            return None

        M.logout()
        return user


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None