import streamlit as st
import time
import math
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Risk Survey System", layout="wide")

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
# UI
# =========================
progress = st.session_state.step / (len(sections) - 1)
st.progress(progress)
st.title("📊 Risk Survey System")

# =========================
# WELCOME
# =========================
if section == "Welcome":
    placeholder = st.empty()
    for i in range(40):
        y_anim = math.sin(i / 5) * 10
        placeholder.markdown(
            f"<h1 style='text-align:center; transform: translateY({y_anim}px);'>Welcome to EGIK Risk Survey</h1>",
            unsafe_allow_html=True
        )
        time.sleep(0.05)

# =========================
# CLIENT
# =========================
elif section == "Client Info":
    st.header("Client Information")
    d["insured"] = st.text_input("Insured Name", d.get("insured", ""))
    d["address"] = st.text_input("Physical Address", d.get("address", ""))
    d["gps"] = st.text_input("GPS Coordinates", d.get("gps", ""))
    d["distance"] = st.text_input("Distance from Town", d.get("distance", ""))
    d["client_photo"] = st.camera_input("Capture Front View")

elif section == "Contacts & Control":
    st.header("Contacts & Control")
    d["contacts"] = st.text_area("Contacts", d.get("contacts", ""))

elif section == "Business Overview":
    st.header("Business Overview")
    d["business"] = st.text_input("Nature of Business", d.get("business", ""))
    d["background"] = st.text_area("Background", d.get("background", ""))

# =========================
# OTHER SECTIONS (UNCHANGED)
# =========================
elif section == "Site Buildings":
    st.header("Site Buildings")
    d["building_age"] = st.text_input("Age, Structure & Roofing")
    d["floors"] = st.text_input("Floors")
    d["voids"] = st.text_input("Voids")
    d["site_plan"] = st.text_area("Site Plan")

elif section == "Situation":
    st.header("Situation")
    d["physical_address"] = st.text_input("Physical Address", d.get("address", ""))
    d["distance_town"] = st.text_input("Distance From Town", d.get("distance", ""))

elif section == "Exposure":
    st.header("Exposure")
    d["exposure_internal"] = st.text_area("Internal")
    d["exposure_external"] = st.text_area("External")

elif section == "Storage":
    st.header("Storage")
    d["storage"] = st.text_area("Storage Details")
    d["water_damage"] = st.text_area("Water Damage")

elif section == "Utilities":
    st.header("Utilities")
    d["electricity"] = st.text_area("Electricity")
    d["water"] = st.text_area("Water")
    d["heating"] = st.text_area("Heating")

elif section == "Employees":
    st.header("Employees")
    d["employees"] = st.text_area("Employees Info")

elif section == "Health & Safety":
    st.header("Health & Safety")
    d["safety"] = st.text_area("Safety")

elif section == "Fire Protection":
    st.header("Fire Protection")
    d["fire"] = st.text_area("Fire Protection")
    d["fire_photo1"] = st.camera_input("Fire Photo 1", key="f1")

elif section == "Fire Services":
    st.header("Fire Services")
    d["fire_services"] = st.text_area("Fire Services")

elif section == "Security":
    st.header("Security")
    d["security"] = st.text_area("Security")

elif section == "Cash/Stocks":
    st.header("Cash / Stocks")
    d["cash"] = st.text_area("Cash Handling")

elif section == "Computers":
    st.header("Computers")
    d["computers"] = st.text_area("IT Systems")

elif section == "Waste Disposal":
    st.header("Waste Disposal")
    d["waste"] = st.text_area("Waste")

elif section == "Perils":
    st.header("Perils")
    d["perils"] = st.text_area("Perils")

elif section == "Risk Appraisal":
    st.header("Risk Appraisal")
    d["risk"] = st.text_area("Risk")

elif section == "Process":
    st.header("Process")
    d["process"] = st.text_area("Process")

elif section == "Hazardous Substances":
    st.header("Hazardous")
    d["hazard"] = st.text_area("Hazardous")

elif section == "Unions":
    st.header("Unions")
    d["unions"] = st.text_area("Unions")

elif section == "Losses Report":
    st.header("Losses")
    d["losses"] = st.text_area("Losses")

elif section == "Interruption Analysis":
    st.header("Interruption")
    d["interruption"] = st.text_area("Interruption")

# =========================
# SUBMIT (FIXED)
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

            c.drawString(40, y, title)
            y -= 15

            c.drawString(60, y, str(value))
            y -= 25

            return y

        for k, v in d.items():
            y = draw(k, v, y)

        c.save()

        with open("risk_report.pdf", "rb") as f:
            st.download_button("Download Report", f, "risk_report.pdf")

# =========================
# NAV
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    if st.session_state.step > 0:
        st.button("⬅️ Previous", on_click=prev_step)

with col2:
    st.button("💾 Save for Later", on_click=save_progress)

with col3:
    if st.session_state.step < len(sections) - 1:
        st.button("➡️ Next", on_click=next_step)
