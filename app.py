import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Risk Survey System", layout="wide")
st.title("📊 Risk Survey System")

# =========================
# SECTIONS LIST
# =========================
sections = [
    "Client Info",
    "Contacts & Control",
    "Business Overview",
    "Assets",
    "Fire",
    "Security",
    "Employees",
    "Health & Safety",
    "Liability",
    "Engineering",
    "Financial Risk",
    "Environmental",
    "Cyber",
    "Loss History",
    "Business Continuity",
    "Submit"
]

# =========================
# SESSION STATE
# =========================
if "data" not in st.session_state:
    st.session_state.data = {}

if "step_index" not in st.session_state:
    st.session_state.step_index = 0

d = st.session_state.data
section = sections[st.session_state.step_index]

# =========================
# PROGRESS BAR
# =========================
st.progress((st.session_state.step_index + 1) / len(sections))
st.subheader(f"{section}")

# =========================
# SECTIONS CONTENT
# =========================
if section == "Client Info":
    d["insured"] = st.text_input("Insured Name")
    d["address"] = st.text_input("Physical Address")
    d["gps"] = st.text_input("GPS Coordinates")
    d["distance"] = st.text_input("Distance from Town")

elif section == "Contacts & Control":
    d["contacts"] = st.text_area("Contact Persons")
    d["documents"] = st.text_area("Document Control")
    d["communications"] = st.text_area("Communications")

elif section == "Business Overview":
    d["business"] = st.text_input("Nature of Business")
    d["background"] = st.text_area("Background")
    d["occupancy"] = st.text_input("Occupancy")
    d["process"] = st.text_area("Process")
    d["materials"] = st.text_area("Materials")

elif section == "Assets":
    d["buildings"] = st.text_area("Buildings")
    d["storage"] = st.text_area("Storage")
    d["goods_open"] = st.text_input("Goods in Open")
    d["exposure"] = st.text_area("Exposure")

elif section == "Fire":
    st.header("🔥 Fire Protection")
    d["fire"] = st.text_area("Fire Protection Details")

elif section == "Security":
    d["security"] = st.text_area("Security Measures")

elif section == "Employees":
    d["employees"] = st.text_area("Employees")

elif section == "Health & Safety":
    d["health"] = st.text_area("Health & Safety")

elif section == "Liability":
    d["liability"] = st.text_area("Liability")

elif section == "Engineering":
    d["engineering"] = st.text_area("Engineering")

elif section == "Financial Risk":
    d["financial"] = st.text_area("Financial Risk")

elif section == "Environmental":
    d["environment"] = st.text_area("Environmental Risk")

elif section == "Cyber":
    d["cyber"] = st.text_area("Cyber Risk")

elif section == "Loss History":
    d["loss"] = st.text_area("Loss History")

elif section == "Business Continuity":
    d["continuity"] = st.text_area("Continuity")

elif section == "Submit":

    st.header("Generate Report")

    if not d.get("insured"):
        st.warning("Please fill Client Info first")
        st.stop()

    score = len([v for v in d.values() if v])
    level = "LOW" if score < 10 else "MEDIUM" if score < 20 else "HIGH"

    st.subheader(f"Risk Score: {score}")
    st.subheader(f"Risk Level: {level}")

    if st.button("Generate PDF Report"):

        c = canvas.Canvas("risk_report.pdf", pagesize=letter)
        y = 750

        def check(y):
            if y < 60:
                c.showPage()
                return 750
            return y

        def draw(title, items, y):
            y = check(y)
            c.setFont("Helvetica-Bold", 14)
            c.drawString(40, y, title)
            y -= 20

            c.setFont("Helvetica", 10)

            for k, v in items.items():
                if v:
                    y = check(y)
                    c.drawString(40, y, f"{k}:")
                    y -= 15

                    for line in str(v).split("\n"):
                        y = check(y)
                        c.drawString(60, y, line)
                        y -= 14

            y -= 10
            return y

        # COVER PAGE
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(300, 700, "RISK ASSESSMENT REPORT")
        c.setFont("Helvetica", 12)
        c.drawCentredString(300, 650, f"Client: {d.get('insured')}")
        c.drawCentredString(300, 630, f"Location: {d.get('address')}")

        c.showPage()
        y = 750

        # REPORT STRUCTURE
        y = draw("Executive Summary", {"Summary": f"Risk Level: {level}, Score: {score}"}, y)
        y = draw("Contacts & Control", d, y)
        y = draw("Disclaimer & Signatures", {
            "Disclaimer": "This report is based on site observations and provided data.",
            "Surveyor Signature": "________________",
            "Client Signature": "________________"
        }, y)
        y = draw("Risk Score", {"Score": score, "Level": level}, y)
        y = draw("Gap Analysis", {"Findings": "Operational risks identified"}, y)
        y = draw("Recommendations", {"Actions": "Improve controls and monitoring"}, y)
        y = draw("Loss History", {"Loss": d.get("loss")}, y)

        y = draw("Detailed Sections", d, y)

        c.save()

        with open("risk_report.pdf", "rb") as f:
            st.download_button("📥 Download Report", f, "risk_report.pdf")

# =========================
# NAVIGATION BUTTONS
# =========================
col1, col2 = st.columns(2)

with col1:
    if st.session_state.step_index > 0:
        if st.button("⬅️ Previous"):
            st.session_state.step_index -= 1

with col2:
    if st.session_state.step_index < len(sections) - 1:
        if st.button("Next ➡️"):
            st.session_state.step_index += 1
