# pages/2_🛒_Community_Board.py
import pandas as pd
import streamlit as st
from sheets_db import load_listings, save_listing

st.set_page_config(page_title="Community Board", page_icon="🛒", layout="wide")
st.title("🛒 Community Board")
st.write("Buy or sell old electronics with other students.")

# ----- Posting form -----
with st.expander("➕ Post a listing", expanded=False):
    with st.form("listing_form", clear_on_submit=True):
        listing_type = st.radio("I want to", ["Sell", "Buy"], horizontal=True)
        device_name = st.text_input("Device name (e.g., Arduino Uno R3)")
        condition = st.selectbox("Condition", ["Working", "Needs repair", "For parts only"])
        price_php = st.number_input("Price (PHP)", min_value=0, value=0, step=50)
        contact = st.text_input("Contact (phone, email, or social handle)")
        description = st.text_area("Description (optional)", max_chars=300)

        submitted = st.form_submit_button("Post listing")

    if submitted:
        if not device_name.strip() or not contact.strip():
            st.error("Please enter a device name and a contact method.")
        else:
            try:
                save_listing({
                    "type": listing_type,
                    "device": device_name.strip(),
                    "condition": condition,
                    "price_php": int(price_php),
                    "contact": contact.strip(),
                    "description": description.strip(),
                })
                st.success("Your listing has been posted.")
            except Exception as error:
                st.error("Could not save your listing. Please try again in a moment.")
                st.caption(f"Technical details: {error}")

# ----- Browse listings -----
st.subheader("Browse listings")

try:
    listings = load_listings()
except Exception as error:
    st.error("Could not load listings from Google Sheets.")
    st.caption(f"Technical details: {error}")
    st.stop()

if listings.empty:
    st.info("No listings yet. Be the first to post one!")
else:
    filter_type = st.radio("Show", ["All", "Sell", "Buy"], horizontal=True)

    if filter_type != "All":
        listings = listings[listings["type"] == filter_type]

    # Show newest first
    listings = listings.iloc[::-1]

    for _, row in listings.iterrows():
        with st.container(border=True):
            st.markdown(f"**{row['type']}: {row['device']}**")
            st.write(f"Condition: {row['condition']} · Price: ₱{int(row['price_php']):,}")
            if pd.notna(row["description"]) and str(row["description"]).strip():
                st.write(row["description"])
            st.caption(f"Contact: {row['contact']}")