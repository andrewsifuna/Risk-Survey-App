import streamlit as st
import time
import math
import requests
import streamlit.components.v1 as components
from geopy.distance import geodesic
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Equity Risk Survey System", layout="wide")

# =========================
# EQUITY STYLING
# =========================
st.markdown("""
<style>
body { background-color: #0E1117; }
h1, h2, h3 { color: #008751; }

.stButton>button {
    background-color: #008751;
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 100%;
    font-weight: bold;
}
.stButton>button:hover { background-color: #006F42; }

.stProgress > div > div { background-color: #008751; }
input, textarea { border-radius: 8px !important; }
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION INIT
# =========================
if "step" not in st.session_state:
    st.session_state.step = 0

if "data" not in st.session_state:
    st.session_state.data = {}

d = st.session_state.data

# =========================
# SECTIONS
# =========================
sections = [
    "Welcome","Client Info","Contacts & Control","Business Overview",
    "Site Buildings","Situation","Exposure","Storage","Utilities",
    "Employees","Health & Safety","Fire Protection","Fire Services",
    "Security","Cash/Stocks","Computers","Waste Disposal","Perils",
    "Risk Appraisal","Process","Hazardous Substances","Unions",
    "Losses Report","Interruption Analysis","Submit"
]

# =========================
# NAVIGATION
# =========================
def next_step():
    if st.session_state.step < len(sections) - 1:
        st.session_state.step += 1

def prev_step():
    if st.session_state.step > 0:
        st.session_state.step -= 1

def save_progress():
    st.success("Progress saved!")

section = sections[st.session_state.step]

# =========================
# HEADER
# =========================
progress = st.session_state.step / (len(sections) - 1)
st.progress(progress)
st.markdown("<h1>🏦 Equity Risk Survey System</h1>", unsafe_allow_html=True)

# =========================
# WELCOME
# =========================
if section == "Welcome":
    st.image("equity_logo.png", width=300)
    st.markdown("<h2 style='text-align:center; color:#008751;'>Welcome to Equity Risk Survey</h2>", unsafe_allow_html=True)
    st.markdown("### Click Next to begin")

# =========================
# CLIENT INFO
# =========================
elif section == "Client Info":
    st.header("Client Information")

    d["insured"] = st.text_input("Insured Name", d.get("insured", ""))
    d["address"] = st.text_input("Physical Address", d.get("address", ""))

    # GPS via browser
    components.html("""
    <script>
    navigator.geolocation.getCurrentPosition(function(position) {
        const coords = position.coords.latitude + "," + position.coords.longitude;
        const inputs = window.parent.document.querySelectorAll('input[type="text"]');
        if (inputs.length > 2) {
            inputs[2].value = coords;
            inputs[2].dispatchEvent(new Event('input', { bubbles: true }));
        }
    });
    </script>
    """, height=0)

    if st.button("📍 Use Approx Location"):
        res = requests.get("https://ipinfo.io/json").json()
        d["gps"] = res.get("loc")

    d["gps"] = st.text_input("GPS Coordinates", d.get("gps", ""))

    # Distance calculation
    if d.get("gps") and "," in d["gps"]:
        lat, lon = map(float, d["gps"].split(","))
        distance = geodesic((lat, lon), (-1.286389, 36.817223)).km
        d["distance"] = f"{distance:.2f} km"
        st.success(f"Distance from Nairobi: {distance:.2f} km")

    d["distance"] = st.text_input("Distance from Town", d.get("distance", ""))

    # ✅ CAMERA BACK
    d["client_photo"] = st.camera_input("📸 Capture Front View")

# =========================
elif section == "Contacts & Control":
    st.header("Contacts & Control")
    d["contacts"] = st.text_area("Contacts")

elif section == "Business Overview":
    st.header("Business Overview")
    d["business"] = st.text_input("Nature of Business")
    d["background"] = st.text_area("Background")

# =========================
# OTHER SECTIONS
# =========================
elif section == "Site Buildings":
    st.header("Site Buildings")
    d["building_age"] = st.text_input("Age, Structure & Roofing")
    d["floors"] = st.text_input("Floors")

elif section == "Situation":
    st.header("Situation")
    d["physical_address"] = st.text_input("Physical Address")
    d["distance_town"] = st.text_input("Distance From Town")

elif section == "Exposure":
    st.header("Exposure")
    d["exposure_internal"] = st.text_area("Internal Exposure")
    d["exposure_external"] = st.text_area("External Exposure")

elif section == "Storage":
    st.header("Storage")
    d["storage"] = st.text_area("Storage Details")

elif section == "Utilities":
    st.header("Utilities")
    d["electricity"] = st.text_area("Electricity")
    d["water"] = st.text_area("Water")

elif section == "Employees":
    st.header("Employees")
    d["employees"] = st.text_area("Employee Details")

elif section == "Health & Safety":
    st.header("Health & Safety")
    d["safety"] = st.text_area("Safety Measures")

elif section == "Fire Protection":
    st.header("Fire Protection")
    d["fire"] = st.text_area("Fire Protection Systems")

elif section == "Fire Services":
    st.header("Fire Services")
    d["fire_services"] = st.text_area("Nearby Fire Services")

elif section == "Security":
    st.header("Security")
    d["security"] = st.text_area("Security Systems")

elif section == "Cash/Stocks":
    st.header("Cash / Stocks")
    d["cash"] = st.text_area("Cash Handling")

elif section == "Computers":
    st.header("Computers")
    d["computers"] = st.text_area("IT Systems")

elif section == "Waste Disposal":
    st.header("Waste Disposal")
    d["waste"] = st.text_area("Waste Management")

elif section == "Perils":
    st.header("Perils")
    d["perils"] = st.text_area("Perils")

# =========================
# PROCESS
# =========================
elif section == "Process":
    st.header("Process")
    process = st.text_area("Describe Production Process")

    hazards = []
    if "boiler" in process.lower(): hazards.append("Explosion Risk")
    if "chemical" in process.lower(): hazards.append("Chemical Risk")

    for h in hazards:
        st.warning(h)

    st.metric("Risk Score", f"{min(len(hazards)*20,100)}%")

# =========================
# LOSS ESTIMATION
# =========================
elif section == "Risk Appraisal":
    st.header("Loss Estimation")
    sum_insured = st.number_input("Sum Insured", value=1000000.0)
    loss_percent = st.slider("Damage %", 0, 100, 20)

    loss = sum_insured * loss_percent / 100
    st.success(f"Loss: {loss:,.2f}")

# =========================
# 🔥 FINAL MISSING SECTIONS (FIXED)
# =========================
elif section == "Hazardous Substances":
    st.header("Hazardous Substances")
    d["hazardous"] = st.text_area("List Hazardous Substances")

elif section == "Unions":
    st.header("Unions")
    d["unions"] = st.text_area("Union Presence / Issues")

elif section == "Losses Report":
    st.header("Losses Report")
    d["losses"] = st.text_area("Past Losses / Claims History")

elif section == "Interruption Analysis":
    st.header("Interruption Analysis")
    d["interruption"] = st.text_area("Business Interruption Details")

# =========================
# SUBMIT
# =========================
elif section == "Submit":
    st.header("Generate Report")

    if st.button("Generate PDF"):
        c = canvas.Canvas("report.pdf")
        y = 750
        for k, v in d.items():
            c.drawString(40, y, f"{k}: {v}")
            y -= 20
        c.save()

        with open("report.pdf", "rb") as f:
            st.download_button(
        label="⬇️ Download Report",
        data=f,
        file_name="Risk_Report.pdf",
        mime="application/pdf"
    )

# =========================
# 🚨 FALLBACK (NO BLANK SCREENS EVER)
# =========================
else:
    st.warning(f"⚠️ Section '{section}' not yet implemented")

# =========================
# NAV
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    if st.session_state.step > 0:
        st.button("⬅️ Previous", on_click=prev_step)

with col2:
    st.button("💾 Save", on_click=save_progress)

with col3:
    if st.session_state.step < len(sections) - 1:
        st.button("Next ➡️", on_click=next_step)
