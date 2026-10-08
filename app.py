import streamlit as st

# 1. Page Setup
st.set_page_config(page_title="E-Waste & Repair Hub", page_icon="♻️")
st.title("♻️ E-Waste & Device Repair Hub")
st.write("Find repair guides, calculate environmental impact, and locate recycling drop-offs.")

# 2. The Database
devices_db = {
    "iphone 13": {
        "brand": "Apple",
        "name": "iPhone 13",
        "repair_score": 5,
        "co2_saved_kg": 64,
        "common_issues": ["Battery degradation", "Cracked screen", "Charging port failure"],
        "diy_difficulty": "Hard"
    },
    "arduino uno": {
        "brand": "Arduino",
        "name": "Arduino Uno R3",
        "repair_score": 10,
        "co2_saved_kg": 2,
        "common_issues": ["Fried ATmega328P chip", "Broken USB port connector"],
        "diy_difficulty": "Easy"
    }
}

# 3. Tabs Navigation Layout
tab1, tab2, tab3 = st.tabs(["🔧 Repair Guide", "🌱 Impact Calculator", "📍 Recycling Drop-offs"])

# ==========================================
# TAB 1: REPAIR GUIDE
# ==========================================
with tab1:
    def set_search(name):
        st.session_state["search_box"] = name

    search_query = st.text_input(
        "Search for a device (e.g., iPhone 13, Arduino Uno)",
        key="search_box"
    )

    # Suggestion buttons
    st.caption("Suggestions:")
    suggestion_keys = list(devices_db)[:4]
    cols = st.columns(len(suggestion_keys))
    for idx, key in enumerate(suggestion_keys):
        name = devices_db[key]["name"]
        cols[idx].button(name, on_click=set_search, args=(name,), key=f"btn_{key}_{idx}")

    def show_name(key):
        return f"{devices_db[key]['brand']} - {devices_db[key]['name']}"

    if search_query:
        query_clean = search_query.lower().replace(" ", "")

        matches = []
        for key in devices_db:
            name_clean = devices_db[key]["name"].lower().replace(" ", "")
            brand_clean = devices_db[key]["brand"].lower().replace(" ", "")
            key_clean = key.replace(" ", "")
            if query_clean in key_clean or query_clean in name_clean or query_clean in brand_clean:
                matches.append(key)

        if len(matches) == 0:
            st.error("Device not found in our database.")
            st.write("Devices we have:")
            for key in devices_db:
                st.write(f"- **{devices_db[key]['brand']}** {devices_db[key]['name']}")
        else:
            if len(matches) > 1:
                st.info(f"{len(matches)} devices matched your search.")
                chosen_key = st.selectbox("Pick a device", matches, format_func=show_name, key="device_select_box")
            else:
                chosen_key = matches[0]

            device = devices_db[chosen_key]
            
            # Display Brand (Gap 6)
            st.caption(f"Brand: **{device['brand']}**")
            st.success(f"Found: **{device['brand']} {device['name']}**")

            # Stats
            col1, col2, col3 = st.columns(3)
            col1.metric("Repairability Score", f"{device['repair_score']}/10")
            col2.metric("DIY Difficulty", device['diy_difficulty'])
            col3.metric("CO2 Saved by Repair", f"{device['co2_saved_kg']} kg")

            st.subheader("Common Issues & Fixes")
            for issue in device['common_issues']:
                st.write(f"- {issue}")

# ==========================================
# TAB 2: IMPACT CALCULATOR
# ==========================================
with tab2:
    st.header("🌱 Calculate Your Environmental Impact")
    st.write("See how much carbon you keep out of the atmosphere by choosing repair over buying new.")

    selected_calc_key = st.selectbox(
        "Select a device you repaired or reused:",
        options=list(devices_db.keys()),
        format_func=lambda key: f"{devices_db[key]['brand']} - {devices_db[key]['name']}",
        key="calc_device_select"
    )

    quantity = st.number_input("How many units?", min_value=1, value=1, step=1, key="calc_quantity_input")

    if selected_calc_key:
        calc_device = devices_db[selected_calc_key]
        unit_co2 = calc_device["co2_saved_kg"]
        total_co2 = unit_co2 * quantity

        trees_equivalent = total_co2 / 22.0
        km_driven_equivalent = total_co2 / 0.17

        st.markdown("---")
        st.subheader("Your Impact Summary")

        m_col1, m_col2 = st.columns(2)
        m_col1.metric("Total CO2 Emissions Prevented", f"{total_co2} kg")
        m_col2.metric("Devices Saved", f"{quantity} unit(s)")

        st.subheader("What does this mean?")
        st.write(f"🌳 **Trees:** Equal to the annual CO₂ absorption of approximately **{trees_equivalent:.1f} trees**.")
        st.write(f"🚗 **Driving:** Equal to avoiding roughly **{km_driven_equivalent:.0f} km** of passenger car driving.")

# ==========================================
# TAB 3: RECYCLING DROP-OFFS
# ==========================================
with tab3:
    st.header("📍 Find Recycling Drop-offs")
    st.info("Recycling location search and mapping features will be added here once researched.")
