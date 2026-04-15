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

    placeholder = st.empty()
    for i in range(30):
        y_anim = math.sin(i / 5) * 10
        placeholder.markdown(
            f"<h2 style='text-align:center; color:#008751;'>Welcome to Equity Risk Survey</h2>",
            unsafe_allow_html=True
        )
        time.sleep(0.02)

    st.markdown("### Click Next to begin")

# =========================
# CLIENT INFO + REAL GPS
# =========================
elif section == "Client Info":
    st.header("Client Information")

    d["insured"] = st.text_input("Insured Name", d.get("insured", ""))
    d["address"] = st.text_input("Physical Address", d.get("address", ""))

    # 🌍 OPTION 1 — REAL GPS (Browser)
    st.markdown("### 📍 Get Real GPS Location")

    components.html("""
    <script>
    navigator.geolocation.getCurrentPosition(function(position) {
        const coords = position.coords.latitude + "," + position.coords.longitude;
        const streamlitDoc = window.parent.document;
        const inputs = streamlitDoc.querySelectorAll('input[type="text"]');
        if (inputs.length > 2) {
            inputs[2].value = coords;
            inputs[2].dispatchEvent(new Event('input', { bubbles: true }));
        }
    });
    </script>
    """, height=0)

    # 🌍 OPTION 2 — IP FALLBACK BUTTON
    def get_location():
        try:
            res = requests.get("https://ipinfo.io/json").json()
            return res.get("loc"), res.get("city"), res.get("country")
        except:
            return "Unavailable", "-", "-"

    if st.button("📍 Use Approx Location (Fallback)"):
        loc, city, country = get_location()
        d["gps"] = loc
        st.success(f"Location updated: {loc} ({city}, {country})")

    # GPS INPUT
    d["gps"] = st.text_input("GPS Coordinates", d.get("gps", ""))

    # 📏 AUTO DISTANCE CALCULATION (NAIROBI)
    town_coords = (-1.286389, 36.817223)

    if d.get("gps") and "," in d["gps"]:
        try:
            lat, lon = map(float, d["gps"].split(","))
            distance_km = geodesic((lat, lon), town_coords).km

            st.success(f"📏 Distance from Nairobi: {distance_km:.2f} km")

            d["distance"] = f"{distance_km:.2f} km"
        except:
            st.warning("Invalid GPS format")

    d["distance"] = st.text_input("Distance from Town", d.get("distance", ""))

    d["client_photo"] = st.camera_input("Capture Front View")

# =========================
elif section == "Contacts & Control":
    st.header("Contacts & Control")
    d["contacts"] = st.text_area("Contacts", d.get("contacts", ""))

elif section == "Business Overview":
    st.header("Business Overview")
    d["business"] = st.text_input("Nature of Business", d.get("business", ""))
    d["background"] = st.text_area("Background", d.get("background", ""))

# =========================
# PROCESS + AI HAZARDS
# =========================
elif section == "Process":
    st.header("Process")

    process = st.text_area("Describe Production Process")

    def detect_hazards(process):
        p = process.lower()
        hazards = []

        if "boiler" in p or "steam" in p:
            hazards.append("🔥 Explosion Risk")
        if "chemical" in p or "acid" in p:
            hazards.append("☣️ Chemical Exposure")
        if "machine" in p:
            hazards.append("⚙️ Mechanical Injury")
        if "flammable" in p:
            hazards.append("🔥 Fire Risk")
        if "dust" in p:
            hazards.append("💥 Dust Explosion")

        return hazards

    hazards = detect_hazards(process)

    st.subheader("⚠️ Auto Detected Hazards")

    if hazards:
        for h in hazards:
            st.warning(h)
    else:
        st.info("No major hazards detected")

    risk_score = min(len(hazards) * 20, 100) if hazards else 10
    st.metric("Risk Score", f"{risk_score}%")

    d["process"] = process
    d["hazards"] = ", ".join(hazards)

# =========================
# LOSS ESTIMATION
# =========================
elif section == "Risk Appraisal":
    st.header("💰 Loss Estimation")

    d["sum_insured"] = st.number_input("Sum Insured (KES)", value=1000000.0)

    loss_percent = st.slider("Damage Severity (%)", 0, 100, 20)

    estimated_loss = d["sum_insured"] * loss_percent / 100

    st.success(f"Estimated Loss: KES {estimated_loss:,.2f}")

    if loss_percent > 70:
        st.error("⚠️ HIGH RISK")
    elif loss_percent > 40:
        st.warning("⚠️ MEDIUM RISK")
    else:
        st.success("✅ LOW RISK")

    d["estimated_loss"] = estimated_loss

# =========================
# MINIMAL OTHER SECTIONS
# =========================
elif section == "Security":
    st.header("Security")
    d["security"] = st.text_area("Security")

elif section == "Perils":
    st.header("Perils")
    d["perils"] = st.text_area("Perils")

# =========================
# SUBMIT
# =========================
elif section == "Submit":

    st.header("Generate Report")

    if st.button("📄 Generate Report"):

        c = canvas.Canvas("risk_report.pdf", pagesize=letter)
        y = 750

        def draw(title, value, y):
            if y < 100:
                c.showPage()
                y = 750

            c.setFont("Helvetica-Bold", 11)
            c.drawString(40, y, title)
            y -= 15

            c.setFont("Helvetica", 10)
            c.drawString(60, y, str(value))
            y -= 25

            return y

        for k, v in d.items():
            y = draw(k, v, y)

        c.save()

        with open("risk_report.pdf", "rb") as f:
            st.download_button("⬇️ Download Report", f, "risk_report.pdf")

# =========================
# NAVIGATION
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
