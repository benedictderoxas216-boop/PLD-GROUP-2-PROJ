# pages/2_🛒_Community_Board.py
import pandas as pd
import streamlit as st
from sheets_db import (
    MIN_CODE_LENGTH,
    STATUS_AVAILABLE,
    STATUS_UNAVAILABLE,
    hash_code,
    load_listings,
    save_listing,
    update_status,
)

st.set_page_config(page_title="Community Board", page_icon="🛒", layout="wide")
st.title("🛒 Community Board")
st.write("Buy or sell old electronics with other students.")

STATUS_BADGES = {
    STATUS_AVAILABLE: "🟢 Available",
    STATUS_UNAVAILABLE: "🔴 Unavailable",
}

# ----- Posting form -----
with st.expander("➕ Post a listing", expanded=False):
    with st.form("listing_form", clear_on_submit=True):
        listing_type = st.radio("I want to", ["Sell", "Buy"], horizontal=True)
        device_name = st.text_input("Device name (e.g., Arduino Uno R3)")
        condition = st.selectbox("Condition", ["Working", "Needs repair", "For parts only"])
        price_php = st.number_input("Price (PHP)", min_value=0, value=0, step=50)
        contact = st.text_input("Contact (phone, email, or social handle)")
        description = st.text_area("Description (optional)", max_chars=300)
        manage_code = st.text_input(
            f"Manage code (at least {MIN_CODE_LENGTH} characters)",
            type="password",
            help="You'll need this code to mark the item as unavailable or available again.",
        )

        submitted = st.form_submit_button("Post listing")

    if submitted:
        if not device_name.strip() or not contact.strip():
            st.error("Please enter a device name and a contact method.")
        elif len(manage_code.strip()) < MIN_CODE_LENGTH:
            st.error(f"Your manage code must be at least {MIN_CODE_LENGTH} characters.")
        else:
            try:
                save_listing({
                    "type": listing_type,
                    "device": device_name.strip(),
                    "condition": condition,
                    "price_php": int(price_php),
                    "contact": contact.strip(),
                    "description": description.strip(),
                    "status": STATUS_AVAILABLE,
                    "code_hash": hash_code(manage_code),
                })
                st.success(
                    "Your listing has been posted. Keep your manage code safe. "
                    "You need it to mark the item unavailable."
                )
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
    show_closed = st.checkbox("Include unavailable listings", value=False)

    if filter_type != "All":
        listings = listings[listings["type"] == filter_type]

    if not show_closed:
        listings = listings[listings["status"] == STATUS_AVAILABLE]

    if listings.empty:
        st.info("No listings match these filters.")

    # Show newest first
    listings = listings.iloc[::-1]

    for _, row in listings.iterrows():
        sheet_row = int(row["sheet_row"])
        current_status = row["status"]
        stored_hash = row["code_hash"]
        badge = STATUS_BADGES.get(current_status, current_status)

        with st.container(border=True):
            st.markdown(f"**{row['type']}: {row['device']}**  ·  {badge}")
            st.write(f"Condition: {row['condition']} · Price: ₱{int(row['price_php']):,}")

            if pd.notna(row["description"]) and str(row["description"]).strip():
                st.write(row["description"])

            st.caption(f"Contact: {row['contact']}")

            with st.expander("Change status"):
                entered_code = st.text_input(
                    "Manage code",
                    type="password",
                    key=f"code_{sheet_row}",
                )

                if current_status == STATUS_AVAILABLE:
                    button_label = "Mark as unavailable"
                    target_status = STATUS_UNAVAILABLE
                else:
                    button_label = "Mark as available"
                    target_status = STATUS_AVAILABLE

                if st.button(button_label, key=f"toggle_{sheet_row}"):
                    changed = False

                    if not stored_hash:
                        st.error("This listing has no manage code, so it can't be changed here.")
                    elif not entered_code.strip():
                        st.error("Enter the manage code to change this listing.")
                    elif hash_code(entered_code) != stored_hash:
                        st.error("Wrong manage code.")
                    else:
                        try:
                            update_status(sheet_row, target_status)
                            changed = True
                        except Exception as error:
                            st.error("Could not update the status. Please try again.")
                            st.caption(f"Technical details: {error}")

                    if changed:
                        st.rerun()