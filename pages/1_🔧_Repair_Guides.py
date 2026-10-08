# pages/1_🔧_Repair_Guides.py
import streamlit as st
from guides_data import DEVICES

st.set_page_config(page_title="Repair Guides", page_icon="🔧", layout="wide")
st.title("🔧 Repair Guides")

search_query = st.text_input(
    "Search for a device",
    placeholder="e.g., iPhone 13, Arduino Uno",
)


def device_matches(query, device_key, device):
    """Return True if every word in the query appears in the device's searchable text."""
    searchable_text = f"{device_key} {device['brand']} {device['name']} {device['category']}".lower()
    query_words = query.lower().split()
    return all(word in searchable_text for word in query_words)


# Find matching devices
if search_query.strip():
    matches = [key for key, device in DEVICES.items() if device_matches(search_query, key, device)]
else:
    matches = list(DEVICES.keys())

if not matches:
    st.error("No device matched your search.")
    st.write("Devices in our database:")
    for key in DEVICES:
        st.write(f"- **{DEVICES[key]['brand']}** {DEVICES[key]['name']}")
    st.stop()

# Let the user choose if several devices matched
if len(matches) > 1:
    chosen_key = st.selectbox(
        f"{len(matches)} devices matched. Pick one:",
        matches,
        format_func=lambda key: f"{DEVICES[key]['brand']} - {DEVICES[key]['name']}",
    )
else:
    chosen_key = matches[0]

device = DEVICES[chosen_key]

st.success(f"Showing guides for **{device['brand']} {device['name']}**")

# Summary metrics
m1, m2, m3 = st.columns(3)
m1.metric("Repairability Score", f"{device['repair_score']}/10")
m2.metric("DIY Difficulty", device["diy_difficulty"])
m3.metric("Common Issues", len(device["issues"]))

st.subheader("Common Issues & Fixes")

# One expandable section per issue
for issue in device["issues"]:
    with st.expander(issue["problem"]):
        st.write(f"**Symptoms:** {issue['symptoms']}")

        st.markdown("**Steps:**")
        for step_number, step in enumerate(issue["steps"], start=1):
            st.write(f"{step_number}. {step}")

        st.warning(f"⚠️ Safety: {issue['safety']}")