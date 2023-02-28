import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

USER = os.getenv('TEST1')
print(USER)
USER = os.getenv('TEST2')
print(USER)
USER = os.getenv('TEST3')
print(USER)