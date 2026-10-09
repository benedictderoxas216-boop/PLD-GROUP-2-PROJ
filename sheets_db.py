# sheets_db.py
# Reads and writes community listings to a Google Sheet.

import hashlib

import gspread
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# These must match the header row in the Google Sheet, in the same order
COLUMNS = [
    "type",
    "device",
    "condition",
    "price_php",
    "contact",
    "description",
    "status",
    "code_hash",
]

STATUS_AVAILABLE = "Available"
STATUS_UNAVAILABLE = "Unavailable"
STATUSES = [STATUS_AVAILABLE, STATUS_UNAVAILABLE]

# Minimum length for a manage code. Longer codes are harder to guess.
MIN_CODE_LENGTH = 4


def hash_code(code):
    """Return a fingerprint of a manage code. The code itself is never stored."""
    digest = hashlib.sha256(code.strip().encode("utf-8")).hexdigest()
    # The prefix stops Google Sheets from reading the hash as a number
    return "sha256:" + digest


def clean_text(value):
    """Turn a sheet value into a clean string. Empty cells become an empty string."""
    text = str(value).strip()
    if text.lower() == "nan":
        return ""
    return text


def normalize_status(value):
    """Old 'Sold' entries count as unavailable. Anything else counts as available."""
    if clean_text(value) in ("Sold", STATUS_UNAVAILABLE):
        return STATUS_UNAVAILABLE
    return STATUS_AVAILABLE


@st.cache_resource
def get_listings_sheet():
    """Connect to the Google Sheet once and reuse the connection."""
    credentials = Credentials.from_service_account_info(
        dict(st.secrets["gcp_service_account"]),
        scopes=SCOPES,
    )
    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_url(st.secrets["sheets"]["listings_url"])
    return spreadsheet.sheet1


@st.cache_data(ttl=30)
def load_listings():
    """Return all listings as a DataFrame. Refreshes every 30 seconds."""
    sheet = get_listings_sheet()
    records = sheet.get_all_records()

    if records:
        listings = pd.DataFrame(records)
    else:
        listings = pd.DataFrame(columns=COLUMNS)

    # Add any missing columns, for example if the sheet header is older
    for column in COLUMNS:
        if column not in listings.columns:
            listings[column] = ""

    listings["status"] = listings["status"].apply(normalize_status)
    listings["code_hash"] = listings["code_hash"].apply(clean_text)

    # Remember each listing's row number in the sheet so we can update it later.
    # Row 1 is the header, so the first data row is row 2.
    listings["sheet_row"] = range(2, len(listings) + 2)

    return listings


def save_listing(new_listing):
    """Add one listing as a new row at the bottom of the sheet."""
    sheet = get_listings_sheet()
    row = [new_listing.get(column, "") for column in COLUMNS]
    sheet.append_row(row, value_input_option="USER_ENTERED")

    # Clear the cached listings so the new post appears right away
    load_listings.clear()


def update_status(sheet_row, new_status):
    """Change the status cell of one listing."""
    sheet = get_listings_sheet()
    status_column = COLUMNS.index("status") + 1  # Sheets columns start at 1
    sheet.update_cell(sheet_row, status_column, new_status)

    # Clear the cache so the change shows up right away
    load_listings.clear()