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
# SECTIONS ORDER
# =========================
sections = [
    "Welcome",
    "Client Info",
    "Contacts & Control",
    "Business Overview",
    "Assets",
    "Fire",
    "Engineering",
    "Submit"
]

# =========================
# NAVIGATION FUNCTIONS
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
# PROGRESS BAR
# =========================
progress = st.session_state.step / (len(sections) - 1)
st.progress(progress)

st.title("📊 Risk Survey System")

# =========================
# 1. WELCOME PAGE
# =========================
if section == "Welcome":

    placeholder = st.empty()

    for i in range(40):
        y_anim = math.sin(i / 5) * 10
        placeholder.markdown(
            f"<h1 style='text-align:center; transform: translateY({y_anim}px);'>"
            f"Welcome to EGIK Risk Survey</h1>",
            unsafe_allow_html=True
        )
        time.sleep(0.05)

    st.markdown("### Click Next to begin")

# =========================
# CLIENT INFO
# =========================
elif section == "Client Info":

    st.header("Client Information")

    d["insured"] = st.text_input("Insured Name", d.get("insured", ""))
    d["address"] = st.text_input("Physical Address", d.get("address", ""))
    d["gps"] = st.text_input("GPS Coordinates", d.get("gps", ""))
    d["distance"] = st.text_input("Distance from Town", d.get("distance", ""))

    st.subheader("📸 Take Front Photo")
    d["client_photo"] = st.camera_input("Capture Front View")

# =========================
# CONTACTS
# =========================
elif section == "Contacts & Control":

    st.header("Contacts & Control")

    d["contacts"] = st.text_area("Contacts", d.get("contacts", ""))
    d["documents"] = st.text_area("Documents", d.get("documents", ""))
    d["communications"] = st.text_area("Communications", d.get("communications", ""))

# =========================
# BUSINESS
# =========================
elif section == "Business Overview":

    st.header("Business Overview")

    d["business"] = st.text_input("Nature of Business", d.get("business", ""))
    d["background"] = st.text_area("Background", d.get("background", ""))

# =========================
# ASSETS
# =========================
elif section == "Assets":

    st.header("Assets")

    d["buildings"] = st.text_area("Buildings", d.get("buildings", ""))

# =========================
# FIRE
# =========================
elif section == "Fire":

    st.header("🔥 Fire Protection")

    d["fire"] = st.text_area("Fire Protection", d.get("fire", ""))

    st.subheader("📸 Fire Photos")
    d["fire_photo1"] = st.camera_input("Capture Fire Equipment", key="fire1")
    d["fire_photo2"] = st.camera_input("Capture Fire Area", key="fire2")

# =========================
# ENGINEERING
# =========================
elif section == "Engineering":

    st.header("Engineering")

    d["engineering"] = st.text_area("Engineering", d.get("engineering", ""))

    st.subheader("📸 Engineering Photos")
    d["eng_photo1"] = st.camera_input("Capture Machinery", key="eng1")
    d["eng_photo2"] = st.camera_input("Capture Systems", key="eng2")

# =========================
# SUBMIT PAGE
# =========================
elif section == "Submit":

    st.header("Generate Report")

    # =========================
    # REQUIRED FIELDS CHECK
    # =========================
    required_fields = {
        "Client Info - Insured Name": d.get("insured"),
        "Client Info - Address": d.get("address"),
        "Business Overview": d.get("business"),
        "Fire Protection": d.get("fire"),
        "Engineering": d.get("engineering"),
    }

    missing_fields = [k for k, v in required_fields.items() if not v]

    # =========================
    # SHOW STATUS
    # =========================
    if missing_fields:
        st.warning("⚠️ Please complete all required sections before generating report")

        with st.expander("See missing fields"):
            for field in missing_fields:
                st.write(f"❌ {field}")

    else:
        st.success("✅ All required fields completed")

    # =========================
    # GENERATE BUTTON
    # =========================
    if st.button("📄 Generate Report"):

        # 🚫 BLOCK IF INCOMPLETE
        if missing_fields:
            st.error("Cannot generate report. Please complete all required fields.")
            st.stop()

        # =========================
        # RISK SCORE
        # =========================
        score = len([v for v in d.values() if v])
        level = "LOW" if score < 5 else "MEDIUM" if score < 10 else "HIGH"

        st.subheader(f"Risk Score: {score}")
        st.subheader(f"Risk Level: {level}")

        # =========================
        # PDF GENERATION
        # =========================
        c = canvas.Canvas("risk_report.pdf", pagesize=letter)
        y = 750

        def draw(title, content, y):
            c.setFont("Helvetica-Bold", 14)
            c.drawString(40, y, title)
            y -= 20

            c.setFont("Helvetica", 10)
            for k, v in content.items():
                if v:
                    c.drawString(40, y, f"{k}: {v}")
                    y -= 15

            y -= 10
            return y

        # Cover Page
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(300, 700, "EGIK RISK REPORT")
        c.showPage()

        y = draw("Executive Summary", {"Risk Level": level, "Score": score}, y)
        y = draw("Client Info", d, y)
        y = draw("Fire", {"Fire": d.get("fire")}, y)
        y = draw("Engineering", {"Engineering": d.get("engineering")}, y)

        c.save()

        with open("risk_report.pdf", "rb") as f:
            st.download_button("📥 Download Report", f, "risk_report.pdf")

# =========================
# NAVIGATION BUTTONS
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
