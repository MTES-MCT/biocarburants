import time
import datetime
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from core.models import Entity, UserRights
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from accounts.tokens import account_activation_token
from django_otp.plugins.otp_email.models import EmailDevice

class AccountTest(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user_name = 'Jean Test'
        self.user_email = 'foobar@example.com'
        self.user_password = 'totopouet'
        self.user1 = user_model.objects.create_user(email='testuser1@toto.com', name='Le Super Testeur 1', password='totopouet')

    def test_register(self):
        # go to register page
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        # send form with missing data
        response = self.client.post(reverse('register'), {'name': self.user_name, 'email': self.user_email, 'password1': self.user_password})
        self.assertEqual(response.status_code, 200)
        usermodel = get_user_model()
        nb_users = len(usermodel.objects.filter(email=self.user_email))
        self.assertEqual(nb_users, 0)

        # send form normally
        response = self.client.post(reverse('register'), {'name': self.user_name, 'email': self.user_email, 'password1': self.user_password, 'password2': self.user_password})
        self.assertEqual(response.status_code, 302)
        nb_users = len(usermodel.objects.filter(email=self.user_email))
        self.assertEqual(nb_users, 1)

        # try to register an already existing user
        response = self.client.post(reverse('register'), {'name': self.user_name, 'email': self.user_email, 'password1': self.user_password, 'password2': self.user_password})
        self.assertEqual(response.status_code, 200)
        nb_users = len(usermodel.objects.filter(email=self.user_email))
        self.assertEqual(nb_users, 1) # no additional user created

        # submit wrong activation link
        response = self.client.get(reverse('activate', kwargs={'uidb64': 'blablabla', 'token': 'blablabla'}))
        self.assertEqual(response.status_code, 200)
        user = usermodel.objects.get(email=self.user_email)
        self.assertEqual(user.is_active, False)

        # request to resend another activation link
        response = self.client.get(reverse('resend-activation-link'))
        self.assertEqual(response.status_code, 200)        
        
        response = self.client.post(reverse('resend-activation-link'), {'email': "wrongemail@example.com"})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('resend-activation-link'), {'email': self.user_email})
        self.assertEqual(response.status_code, 200)      

        # submit good activation link
        user = usermodel.objects.get(email=self.user_email)
        data = {
            'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),        
        }
        response = self.client.get(reverse('activate',  kwargs=data))
        self.assertEqual(response.status_code, 200)
        user = usermodel.objects.get(email=self.user_email)
        self.assertEqual(user.is_active, True)        


    def test_ro_pages(self):
        loggedin = self.client.login(username='testuser1@toto.com', password='totopouet')
        self.assertTrue(loggedin)        
        response = self.client.get(reverse('account-activation-sent'))
        self.assertEqual(response.status_code, 200)


    def test_login(self):
        user_model = get_user_model()
        user_model.objects.create_user(email=self.user_email, name='Le Super Testeur 1', password=self.user_password)

        # try to login with non existent user
        response = self.client.post(reverse('login'), {'username': 'bademail', 'password': 'badpasword'})
        self.assertEqual(response.status_code, 200)
        # try to login with existing user but bad password
        response = self.client.post(reverse('login'), {'username': self.user_email, 'password': 'badpasword'})
        self.assertEqual(response.status_code, 200)
        # login
        response = self.client.post(reverse('login'), {'username': self.user_email, 'password': self.user_password})
        self.assertEqual(response.status_code, 302) # be redirected to otp_verify page
        self.assertEqual(response.url, reverse('otp-verify'))
        # load otp-verify page to generate token
        response = self.client.get(reverse('otp-verify'))
        self.assertEqual(response.status_code, 200)              
        # try to access another page -> 403
        response = self.client.get(reverse('api-v3-settings-get'))
        self.assertEqual(response.status_code, 403)
        # ensure an otp token has been generated
        usermodel = get_user_model()
        user = usermodel.objects.get(email=self.user_email)
        device = EmailDevice.objects.get(user=user)
        self.assertIsNotNone(device.token)
        # submit wrong otp -> try to access another page -> 403
        response = self.client.post(reverse('otp-verify'), {'otp_token': '111111'})
        self.assertEqual(response.status_code, 200)        
        response = self.client.get(reverse('api-v3-settings-get'))
        self.assertEqual(response.status_code, 403)

        # submit expired OTP
        time.sleep(2)
        device.valid_until = timezone.now() - datetime.timedelta(seconds=1)
        device.save()
        response = self.client.post(reverse('otp-verify'), {'otp_token': device.token})
        self.assertEqual(response.status_code, 200) # no redirect

        # send form without otp token
        response = self.client.post(reverse('otp-verify'), {'randomfield': 'testing'})
        self.assertEqual(response.status_code, 200)

        # trigger throttle
        device.throttling_failure_count = 10
        device.save()
        response = self.client.post(reverse('otp-verify'), {'otp_token': device.token})
        self.assertEqual(response.status_code, 200) # no redirect

        # resend otp code by email
        response = self.client.get(reverse('resend-otp-code'))
        self.assertEqual(response.status_code, 200)        

        # submit good otp
        # wait (otp wait time 1,2,4,8 seconds etc..)
        device.throttling_failure_count = 0
        device.valid_until = timezone.now() + datetime.timedelta(seconds=10)
        device.save()
        response = self.client.post(reverse('otp-verify'), {'otp_token': device.token})
        self.assertEqual(response.status_code, 302) #  redirected to home page
        # check that we are logged in
        response = self.client.get(reverse('api-v3-settings-get'))
        self.assertEqual(response.status_code, 200)


    def submit_otp(self, user_email):
        usermodel = get_user_model()
        response = self.client.get(reverse('otp-verify'))
        self.assertEqual(response.status_code, 200) 

        user = usermodel.objects.get(email=user_email)
        device = EmailDevice.objects.get(user=user)
        response = self.client.post(reverse('otp-verify'), {'otp_token': device.token})
        self.assertEqual(response.status_code, 302)

    def test_password_change(self):
        loggedin = self.client.login(username='testuser1@toto.com', password='totopouet')
        self.assertTrue(loggedin)

        # otp
        self.submit_otp(user_email='testuser1@toto.com')

        # now the tests:
        response = self.client.get(reverse('custom-password-change'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('custom-password-change'), {'new_password1': 'totopouet02', 'new_password2': 'totopouet02'})
        self.assertEqual(response.status_code, 302) # redirect to password change success page

        self.client.logout()
        loggedin = self.client.login(username='testuser1@toto.com', password='totopouet02')
        self.assertTrue(loggedin)
        self.submit_otp(user_email='testuser1@toto.com')

        response = self.client.get(reverse('custom-password-change-success'))
        self.assertEqual(response.status_code, 200)
