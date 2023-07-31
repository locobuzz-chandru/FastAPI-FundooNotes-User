from os import getenv

from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM")
REDIS_CONF = {'host': 'localhost', 'port': 6379, 'db': 0}
