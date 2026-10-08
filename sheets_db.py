# sheets_db.py
# Reads and writes community listings to a Google Sheet.

import gspread
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# These must match the header row in the Google Sheet, in the same order
COLUMNS = ["type", "device", "condition", "price_php", "contact", "description"]


@st.cache_resource
def get_listings_sheet():
    """Connect to the Google Sheet once and reuse the connection."""
    credentials = Credentials.from_service_account_info(
        dict(st.secrets["gcp_service_account"]),
        scopes=SCOPES,
    )
    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_url(st.secrets["sheets"]["listings_url"])
    return spreadsheet.sheet1  # The first tab in the sheet


@st.cache_data(ttl=30)
def load_listings():
    """Return all listings as a DataFrame. Refreshes every 30 seconds."""
    sheet = get_listings_sheet()
    records = sheet.get_all_records()  # List of dicts, one per row

    if not records:
        return pd.DataFrame(columns=COLUMNS)

    return pd.DataFrame(records)


def save_listing(new_listing):
    """Add one listing as a new row at the bottom of the sheet."""
    sheet = get_listings_sheet()
    row = [new_listing[column] for column in COLUMNS]
    sheet.append_row(row, value_input_option="USER_ENTERED")

    # Clear the cached listings so the new post appears right away
    load_listings.clear()