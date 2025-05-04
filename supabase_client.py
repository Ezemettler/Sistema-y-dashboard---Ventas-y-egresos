# supabase_client.py
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()  # Carga las variables desde .env

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
