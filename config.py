# config.py
# All the settings for the pipeline live here.
# Secrets are read from environment variables so they never sit in the code.

import os

# Coinbase public endpoint, no API key needed
API_URL = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
HTTP_TIMEOUT = 20  # seconds

# Supabase settings (set these as environment variables before running)
SUPABASE_URL = os.environ.get("SUPABASE_URL")              # e.g. https://abcdefgh.supabase.co
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")      # service_role key
SUPABASE_TABLE = os.environ.get("SUPABASE_TABLE", "prices")  # defaults to "prices"
