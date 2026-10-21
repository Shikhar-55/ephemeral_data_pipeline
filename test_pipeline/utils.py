# utils.py
# Helper functions used by main.py. Only the Python standard library is used.

import datetime
import json
import logging
import sys
import urllib.request

import test_pipeline.config as config


def setup_logging():
    """Send log messages to the screen (stdout) so Airflow can capture them."""
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    return logging.getLogger("pipeline")


def check_config():
    """Stop early with a clear message if a required setting is missing."""
    if not config.SUPABASE_URL:
        raise RuntimeError("Missing environment variable: SUPABASE_URL")
    if not config.SUPABASE_KEY:
        raise RuntimeError("Missing environment variable: SUPABASE_SERVICE_KEY")


def fetch_price():
    """Call the Coinbase API and return the current BTC price as a float."""
    request = urllib.request.Request(config.API_URL, headers={"User-Agent": "pipeline-demo"})
    with urllib.request.urlopen(request, timeout=config.HTTP_TIMEOUT) as response:
        data = json.load(response)
    return float(data["data"]["amount"])


def insert_row(run_time, price):
    """Insert one row (run_time, price) into the Supabase table."""
    url = config.SUPABASE_URL + "/rest/v1/" + config.SUPABASE_TABLE

    row = {"run_time": run_time, "price": price}
    body = json.dumps(row).encode("utf-8")

    headers = {
        "apikey": config.SUPABASE_KEY,
        "Authorization": "Bearer " + config.SUPABASE_KEY,
        "Content-Type": "application/json",
        "Prefer": "return=minimal",
    }

    request = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(request, timeout=config.HTTP_TIMEOUT) as response:
        if response.status not in (200, 201):
            raise RuntimeError("Supabase insert failed with HTTP " + str(response.status))
