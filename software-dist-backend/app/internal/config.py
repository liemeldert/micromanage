import os
from dotenv import load_dotenv

required_env = ['DATABASE_CONNECTION_URL', 'AUTH0_TENANT_URL', 'AUTH0_AUDIENCE']

for each in required_env:
    env = os.getenv(each)
    if each is None:
        raise ValueError(f'{each} is not set')

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
AUTH0_URL = os.getenv('AUTH0_TENANT_URL')
AUTH0_AUDIENCE = os.getenv('AUTH0_AUDIENCE')
AUTH0_SCOPES = os.getenv('AUTH0_SCOPES')
aws_endpoint = os.getenv('AWS_ENDPOINT')  # https://s3.wasabisys.com
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

