import streamlit as st
import requests
import streamlit.components.v1 as components
from geopy.distance import geodesic

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Equity Risk Survey System", layout="wide")

# =========================
# STYLE
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
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION
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
# NAV
# =========================
def next_step():
    if st.session_state.step < len(sections) - 1:
        st.session_state.step += 1

def prev_step():
    if st.session_state.step > 0:
        st.session_state.step -= 1

section = sections[st.session_state.step]

# =========================
# HEADER
# =========================
st.progress(st.session_state.step / (len(sections)-1))
st.markdown("<h1>🏦 Equity Risk Survey System</h1>", unsafe_allow_html=True)

# =========================
# WELCOME
# =========================
if section == "Welcome":
    st.image("equity_logo.png", width=300)
    st.markdown("### Click Next to begin")

# =========================
# CLIENT INFO
# =========================
elif section == "Client Info":

    d["insured"] = st.text_input("Insured Name", d.get("insured",""))
    d["address"] = st.text_input("Address", d.get("address",""))

    # GPS
    components.html("""
    <script>
    navigator.geolocation.getCurrentPosition(function(pos){
        const coords = pos.coords.latitude + "," + pos.coords.longitude;
        const inputs = window.parent.document.querySelectorAll('input');
        if(inputs.length>2){
            inputs[2].value = coords;
            inputs[2].dispatchEvent(new Event('input',{bubbles:true}));
        }
    });
    </script>
    """, height=0)

    if st.button("📍 Use Approx Location"):
        res = requests.get("https://ipinfo.io/json").json()
        d["gps"] = res.get("loc")

    d["gps"] = st.text_input("GPS", d.get("gps",""))

    if d.get("gps") and "," in d["gps"]:
        lat, lon = map(float, d["gps"].split(","))
        dist = geodesic((lat,lon),(-1.286389,36.817223)).km
        d["distance"] = f"{dist:.2f} km"
        st.success(f"Distance: {dist:.2f} km")

    d["distance"] = st.text_input("Distance", d.get("distance",""))

    d["client_photo"] = st.camera_input("Capture Front View")

# =========================
# SIMPLE SECTIONS
# =========================
elif section == "Contacts & Control":
    d["contacts"] = st.text_area("Contacts")

elif section == "Business Overview":
    d["business"] = st.text_input("Business")
    d["background"] = st.text_area("Background")

elif section == "Site Buildings":
    d["building_age"] = st.text_input("Building Details")

elif section == "Utilities":
    d["electricity"] = st.text_area("Electricity")
    d["water"] = st.text_area("Water")

elif section == "Employees":
    d["employees"] = st.text_area("Employees")

elif section == "Health & Safety":
    d["safety"] = st.text_area("Safety")

elif section == "Fire Protection":
    d["fire"] = st.text_area("Fire Systems")

elif section == "Security":
    d["security"] = st.text_area("Security")

elif section == "Storage":
    d["storage"] = st.text_area("Storage")

elif section == "Computers":
    d["computers"] = st.text_area("IT")

elif section == "Waste Disposal":
    d["waste"] = st.text_area("Waste")

elif section == "Perils":
    d["perils"] = st.text_area("Perils")

elif section == "Process":
    d["process"] = st.text_area("Process")

elif section == "Interruption Analysis":
    d["interruption"] = st.text_area("Business Interruption")

# =========================
# LOSS
# =========================
elif section == "Risk Appraisal":
    d["sum_insured"] = st.number_input("Sum Insured", value=1000000.0)
    d["estimated_loss"] = st.number_input("Estimated Loss", value=200000.0)

