import os
from dotenv import load_dotenv


load_dotenv()

TOKEN_API = os.environ.get('TOKEN_API')
ADMIN_IDS = set(map(int ,os.environ.get('ADMIN_IDS').split()))
PROMO_ID = os.environ.get('PROMO_ID')