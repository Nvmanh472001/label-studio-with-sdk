import os
from label_studio_sdk import Client
import dotenv

dotenv.load_dotenv(dotenv.find_dotenv())

lbs_url = 'http://localhost:8080'
lbs_auth_key = os.getenv("LABEL_STUDIO_USER_TOKEN")

lbs_client = Client(url=lbs_url, api_key=lbs_auth_key)