# =========================
# SUBMIT (FINAL PROFESSIONAL)
# =========================
elif section == "Submit":

    st.header("Generate Professional Report")

    if st.button("📄 Generate Professional PDF"):

        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet

        doc = SimpleDocTemplate("professional_report.pdf")
        styles = getSampleStyleSheet()

        story = []

        title = styles["Heading1"]
        h2 = styles["Heading2"]
        h3 = styles["Heading3"]
        normal = styles["Normal"]

        # =========================
        # HEADER / FOOTER
        # =========================
        def header(canvas, doc):
            canvas.drawImage("equity_logo.png", 40, 750, width=80, height=40)
            canvas.setFont("Helvetica", 9)
            canvas.drawString(40, 20, "Equity General Insurance (Kenya) Ltd")
            canvas.drawRightString(550, 20, f"Page {doc.page}")

        # =========================
        # COVER PAGE
        # =========================
        story.append(Paragraph("RISK SURVEY REPORT", title))
        story.append(Spacer(1, 20))

        story.append(Paragraph(f"<b>Insured:</b> {d.get('insured','')}", normal))
        story.append(Paragraph(f"<b>Address:</b> {d.get('address','')}", normal))
        story.append(Spacer(1, 20))

        if d.get("client_photo"):
            with open("photo.jpg", "wb") as f:
                f.write(d["client_photo"].getbuffer())
            story.append(Image("photo.jpg", width=400, height=250))

        story.append(PageBreak())

        # =========================
        # HELPERS
        # =========================
        def section(title):
            story.append(Paragraph(title, h2))
            story.append(Spacer(1, 8))

        def subsection(title):
            story.append(Paragraph(title, h3))
            story.append(Spacer(1, 5))

        def text_block(text):
            story.append(Paragraph(text or "-", normal))
            story.append(Spacer(1, 10))

        def table(data):
            t = Table(data)
            t.setStyle(TableStyle([
                ("GRID", (0,0), (-1,-1), 1, colors.black),
                ("BACKGROUND", (0,0), (-1,0), colors.grey),
                ("TEXTCOLOR",(0,0),(-1,0),colors.white)
            ]))
            story.append(t)
            story.append(Spacer(1, 15))

        # =========================
        # PROFESSIONAL STRUCTURE
        # =========================
        section("1.0 Contacts & Control Sheet")
        text_block(d.get("contacts"))

        section("2.0 Disclaimer & Risk Survey Sign-Off")
        text_block("This report reflects observed conditions at time of survey.")

        section("3.0 Executive Summary")
        text_block("Overall risk profile based on survey inputs.")

        section("4.0 Risk Improvement Recommendations (RIRs)")
        text_block("• Improve fire systems\n• Enhance safety controls")

        section("5.0 Insurance Gap Analysis")
        table([
            ["Area", "Status"],
            ["Fire Cover", "Adequate"],
            ["Business Interruption", "Review Needed"]
        ])

        section("6.0 Loss Estimation (PML/EML)")
        table([
            ["Metric", "Value"],
            ["Sum Insured", str(d.get("sum_insured",""))],
            ["Estimated Loss", str(d.get("estimated_loss",""))]
        ])

        section("7.0 Overall Risk Scoring Model")
        table([
            ["Factor", "Score"],
            ["Fire Risk", "Medium"],
            ["Security", "Low"]
        ])

        section("8.0 Background Information")

        subsection("8.1 History & Age")
        text_block(d.get("building_age"))

        subsection("8.2 GPS Location & Map")
        text_block(d.get("gps"))

        subsection("8.3 Employees")
        text_block(d.get("employees"))

        section("9.0 Construction & Structural Integrity")
        text_block(d.get("building_age"))

        section("10.0 Occupancy/Processes & Operational Controls")
        text_block(d.get("process"))

        section("11.0 Electrical Systems Safety")
        text_block(d.get("electricity"))

        section("12.0 Human Factors")
        text_block(d.get("employees"))

        section("13.0 Fire, Explosion, and Protection Systems")
        text_block(d.get("fire"))

        section("14.0 Security Systems")
        text_block(d.get("security"))

        section("15.0 Utilities & Critical Services")
        text_block(d.get("water"))

        section("16.0 Machinery & Engineering Systems")
        text_block(d.get("computers"))

        section("17.0 Occupational Safety & Health (OSH)")
        text_block(d.get("safety"))

        section("18.0 Storage & Material Handling")
        text_block(d.get("storage"))

        section("19.0 Natural Catastrophes (NatCat)")
        text_block(d.get("perils"))

        section("20.0 Cyber & Information Security")
        text_block("Basic controls observed")

        section("21.0 Supply Chain & Logistics")
        text_block("Moderate dependency")

        section("22.0 Environmental Management")
        text_block(d.get("waste"))

        section("23.0 Business Continuity (BI)")
        text_block(d.get("interruption"))

        section("24.0 Management Systems & Risk Governance")
        text_block("Management controls in place")

        # =========================
        # BUILD
        # =========================
        doc.build(story, onFirstPage=header, onLaterPages=header)

        with open("professional_report.pdf", "rb") as f:
            st.download_button("⬇️ Download Professional Report", f, "professional_report.pdf")

# =========================
# NAV BUTTONS
# =========================
c1,c2,c3 = st.columns(3)

with c1:
    if st.session_state.step>0:
        st.button("⬅️ Previous", on_click=prev_step)

with c3:
    if st.session_state.step < len(sections)-1:
        st.button("Next ➡️", on_click=next_step)
