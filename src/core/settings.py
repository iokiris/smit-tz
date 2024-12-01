import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env.auth'))

database_url = os.getenv("DATABASE_URL")

declared_cost = 10000