import dotenv
import os
dotenv.load_dotenv()

SENDER_EMAIL = os.getenv('SENDER_EMAIL')
EMAIL_PASSWD = os.getenv('EMAIL_PASSWD')
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
SENDER_NUMBER = os.getenv('SENDER_NUMBER')
