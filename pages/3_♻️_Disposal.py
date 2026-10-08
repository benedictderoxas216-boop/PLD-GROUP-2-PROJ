# pages/3_♻️_Disposal.py
import streamlit as st

st.set_page_config(page_title="Disposal", page_icon="♻️", layout="wide")
st.title("♻️ Should I Repair, Sell, or Recycle?")
st.write("Answer a few questions about your device to get a recommendation.")

powers_on = st.radio("Does the device power on?", ["Yes", "No"], horizontal=True)
physically_damaged = st.radio("Is the device physically damaged (cracks, water damage, swelling)?", ["No", "Yes"], horizontal=True)
has_battery_swelling = st.checkbox("The battery is swollen or the device is hot when charging")
repair_cost_known = st.radio(
    "Is the repair cheaper than 50% of the price of a similar used device?",
    ["Yes", "No", "Not sure"],
    horizontal=True,
)
has_personal_data = st.checkbox("The device still contains personal data I have not wiped")

st.markdown("---")

if st.button("Get recommendation", type="primary"):
    st.subheader("Recommendation")

    if has_battery_swelling:
        st.error("🔥 **Recycle immediately at a battery-safe drop-off.**")
        st.write("A swollen lithium battery is a fire risk. Store the device away from flammable materials and do not charge it.")

    elif powers_on == "No" and physically_damaged == "Yes":
        st.error("♻️ **Recycle it.**")
        st.write("The device is probably beyond an easy repair. Use it for parts if you can, then recycle the rest.")

    elif powers_on == "Yes" and repair_cost_known == "Yes":
        st.success("🔧 **Repair it.**")
        st.write("A repair is cost-effective and keeps the device in use. Check the Repair Guides page for steps.")

    elif powers_on == "Yes" and repair_cost_known == "No":
        st.info("🛒 **Sell it as-is on the Community Board.**")
        st.write("The repair costs more than the device is worth to most buyers. Someone else may repair it or use it for parts.")

    else:
        st.warning("🤔 **Get a quote first.**")
        st.write("Check the repair price at a local shop or look up the part price online, then return to this page.")

    if has_personal_data:
        st.warning("🔐 **Before you sell, recycle, or donate:** wipe all personal data, sign out of accounts, and remove any SIM card or memory card.")