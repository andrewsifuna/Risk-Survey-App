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

        # HEADER
        def header(canvas, doc):
            canvas.drawImage("equity_logo.png", 40, 750, width=80, height=40)
            canvas.setFont("Helvetica", 9)
            canvas.drawString(40, 20, "Equity General Insurance (Kenya) Ltd")
            canvas.drawRightString(550, 20, f"Page {doc.page}")

        # COVER
        story.append(Paragraph("RISK SURVEY REPORT", title))
        story.append(Spacer(1,20))
        story.append(Paragraph(f"<b>Insured:</b> {d.get('insured','')}", normal))
        story.append(Paragraph(f"<b>Address:</b> {d.get('address','')}", normal))

        if d.get("client_photo"):
            with open("photo.jpg","wb") as f:
                f.write(d["client_photo"].getbuffer())
            story.append(Image("photo.jpg", width=400, height=250))

        story.append(PageBreak())

        # HELPERS
        def sec(t):
            story.append(Paragraph(t, h2))
            story.append(Spacer(1,8))

        def sub(t):
            story.append(Paragraph(t, h3))
            story.append(Spacer(1,5))

        def txt(v):
            story.append(Paragraph(v or "-", normal))
            story.append(Spacer(1,10))

        def tbl(data):
            t = Table(data)
            t.setStyle(TableStyle([
                ("GRID",(0,0),(-1,-1),1,colors.black),
                ("BACKGROUND",(0,0),(-1,0),colors.grey),
                ("TEXTCOLOR",(0,0),(-1,0),colors.white)
            ]))
            story.append(t)
            story.append(Spacer(1,10))

        # STRUCTURED REPORT
        sec("1.0 Contacts & Control Sheet"); txt(d.get("contacts"))
        sec("2.0 Disclaimer"); txt("Survey-based assessment.")
        sec("3.0 Executive Summary"); txt("Overall moderate risk.")

        sec("4.0 Risk Improvements"); txt("Improve fire + safety")

        sec("5.0 Insurance Gap")
        tbl([["Area","Status"],["Fire","OK"],["BI","Review"]])

        sec("6.0 Loss Estimation")
        tbl([["Metric","Value"],["Sum",str(d.get("sum_insured"))],["Loss",str(d.get("estimated_loss"))]])

        sec("7.0 Risk Score")
        tbl([["Factor","Score"],["Fire","Medium"],["Security","Low"]])

        sec("8.0 Background")
        sub("8.1 Building"); txt(d.get("building_age"))
        sub("8.2 GPS"); txt(d.get("gps"))
        sub("8.3 Employees"); txt(d.get("employees"))

        sec("9.0 Construction"); txt(d.get("building_age"))
        sec("10.0 Process"); txt(d.get("process"))
        sec("11.0 Electrical"); txt(d.get("electricity"))
        sec("12.0 Human"); txt(d.get("employees"))
        sec("13.0 Fire"); txt(d.get("fire"))
        sec("14.0 Security"); txt(d.get("security"))
        sec("15.0 Utilities"); txt(d.get("water"))
        sec("16.0 Machinery"); txt(d.get("computers"))
        sec("17.0 OSH"); txt(d.get("safety"))
        sec("18.0 Storage"); txt(d.get("storage"))
        sec("19.0 NatCat"); txt(d.get("perils"))
        sec("20.0 Cyber"); txt("Basic controls")
        sec("21.0 Supply Chain"); txt("Moderate")
        sec("22.0 Environmental"); txt(d.get("waste"))
        sec("23.0 BI"); txt(d.get("interruption"))
        sec("24.0 Governance"); txt("Structured")

        doc.build(story, onFirstPage=header, onLaterPages=header)

        with open("professional_report.pdf","rb") as f:
            st.download_button("⬇️ Download Report", f, "professional_report.pdf")

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
