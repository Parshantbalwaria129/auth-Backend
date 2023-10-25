from twilio.rest import Client
import smtplib
import ssl
from email.mime.text import MIMEText
from .models import EmailOtpModel, phoneOtpModel
from datetime import datetime, timezone
from . import app_settings


class SendEmailOtp:
    def __init__(self, **kargs) -> None:
        self.defaults = {
            'stmpServer': 'smtp.gmail.com',
            'smtpPort': 587,
            'sslContext': ssl.create_default_context(),
            'senderEmail': app_settings.SENDER_EMAIL,
            'emailPasswd': app_settings.EMAIL_PASSWD,
        }

        for key, value in kargs.items():
            if key in self.defaults:
                self.defaults[key] = value

        self.smtpServer = self.defaults['stmpServer']
        self.smtpPort = self.defaults['smtpPort']
        self.context = self.defaults['sslContext']
        self.senderEmail = self.defaults['senderEmail']
        self.emailPasswd = self.defaults['emailPasswd']

    def send_otp(self, recipient_email, otp):
        try:

            subject = 'Your OTP'
            message = f'Your OTP is: {otp}'
            msg = MIMEText(message)
            msg['Subject'] = subject
            msg['From'] = self.senderEmail
            msg['To'] = recipient_email

            with smtplib.SMTP(self.smtpServer, self.smtpPort) as server:
                server.ehlo()
                server.starttls(context=self.context)
                server.ehlo()
                server.login(self.senderEmail, self.emailPasswd)
                server.sendmail(self.senderEmail, [
                                recipient_email], msg.as_string())
                server.quit()
                return True
        except Exception as e:
            print(e)
            return False


class VarifyOTP:
    def __init__(self, **kargs) -> None:
        """
        params:
            otpField: options: email, phone
            otp: otp value
        optional params:
            otpModel: options: EmailOtpModel, phoneOtpModel
            fieldType: options: email, phone
        """
        self.defaults = {
            'otpModel': None,
            'otpField': None,
            'fieldType': None,
            'otp': None,
        }

        for key, value in kargs.items():
            if key in self.defaults:
                self.defaults[key] = value

        self.otpModel = self.defaults['otpModel']
        self.otpField = self.defaults['otpField']
        self.otp = self.defaults['otp']
        if '@' in self.otpField:
            self.fieldType = 'email'
            self.otpModel = EmailOtpModel
        else:
            self.fieldType = 'phone'
            self.otpModel = phoneOtpModel

    def isExist(self):
        # we need to pass email as email=self.otpField in EmailOtpModel and phone as phone=self.otpField in phoneOtpModel
        # because we are using **kargs in __init__ function
        if self.otpModel.objects.filter(otp=self.otp, **{self.fieldType: self.otpField}).exists():
            return True
        else:
            return False

    def isValid(self):
        otpModel = self.otpModel.objects.filter(
            otp=self.otp, **{self.fieldType: self.otpField})
        otpModel = otpModel.get()
        now_with_timezone = datetime.now().replace(tzinfo=timezone.utc)
        if otpModel.validTime > now_with_timezone:
            return True
        else:
            return False

    def delete(self):
        if self.isExist():
            otpModel = self.otpModel.objects.filter(
                otp=self.otp, **{self.fieldType: self.otpField})
            otpModel.delete()


class SendPhoneOtp:
    def __init__(self, **kargs) -> None:
        self.defaults = {
            'account_sid': app_settings.TWILIO_ACCOUNT_SID,
            'auth_token': app_settings.TWILIO_AUTH_TOKEN,
            'sender_number': app_settings.SENDER_NUMBER
        }

    def sendOtp(self, phone, otp):
        try:
            client = Client(self.defaults['account_sid'],
                            self.defaults['auth_token'])
            client.messages \
                .create(
                    body=f"Your otp for subtitle website: {otp}",
                    from_=self.defaults['sender_number'],
                    to=phone
                )
            return True
        except:
            return False
