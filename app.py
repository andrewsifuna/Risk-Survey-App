import streamlit as st
import time
import math
import requests
import streamlit.components.v1 as components
from datetime import datetime
from geopy.distance import geodesic
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import TabStop


class MyDocTemplate(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            text = flowable.getPlainText()

            if text.startswith(tuple(f"{i}." for i in range(1, 14))):
                self.notify('TOCEntry', (0, text, self.page))


def safe_float(val):
    try:
        return float(str(val).replace(",", ""))
    except:
        return 0.0


def clean_text(value):
    if value is None:
        return ""

    if isinstance(value, list):
        return ", ".join([str(v) for v in value])

    if isinstance(value, dict):
        return str(value)

    if not isinstance(value, str):
        value = str(value)

    value = value.replace("\xa0", " ")
    value = value.replace("&", "&amp;")
    value = value.replace("<", "&lt;")
    value = value.replace(">", "&gt;")

    return value.strip()


# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Equity Risk Survey System", layout="wide")

# =========================
# STYLE
# =========================
st.markdown(
    """
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
""",
    unsafe_allow_html=True,
)

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
    "Welcome",
    "Client Info",
    "Contacts & Control",
    "Business Overview",
    "Site Buildings",
    "Situation",
    "Exposure",
    "Storage",
    "Utilities",
    "Employees",
    "Machinery & Engineering Systems",
    "Health & Safety",
    "Fire Protection",
    "Fire Services",
    "Security",
    "Cash/Stocks",
    "Computers",
    "Waste Disposal",
    "Perils",
    "Risk Appraisal",
    "Process",
    "Hazardous Substances",
    "Unions",
    "Losses Report",
    "Interruption Analysis",
    "Submit",
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
st.progress(st.session_state.step / (len(sections) - 1))
st.markdown("<h1>🏦 Equity Risk Survey System</h1>", unsafe_allow_html=True)

# =========================
# WELCOME
# =========================
if section == "Welcome":

    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.image("equity_logo.png", width=200)

        # Animated title
        placeholder = st.empty()
        for i in range(20):
            y_anim = math.sin(i / 3) * 8
            placeholder.markdown(
                f"""
                <h2 style='text-align:center;
                           color:#008751;
                           transform: translateY({y_anim}px);'>
                    Welcome to Equity Risk Survey
                </h2>
                """,
                unsafe_allow_html=True,
            )
            time.sleep(0.02)

        st.markdown(
            "<p style='text-align:center;'>Select an option to continue</p>",
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # =========================
        # BUTTONS (CENTERED)
        # =========================
        b1, b2, b3 = st.columns(3)

        with b1:
            if st.button("▶️ Begin Survey"):
                next_step()

        with b2:
            if st.button("📄 View Reports"):
                st.info("Report viewer coming next...")

        with b3:
            if st.button("🔄 Resume Survey"):
                st.info("Resume functionality coming next...")

# =========================
# CLIENT INFO
# =========================
elif section == "Client Info":

    d["insured"] = st.text_input("Insured Name", d.get("insured", ""))
    d["address"] = st.text_input("Address", d.get("address", ""))

    # GPS
    components.html(
        """
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
    """,
        height=0,
    )

    if st.button("📍 Use Approx Location"):
        res = requests.get("https://ipinfo.io/json").json()
        d["gps"] = res.get("loc")

    d["gps"] = st.text_input("GPS", d.get("gps", ""))

    if d.get("gps") and "," in d["gps"]:
        lat, lon = map(float, d["gps"].split(","))
        dist = geodesic((lat, lon), (-1.286389, 36.817223)).km
        d["distance"] = f"{dist:.2f} km"
        st.success(f"Distance: {dist:.2f} km")

    d["distance"] = st.text_input("Distance", d.get("distance", ""))

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

elif section == "Situation":
    st.header("Situation")

    d["address"] = st.text_input("Physical Address", d.get("address", ""))

    d["distance_town"] = st.text_input("Distance From Town", d.get("distance_town", ""))
elif section == "Exposure":
    st.header("Exposure")

    d["exposure_internal"] = st.text_area(
        "Internal Exposure (e.g. fire load, machinery, processes)",
        d.get("exposure_internal", ""),
    )

    d["exposure_external"] = st.text_area(
        "External Exposure (e.g. сосед buildings, roads, hazards)",
        d.get("exposure_external", ""),
    )
elif section == "Utilities":
    st.header("Utilities & Services Risk")

    # =========================
    # ELECTRICITY
    # =========================
    d["machinery_power_source"] = st.selectbox(
        "Main Power Source",
        ["Grid", "Generator", "Solar", "Mixed"],
        index=["Grid", "Generator", "Solar", "Mixed"].index(
            d.get("machinery_power_source", "Grid")
        ),
    )

    d["power_reliability"] = st.selectbox(
        "Power Reliability",
        ["Stable", "Occasional Outages", "Frequent Outages"],
        index=["Stable", "Occasional Outages", "Frequent Outages"].index(
            d.get("power_reliability", "Stable")
        ),
    )

    d["backup_power"] = st.selectbox(
        "Backup Power Available?",
        ["Yes", "No"],
        index=["Yes", "No"].index(d.get("backup_power", "No")),
    )

    d["generator_details"] = st.text_area(
        "Generator / Backup Details (capacity, fuel type, maintenance)",
        d.get("generator_details", ""),
    )

    # =========================
    # ELECTRICAL RISK
    # =========================
    d["wiring_condition"] = st.selectbox(
        "Electrical Wiring Condition",
        ["New", "Good", "Old", "Poor"],
        index=["New", "Good", "Old", "Poor"].index(d.get("wiring_condition", "Good")),
    )

    d["maintenance"] = st.selectbox(
        "Electrical Maintenance Frequency",
        ["Regular", "Occasional", "None"],
        index=["Regular", "Occasional", "None"].index(
            d.get("maintenance", "Occasional")
        ),
    )

    # =========================
    # WATER
    # =========================
    d["water_source"] = st.selectbox(
        "Water Source",
        ["Municipal", "Borehole", "Well", "Mixed"],
        index=["Municipal", "Borehole", "Well", "Mixed"].index(
            d.get("water_source", "Municipal")
        ),
    )

    d["water_reliability"] = st.selectbox(
        "Water Supply Reliability",
        ["Stable", "Occasional Interruptions", "Frequent Interruptions"],
        index=["Stable", "Occasional Interruptions", "Frequent Interruptions"].index(
            d.get("water_reliability", "Stable")
        ),
    )

    # =========================
    # FIRE SUPPORT
    # =========================
    d["fire_water_availability"] = st.selectbox(
        "Adequate Water for Firefighting?",
        ["Yes", "No"],
        index=["Yes", "No"].index(d.get("fire_water_availability", "Yes")),
    )

    # =========================
    # GAS / FUEL
    # =========================
    d["fuel_storage"] = st.text_area(
        "Fuel / Gas Storage (diesel, LPG, etc.)", d.get("fuel_storage", "")
    )

    # =========================
    # SMART RISK ALERT
    # =========================
    if (
        d.get("power_reliability") == "Frequent Outages"
        and d.get("backup_power") == "No"
    ):
        st.error("⚠️ High operational risk: No backup power with frequent outages")

    if d.get("wiring_condition") in ["Old", "Poor"]:
        st.warning("⚠️ Electrical fire risk: Wiring condition is not adequate")

elif section == "Employees":
    st.header("Employees & Workforce Risk")

    d["num_employees"] = st.number_input(
        "Number of Employees", min_value=0, value=int(d.get("num_employees", 0))
    )

    d["employee_type"] = st.selectbox(
        "Type of Workforce",
        ["Skilled", "Semi-skilled", "Unskilled", "Mixed"],
        index=["Skilled", "Semi-skilled", "Unskilled", "Mixed"].index(
            d.get("employee_type", "Mixed")
        ),
    )

    d["shift_work"] = st.selectbox(
        "Shift Work?",
        ["No", "Day Only", "Night Shifts", "24/7 Operations"],
        index=["No", "Day Only", "Night Shifts", "24/7 Operations"].index(
            d.get("shift_work", "No")
        ),
    )

    d["training"] = st.selectbox(
        "Employee Training Level",
        ["None", "Basic", "Regular", "Advanced"],
        index=["None", "Basic", "Regular", "Advanced"].index(
            d.get("training", "Basic")
        ),
    )

    d["turnover"] = st.selectbox(
        "Staff Turnover Rate",
        ["Low", "Moderate", "High"],
        index=["Low", "Moderate", "High"].index(d.get("turnover", "Moderate")),
    )

    d["fidelity_risk"] = st.selectbox(
        "Fraud / Fidelity Risk Exposure",
        ["Low", "Medium", "High"],
        index=["Low", "Medium", "High"].index(d.get("fidelity_risk", "Low")),
    )

    d["controls"] = st.text_area(
        "Controls (background checks, supervision, access control)",
        d.get("controls", ""),
    )
elif section == "Machinery & Engineering Systems":
    st.header("Machinery & Engineering Systems")

    # =========================
    # MACHINERY INVENTORY
    # =========================
    d["machinery_types"] = st.text_area(
        "Types of Machinery (e.g. generators, boilers, compressors, production lines)",
        d.get("machinery_types", ""),
    )

    d["machinery_value"] = st.number_input(
        "Total Machinery Value (KES)", value=float(d.get("machinery_value", 0))
    )

    d["machinery_age"] = st.number_input(
        "Average Age of Machinery (years)", value=float(d.get("machinery_age", 0))
    )

    d["machinery_condition"] = st.selectbox(
        "Condition of Machinery",
        ["New", "Good", "Fair", "Poor"],
        index=["New", "Good", "Fair", "Poor"].index(
            d.get("machinery_condition", "Good")
        ),
    )

    # =========================
    # MAINTENANCE SYSTEM
    # =========================
    d["maintenance_program"] = st.selectbox(
        "Maintenance Program",
        ["None", "Reactive", "Preventive", "Predictive"],
        index=["None", "Reactive", "Preventive", "Predictive"].index(
            d.get("maintenance_program", "Preventive")
        ),
    )

    d["maintenance_frequency"] = st.selectbox(
        "Maintenance Frequency",
        ["Irregular", "Quarterly", "Monthly", "Weekly"],
        index=["Irregular", "Quarterly", "Monthly", "Weekly"].index(
            d.get("maintenance_frequency", "Monthly")
        ),
    )

    d["last_service"] = st.text_input("Last Service Date", d.get("last_service", ""))

    # =========================
    # BREAKDOWN HISTORY
    # =========================
    d["breakdown_history"] = st.text_area(
        "Breakdown History (last 3 years)", d.get("breakdown_history", "")
    )

    d["major_failures"] = st.selectbox(
        "Any Major Failures in Last 3 Years?",
        ["No", "Yes"],
        index=["No", "Yes"].index(d.get("major_failures", "No")),
    )

    # =========================
    # CRITICAL EQUIPMENT
    # =========================
    d["critical_machines"] = st.text_area(
        "Critical Machines (whose failure stops operations)",
        d.get("critical_machines", ""),
    )

    d["redundancy"] = st.selectbox(
        "Backup / Redundancy Available?",
        ["Yes", "No"],
        index=["Yes", "No"].index(d.get("redundancy", "No")),
    )

    # =========================
    # POWER & ELECTRICAL
    # =========================
    d["power_source"] = st.selectbox(
        "Main Power Source",
        ["Grid", "Generator", "Solar", "Mixed"],
        index=["Grid", "Generator", "Solar", "Mixed"].index(
            d.get("power_source", "Grid")
        ),
    )

    d["power_stability"] = st.selectbox(
        "Power Stability",
        ["Stable", "Moderate Interruptions", "Frequent Outages"],
        index=["Stable", "Moderate Interruptions", "Frequent Outages"].index(
            d.get("power_stability", "Moderate Interruptions")
        ),
    )

    d["surge_protection"] = st.selectbox(
        "Surge Protection Installed?",
        ["Yes", "No"],
        index=["Yes", "No"].index(d.get("surge_protection", "Yes")),
    )

    # =========================
    # BOILERS / PRESSURE PLANT
    # =========================
    d["pressure_equipment"] = st.selectbox(
        "Boilers / Pressure Equipment Present?",
        ["No", "Yes"],
        index=["No", "Yes"].index(d.get("pressure_equipment", "No")),
    )

    if d["pressure_equipment"] == "Yes":
        d["inspection_status"] = st.selectbox(
            "Inspection Status",
            ["Up to Date", "Overdue"],
            index=["Up to Date", "Overdue"].index(
                d.get("inspection_status", "Up to Date")
            ),
        )

    # =========================
    # OPERATOR SKILL LEVEL
    # =========================

    def safe_index(options, value, default=0):
        return options.index(value) if value in options else default

    options = ["Low", "Moderate", "High"]

    d["process_operator_skill"] = st.selectbox(
        "Operator Skill Level",
        options,
        index=safe_index(options, d.get("process_operator_skill", "Moderate")),
    )

    # =========================
    # AUTOMATION LEVEL
    # =========================
    d["automation_level"] = st.selectbox(
        "Automation Level",
        ["Manual", "Semi-automated", "Fully automated"],
        index=["Manual", "Semi-automated", "Fully automated"].index(
            d.get("automation_level", "Semi-automated")
        ),
    )

    # =========================
    # RISK FLAGS
    # =========================
    if d["maintenance_program"] == "None":
        st.error("🚨 No maintenance program → HIGH breakdown risk")

    if d["machinery_condition"] == "Poor":
        st.error("🚨 Poor machinery condition → HIGH risk")

    if d["redundancy"] == "No":
        st.warning("⚠️ No backup machinery → Business interruption risk")

    if d["power_stability"] == "Frequent Outages":
        st.warning("⚠️ Power instability → Equipment damage risk")

    if d.get("inspection_status") == "Overdue":
        st.error("🚨 Pressure equipment inspection overdue → CRITICAL risk")


elif section == "Health & Safety":
    st.header("Health & Safety Management")

    # =========================
    # POLICY & COMPLIANCE
    # =========================
    d["hs_policy"] = st.selectbox(
        "Health & Safety Policy in Place?",
        ["Yes", "No"],
        index=["Yes", "No"].index(d.get("hs_policy", "No")),
    )

    d["regulatory_compliance"] = st.selectbox(
        "Compliance with OSHA / Local Regulations",
        ["Compliant", "Partially Compliant", "Non-Compliant"],
        index=["Compliant", "Partially Compliant", "Non-Compliant"].index(
            d.get("regulatory_compliance", "Compliant")
        ),
    )

    # =========================
    # TRAINING & AWARENESS
    # =========================
    d["safety_training"] = st.selectbox(
        "Safety Training Level",
        ["None", "Basic", "Regular", "Advanced"],
        index=["None", "Basic", "Regular", "Advanced"].index(
            d.get("safety_training", "Basic")
        ),
    )

    d["induction_training"] = st.selectbox(
        "New Employee Safety Induction?",
        ["Yes", "No"],
        index=["Yes", "No"].index(d.get("induction_training", "No")),
    )

    # =========================
    # INCIDENT HISTORY
    # =========================
    d["incident_history"] = st.selectbox(
        "Accident / Incident History",
        ["None", "Minor Incidents", "Major Incidents"],
        index=["None", "Minor Incidents", "Major Incidents"].index(
            d.get("incident_history", "None")
        ),
    )

    d["incident_details"] = st.text_area(
        "Details of Past Incidents", d.get("incident_details", "")
    )

    # =========================
    # PPE
    # =========================
    d["ppe_provided"] = st.selectbox(
        "PPE Provided to Employees?",
        ["Yes", "No"],
        index=["Yes", "No"].index(d.get("ppe_provided", "Yes")),
    )

    d["ppe_usage"] = st.selectbox(
        "PPE Usage Compliance",
        ["High", "Moderate", "Low"],
        index=["High", "Moderate", "Low"].index(d.get("ppe_usage", "High")),
    )

    # =========================
    # SAFETY SYSTEMS
    # =========================
    d["first_aid"] = st.selectbox(
        "First Aid Facilities Available?",
        ["Yes", "No"],
        index=["Yes", "No"].index(d.get("first_aid", "Yes")),
    )

    d["emergency_plan"] = st.selectbox(
        "Emergency Response Plan in Place?",
        ["Yes", "No"],
        index=["Yes", "No"].index(d.get("emergency_plan", "No")),
    )

    d["signage"] = st.selectbox(
        "Safety Signage Available?",
        ["Adequate", "Limited", "None"],
        index=["Adequate", "Limited", "None"].index(d.get("signage", "Adequate")),
    )

    # =========================
    # HOUSEKEEPING
    # =========================
    d["housekeeping"] = st.selectbox(
        "General Housekeeping Standard",
        ["Good", "Average", "Poor"],
        index=["Good", "Average", "Poor"].index(d.get("housekeeping", "Good")),
    )

    # =========================
    # SMART RISK ALERTS
    # =========================
    if d.get("hs_policy") == "No":
        st.error("⚠️ No Health & Safety policy → High liability risk")

    if d.get("ppe_provided") == "No" or d.get("ppe_usage") == "Low":
        st.warning("⚠️ PPE risk → Increased injury exposure")

    if d.get("incident_history") == "Major Incidents":
        st.error("⚠️ Major past incidents → High underwriting concern")


elif section == "Fire Protection":
    st.header("Fire Protection & Prevention Systems")

    # =========================
    # DETECTION SYSTEMS
    # =========================
    d["fire_detection"] = st.selectbox(
        "Fire Detection System",
        ["None", "Smoke Detectors", "Heat Detectors", "Automatic Fire Alarm System"],
        index=[
            "None",
            "Smoke Detectors",
            "Heat Detectors",
            "Automatic Fire Alarm System",
        ].index(d.get("fire_detection", "None")),
    )

    d["alarm_monitoring"] = st.selectbox(
        "Alarm Monitoring",
        [
            "None",
            "Local Alarm Only",
            "Connected to Security",
            "Connected to Fire Brigade",
        ],
        index=[
            "None",
            "Local Alarm Only",
            "Connected to Security",
            "Connected to Fire Brigade",
        ].index(d.get("alarm_monitoring", "None")),
    )

    # =========================
    # FIRE EXTINGUISHERS
    # =========================
    d["extinguishers"] = st.selectbox(
        "Fire Extinguishers Available?",
        ["Yes", "No"],
        index=["Yes", "No"].index(d.get("extinguishers", "Yes")),
    )

    d["extinguisher_type"] = st.text_input(
        "Type of Extinguishers (CO2, Foam, Dry Powder, etc.)",
        d.get("extinguisher_type", ""),
    )

    d["extinguisher_service"] = st.selectbox(
        "Extinguishers Serviced Regularly?",
        ["Yes", "No"],
        index=["Yes", "No"].index(d.get("extinguisher_service", "Yes")),
    )

    # =========================
    # SPRINKLER SYSTEM
    # =========================
    d["sprinklers"] = st.selectbox(
        "Automatic Sprinkler System?",
        ["Yes", "No"],
        index=["Yes", "No"].index(d.get("sprinklers", "No")),
    )

    d["sprinkler_coverage"] = st.selectbox(
        "Sprinkler Coverage",
        ["Full", "Partial", "None"],
        index=["Full", "Partial", "None"].index(d.get("sprinkler_coverage", "None")),
    )

    # =========================
    # FIRE HYDRANTS / WATER
    # =========================
    d["hydrants"] = st.selectbox(
        "Fire Hydrants Available?",
        ["Yes", "No"],
        index=["Yes", "No"].index(d.get("hydrants", "No")),
    )

    d["water_supply_fire"] = st.selectbox(
        "Dedicated Fire Water Supply?",
        ["Yes", "No"],
        index=["Yes", "No"].index(d.get("water_supply_fire", "No")),
    )

    # =========================
    # FIRE RESPONSE
    # =========================
    d["fire_team"] = st.selectbox(
        "Trained Fire Response Team?",
        ["Yes", "No"],
        index=["Yes", "No"].index(d.get("fire_team", "No")),
    )

    d["fire_drills"] = st.selectbox(
        "Fire Drills Conducted?",
        ["Regular", "Occasional", "None"],
        index=["Regular", "Occasional", "None"].index(d.get("fire_drills", "None")),
    )

    # =========================
    # HOUSEKEEPING & STORAGE
    # =========================
    d["combustibles_control"] = st.selectbox(
        "Combustible Materials Controlled?",
        ["Well Controlled", "Moderate", "Poor"],
        index=["Well Controlled", "Moderate", "Poor"].index(
            d.get("combustibles_control", "Moderate")
        ),
    )

    d["flammable_storage"] = st.text_area(
        "Flammable Materials Storage (chemicals, fuel, etc.)",
        d.get("flammable_storage", ""),
    )

    # =========================
    # ELECTRICAL FIRE RISK
    # =========================
    d["electrical_fire_risk"] = st.selectbox(
        "Electrical Fire Risk",
        ["Low", "Medium", "High"],
        index=["Low", "Medium", "High"].index(d.get("electrical_fire_risk", "Medium")),
    )

    # =========================
    # SMART RISK ALERTS
    # =========================
    if d.get("fire_detection") == "None":
        st.error("🚨 No fire detection system → VERY HIGH RISK")

    if d.get("sprinklers") == "No":
        st.warning("⚠️ No sprinkler system → Increased fire severity risk")

    if d.get("extinguishers") == "No":
        st.error("🚨 No extinguishers → Critical fire exposure")

    if d.get("fire_drills") == "None":
        st.warning("⚠️ No fire drills → Poor emergency preparedness")

    if d.get("combustibles_control") == "Poor":
        st.error("🚨 Poor combustible control → High fire load risk")

elif section == "Fire Services":
    st.header("Fire Services")

    d["fire_services"] = st.text_area(
        "Nearest Fire Brigade / Response Details", d.get("fire_services", "")
    )

    d["fire_distance"] = st.text_input(
        "Distance to Fire Station (km)", d.get("fire_distance", "")
    )

    d["fire_response_time"] = st.text_input(
        "Estimated Response Time (minutes)", d.get("fire_response_time", "")
    )

elif section == "Security":
    st.header("Security & Loss Prevention")

    # =========================
    # PHYSICAL SECURITY
    # =========================
    d["perimeter"] = st.selectbox(
        "Perimeter Protection",
        ["None", "Fence", "Wall", "Electric Fence", "Mixed"],
        index=["None", "Fence", "Wall", "Electric Fence", "Mixed"].index(
            d.get("perimeter", "Fence")
        ),
    )

    d["access_control"] = st.selectbox(
        "Access Control",
        ["None", "Manual (Guards)", "Controlled Entry", "Biometric / Card Access"],
        index=[
            "None",
            "Manual (Guards)",
            "Controlled Entry",
            "Biometric / Card Access",
        ].index(d.get("access_control", "Manual (Guards)")),
    )

    d["security_guards"] = st.selectbox(
        "Security Guards",
        ["None", "Day Only", "Night Only", "24/7"],
        index=["None", "Day Only", "Night Only", "24/7"].index(
            d.get("security_guards", "Night Only")
        ),
    )

    # =========================
    # ELECTRONIC SECURITY
    # =========================
    d["cctv"] = st.selectbox(
        "CCTV Surveillance",
        ["None", "Partial Coverage", "Full Coverage"],
        index=["None", "Partial Coverage", "Full Coverage"].index(
            d.get("cctv", "Partial Coverage")
        ),
    )

    d["alarm_system"] = st.selectbox(
        "Intruder Alarm System",
        ["None", "Local Alarm", "Monitored Alarm"],
        index=["None", "Local Alarm", "Monitored Alarm"].index(
            d.get("alarm_system", "None")
        ),
    )

    d["alarm_response"] = st.selectbox(
        "Alarm Response",
        ["None", "Security Company", "Police Linked"],
        index=["None", "Security Company", "Police Linked"].index(
            d.get("alarm_response", "None")
        ),
    )

    # =========================
    # PANIC BUTTON (YOUR REQUEST)
    # =========================
    d["panic_button"] = st.selectbox(
        "Panic Button Available?",
        ["Yes", "No"],
        index=["Yes", "No"].index(d.get("panic_button", "No")),
    )

    # =========================
    # KEY CONTROL & CASH SECURITY
    # =========================
    d["key_control"] = st.selectbox(
        "Key / Access Control Management",
        ["Poor", "Moderate", "Strict"],
        index=["Poor", "Moderate", "Strict"].index(d.get("key_control", "Moderate")),
    )

    d["safe_available"] = st.selectbox(
        "Safe / Strong Room Available?",
        ["Yes", "No"],
        index=["Yes", "No"].index(d.get("safe_available", "Yes")),
    )

    # =========================
    # LIGHTING
    # =========================
    d["lighting"] = st.selectbox(
        "External Lighting",
        ["Poor", "Adequate", "Good"],
        index=["Poor", "Adequate", "Good"].index(d.get("lighting", "Adequate")),
    )

    # =========================
    # PREVIOUS INCIDENTS (YOUR REQUEST)
    # =========================
    d["theft_history"] = st.selectbox(
        "Previous Theft / Burglary Incidents",
        ["None", "Minor Incidents", "Major Incidents"],
        index=["None", "Minor Incidents", "Major Incidents"].index(
            d.get("theft_history", "None")
        ),
    )

    d["incident_details"] = st.text_area(
        "Details of Previous Security Incidents", d.get("incident_details", "")
    )

    # =========================
    # INTERNAL SECURITY (FRAUD)
    # =========================
    d["internal_controls"] = st.selectbox(
        "Internal Controls (fraud prevention)",
        ["Weak", "Moderate", "Strong"],
        index=["Weak", "Moderate", "Strong"].index(
            d.get("internal_controls", "Moderate")
        ),
    )

    # =========================
    # SMART RISK ALERTS
    # =========================
    if d.get("cctv") == "None":
        st.warning("⚠️ No CCTV → High theft risk")

    if d.get("security_guards") == "None":
        st.warning("⚠️ No security guards → Increased vulnerability")

    if d.get("alarm_system") == "None":
        st.error("🚨 No alarm system → Critical security weakness")

    if d.get("theft_history") == "Major Incidents":
        st.error("🚨 History of major theft → High underwriting risk")

    if d.get("lighting") == "Poor":
        st.warning("⚠️ Poor lighting → Increased night-time risk")

    if d.get("panic_button") == "No":
        st.info("ℹ️ Consider installing panic buttons for emergency response")

elif section == "Cash/Stocks":
    st.header("Cash / Stocks")

    d["cash"] = st.text_area(
        "Cash Handling (limits, safes, controls)", d.get("cash", "")
    )

    d["stock_value"] = st.text_input(
        "Estimated Stock Value (KES)", d.get("stock_value", "")
    )

    d["stock_type"] = st.text_area(
        "Type of Stock (e.g. electronics, food, chemicals)", d.get("stock_type", "")
    )

elif section == "Storage":
    st.header("Storage & Inventory Risk")

    # =========================
    # TYPE OF GOODS
    # =========================
    d["goods_type"] = st.text_area(
        "Type of Goods Stored (e.g. electronics, food, chemicals, flammable goods)",
        d.get("goods_type", ""),
    )

    d["value_concentration"] = st.selectbox(
        "Value Concentration",
        ["Low", "Moderate", "High"],
        index=["Low", "Moderate", "High"].index(
            d.get("value_concentration", "Moderate")
        ),
    )

    # =========================
    # STORAGE METHOD
    # =========================
    d["storage_method"] = st.selectbox(
        "Storage Method",
        ["Open Floor", "Shelving", "Racking System", "Cold Storage"],
        index=["Open Floor", "Shelving", "Racking System", "Cold Storage"].index(
            d.get("storage_method", "Shelving")
        ),
    )

    d["stacking_height"] = st.selectbox(
        "Stacking Height",
        ["Low (<2m)", "Medium (2–4m)", "High (>4m)"],
        index=["Low (<2m)", "Medium (2–4m)", "High (>4m)"].index(
            d.get("stacking_height", "Medium (2–4m)")
        ),
    )

    # =========================
    # HOUSEKEEPING
    # =========================
    d["storage_housekeeping"] = st.selectbox(
        "Housekeeping Standard",
        ["Good", "Average", "Poor"],
        index=["Good", "Average", "Poor"].index(d.get("storage_housekeeping", "Good")),
    )

    # =========================
    # FIRE RISK
    # =========================
    d["combustibility"] = st.selectbox(
        "Combustibility of Stored Goods",
        ["Non-combustible", "Moderately Combustible", "Highly Combustible"],
        index=["Non-combustible", "Moderately Combustible", "Highly Combustible"].index(
            d.get("combustibility", "Moderately Combustible")
        ),
    )

    d["separation"] = st.selectbox(
        "Separation of Goods",
        ["Well Separated", "Partially Separated", "No Separation"],
        index=["Well Separated", "Partially Separated", "No Separation"].index(
            d.get("separation", "Partially Separated")
        ),
    )

    # =========================
    # SECURITY OF STORAGE
    # =========================
    d["storage_security"] = st.selectbox(
        "Storage Area Security",
        ["Restricted Access", "Moderate Control", "Open Access"],
        index=["Restricted Access", "Moderate Control", "Open Access"].index(
            d.get("storage_security", "Moderate Control")
        ),
    )

    # =========================
    # SPECIAL STORAGE CONDITIONS
    # =========================
    d["temperature_control"] = st.selectbox(
        "Temperature-Controlled Storage?",
        ["Yes", "No"],
        index=["Yes", "No"].index(d.get("temperature_control", "No")),
    )

    d["hazardous_storage"] = st.selectbox(
        "Hazardous Materials Stored?",
        ["Yes", "No"],
        index=["Yes", "No"].index(d.get("hazardous_storage", "No")),
    )

    # =========================
    # DAMAGE EXPOSURE
    # =========================
    d["water_damage_risk"] = st.selectbox(
        "Water Damage Risk",
        ["Low", "Medium", "High"],
        index=["Low", "Medium", "High"].index(d.get("water_damage_risk", "Low")),
    )

    # =========================
    # SMART RISK ALERTS
    # =========================
    if d.get("combustibility") == "Highly Combustible":
        st.error("🔥 High fire load → Increased fire severity risk")

    if d.get("value_concentration") == "High":
        st.warning("💰 High value concentration → Large loss potential")

    if d.get("storage_security") == "Open Access":
        st.warning("⚠️ Poor storage security → Theft risk")

    if d.get("storage_housekeeping") == "Poor":
        st.warning("⚠️ Poor housekeeping → Fire + trip hazard")

    if d.get("hazardous_storage") == "Yes":
        st.error("⚠️ Hazardous materials present → Special risk controls required")

elif section == "Computers":
    st.header("IT Systems & Cyber Risk")

    # =========================
    # IT INFRASTRUCTURE
    # =========================
    d["it_usage"] = st.selectbox(
        "IT Dependency Level",
        ["Low", "Moderate", "High", "Critical"],
        index=["Low", "Moderate", "High", "Critical"].index(
            d.get("it_usage", "Moderate")
        ),
    )

    d["systems_type"] = st.text_area(
        "Systems Used (Accounting, ERP, POS, Servers, Cloud systems)",
        d.get("systems_type", ""),
    )

    # =========================
    # HARDWARE SECURITY
    # =========================
    d["hardware_security"] = st.selectbox(
        "Physical Security of IT Equipment",
        ["Poor", "Moderate", "Secure"],
        index=["Poor", "Moderate", "Secure"].index(
            d.get("hardware_security", "Moderate")
        ),
    )

    d["server_location"] = st.selectbox(
        "Server Location",
        ["On-site", "Off-site", "Cloud", "Mixed"],
        index=["On-site", "Off-site", "Cloud", "Mixed"].index(
            d.get("server_location", "On-site")
        ),
    )

    # =========================
    # DATA BACKUP
    # =========================
    d["data_backup"] = st.selectbox(
        "Data Backup Frequency",
        ["None", "Occasional", "Daily", "Real-time"],
        index=["None", "Occasional", "Daily", "Real-time"].index(
            d.get("data_backup", "Occasional")
        ),
    )

    d["backup_location"] = st.selectbox(
        "Backup Storage Location",
        ["None", "On-site", "Off-site", "Cloud"],
        index=["None", "On-site", "Off-site", "Cloud"].index(
            d.get("backup_location", "On-site")
        ),
    )

    # =========================
    # CYBER SECURITY
    # =========================
    d["antivirus"] = st.selectbox(
        "Antivirus / Endpoint Protection",
        ["None", "Basic", "Advanced"],
        index=["None", "Basic", "Advanced"].index(d.get("antivirus", "Basic")),
    )

    d["firewall"] = st.selectbox(
        "Firewall Protection",
        ["None", "Basic", "Advanced"],
        index=["None", "Basic", "Advanced"].index(d.get("firewall", "Basic")),
    )

    d["access_control_it"] = st.selectbox(
        "User Access Control",
        ["Weak", "Moderate", "Strict"],
        index=["Weak", "Moderate", "Strict"].index(
            d.get("access_control_it", "Moderate")
        ),
    )

    # =========================
    # NETWORK SECURITY
    # =========================
    d["network_type"] = st.selectbox(
        "Network Type",
        ["Open", "Password Protected", "Secure (VPN/Segregated)"],
        index=["Open", "Password Protected", "Secure (VPN/Segregated)"].index(
            d.get("network_type", "Password Protected")
        ),
    )

    # =========================
    # INCIDENT HISTORY
    # =========================
    d["cyber_incidents"] = st.selectbox(
        "Previous Cyber Incidents",
        ["None", "Minor", "Major"],
        index=["None", "Minor", "Major"].index(d.get("cyber_incidents", "None")),
    )

    d["incident_details_it"] = st.text_area(
        "Details of Cyber / IT Incidents", d.get("incident_details_it", "")
    )

    # =========================
    # BUSINESS CONTINUITY
    # =========================
    d["it_recovery"] = st.selectbox(
        "IT Recovery Capability",
        ["None", "Basic", "Advanced"],
        index=["None", "Basic", "Advanced"].index(d.get("it_recovery", "Basic")),
    )

    # =========================
    # SMART RISK ALERTS
    # =========================
    if d.get("data_backup") == "None":
        st.error("🚨 No data backup → Critical business risk")

    if d.get("backup_location") == "On-site" and d.get("server_location") == "On-site":
        st.warning("⚠️ Backup and servers in same location → Total loss risk")

    if d.get("antivirus") == "None" or d.get("firewall") == "None":
        st.error("🚨 No cyber protection → High cyber risk")

    if d.get("cyber_incidents") == "Major":
        st.error("🚨 History of cyber attacks → High underwriting concern")

    if d.get("it_usage") == "Critical" and d.get("it_recovery") == "None":
        st.error("🚨 Critical IT with no recovery → Severe interruption risk")

elif section == "Waste Disposal":
    st.header("Waste Management & Environmental Risk")

    # =========================
    # TYPE OF WASTE
    # =========================
    d["waste_type"] = st.multiselect(
        "Type of Waste Generated",
        ["General", "Organic", "Plastic", "Metal", "Chemical", "Hazardous"],
        default=d.get("waste_type", []),
    )

    d["waste_volume"] = st.selectbox(
        "Volume of Waste",
        ["Low", "Moderate", "High"],
        index=["Low", "Moderate", "High"].index(d.get("waste_volume", "Moderate")),
    )

    # =========================
    # STORAGE OF WASTE
    # =========================
    d["waste_storage"] = st.selectbox(
        "Waste Storage Method",
        ["Open Area", "Bins", "Covered Containers", "Segregated Storage"],
        index=["Open Area", "Bins", "Covered Containers", "Segregated Storage"].index(
            d.get("waste_storage", "Bins")
        ),
    )

    d["waste_separation"] = st.selectbox(
        "Waste Segregation",
        ["None", "Partial", "Proper Segregation"],
        index=["None", "Partial", "Proper Segregation"].index(
            d.get("waste_separation", "Partial")
        ),
    )

    # =========================
    # DISPOSAL METHOD
    # =========================
    d["disposal_method"] = st.selectbox(
        "Disposal Method",
        ["Open Dumping", "Municipal Collection", "Recycling", "Licensed Contractor"],
        index=[
            "Open Dumping",
            "Municipal Collection",
            "Recycling",
            "Licensed Contractor",
        ].index(d.get("disposal_method", "Municipal Collection")),
    )

    d["disposal_frequency"] = st.selectbox(
        "Waste Disposal Frequency",
        ["Daily", "Weekly", "Occasional"],
        index=["Daily", "Weekly", "Occasional"].index(
            d.get("disposal_frequency", "Weekly")
        ),
    )

    # =========================
    # HAZARDOUS WASTE
    # =========================
    d["hazardous_waste"] = st.selectbox(
        "Hazardous Waste Present?",
        ["Yes", "No"],
        index=["Yes", "No"].index(d.get("hazardous_waste", "No")),
    )

    d["hazardous_handling"] = st.text_area(
        "Handling of Hazardous Waste (labeling, storage, disposal procedures)",
        d.get("hazardous_handling", ""),
    )

    # =========================
    # COMPLIANCE
    # =========================
    d["waste_compliance"] = st.selectbox(
        "Compliance with Environmental Regulations",
        ["Compliant", "Partially Compliant", "Non-Compliant"],
        index=["Compliant", "Partially Compliant", "Non-Compliant"].index(
            d.get("waste_compliance", "Compliant")
        ),
    )

    d["licensed_collector"] = st.selectbox(
        "Use of Licensed Waste Collector?",
        ["Yes", "No"],
        index=["Yes", "No"].index(d.get("licensed_collector", "Yes")),
    )

    # =========================
    # FIRE & HEALTH RISK
    # =========================
    d["waste_fire_risk"] = st.selectbox(
        "Fire Risk from Waste",
        ["Low", "Medium", "High"],
        index=["Low", "Medium", "High"].index(d.get("waste_fire_risk", "Medium")),
    )

    # =========================
    # SMART RISK ALERTS
    # =========================
    if d.get("disposal_method") == "Open Dumping":
        st.error("🚨 Open dumping → High environmental & fire risk")

    if d.get("hazardous_waste") == "Yes" and d.get("licensed_collector") == "No":
        st.error("🚨 Hazardous waste without licensed disposal → Regulatory risk")

    if d.get("waste_separation") == "None":
        st.warning("⚠️ No waste segregation → Increased contamination risk")

    if d.get("waste_fire_risk") == "High":
        st.error("🔥 Waste poses high fire risk")

    if d.get("waste_compliance") == "Non-Compliant":
        st.error("🚨 Non-compliance → Legal and insurance risk")

elif section == "Perils":
    st.header("Perils & External Risk Exposure")

    # =========================
    # PRIMARY PERILS
    # =========================
    d["fire_peril"] = st.selectbox(
        "Fire Risk Exposure",
        ["Low", "Medium", "High"],
        index=["Low", "Medium", "High"].index(d.get("fire_peril", "Medium")),
    )

    d["flood_peril"] = st.selectbox(
        "Flood Risk",
        ["Low", "Medium", "High"],
        index=["Low", "Medium", "High"].index(d.get("flood_peril", "Low")),
    )

    d["theft_peril"] = st.selectbox(
        "Theft / Burglary Risk",
        ["Low", "Medium", "High"],
        index=["Low", "Medium", "High"].index(d.get("theft_peril", "Medium")),
    )

    # =========================
    # NATURAL PERILS
    # =========================
    d["storm_peril"] = st.selectbox(
        "Storm / Wind Damage Risk",
        ["Low", "Medium", "High"],
        index=["Low", "Medium", "High"].index(d.get("storm_peril", "Low")),
    )

    d["earthquake_peril"] = st.selectbox(
        "Earthquake Risk",
        ["Low", "Medium", "High"],
        index=["Low", "Medium", "High"].index(d.get("earthquake_peril", "Low")),
    )

    d["lightning_peril"] = st.selectbox(
        "Lightning Risk",
        ["Low", "Medium", "High"],
        index=["Low", "Medium", "High"].index(d.get("lightning_peril", "Medium")),
    )

    # =========================
    # LOCATION-BASED RISKS
    # =========================
    d["proximity_risk"] = st.text_area(
        "Nearby Risk Exposures (e.g. petrol stations, factories, rivers)",
        d.get("proximity_risk", ""),
    )

    d["crime_area"] = st.selectbox(
        "Crime Level in Area",
        ["Low", "Moderate", "High"],
        index=["Low", "Moderate", "High"].index(d.get("crime_area", "Moderate")),
    )

    # =========================
    # SPECIAL PERILS
    # =========================
    d["riot_peril"] = st.selectbox(
        "Riot / Strike / Civil Commotion Risk",
        ["Low", "Medium", "High"],
        index=["Low", "Medium", "High"].index(d.get("riot_peril", "Low")),
    )

    d["terrorism_peril"] = st.selectbox(
        "Terrorism Risk",
        ["Low", "Medium", "High"],
        index=["Low", "Medium", "High"].index(d.get("terrorism_peril", "Low")),
    )

    # =========================
    # OVERALL RISK PERCEPTION
    # =========================
    d["overall_peril"] = st.selectbox(
        "Overall Peril Exposure",
        ["Low", "Medium", "High"],
        index=["Low", "Medium", "High"].index(d.get("overall_peril", "Medium")),
    )

    # =========================
    # SMART RISK ALERTS
    # =========================
    if d.get("flood_peril") == "High":
        st.error("🌊 High flood risk → Possible exclusion or loading")

    if d.get("fire_peril") == "High":
        st.error("🔥 High fire exposure → Critical underwriting concern")

    if d.get("crime_area") == "High" and d.get("theft_peril") == "High":
        st.warning("⚠️ High crime area + theft risk → Increased burglary exposure")

    if d.get("riot_peril") == "High":
        st.warning("⚠️ Civil unrest risk → Political violence exposure")

    if d.get("overall_peril") == "High":
        st.error("🚨 Overall risk level high → Requires strict underwriting controls")

elif section == "Process":
    st.header("Operational Process & Risk Exposure")

    # =========================
    # BUSINESS OPERATIONS
    # =========================
    d["process_description"] = st.text_area(
        "Describe Core Business Process / Operations", d.get("process_description", "")
    )

    d["industry_type"] = st.text_input(
        "Industry Type (e.g. manufacturing, retail, hotel, warehouse)",
        d.get("industry_type", ""),
    )

    # =========================
    # PROCESS TYPE
    # =========================
    d["process_nature"] = st.selectbox(
        "Nature of Operations",
        ["Manual", "Semi-Automated", "Fully Automated"],
        index=["Manual", "Semi-Automated", "Fully Automated"].index(
            d.get("process_nature", "Manual")
        ),
    )

    d["process_complexity"] = st.selectbox(
        "Process Complexity",
        ["Simple", "Moderate", "Complex"],
        index=["Simple", "Moderate", "Complex"].index(
            d.get("process_complexity", "Moderate")
        ),
    )

    # =========================
    # MACHINERY & EQUIPMENT
    # =========================
    d["machinery_used"] = st.text_area(
        "Machinery / Equipment Used", d.get("machinery_used", "")
    )

    d["machinery_condition"] = st.selectbox(
        "Condition of Machinery",
        ["New", "Good", "Old", "Poor"],
        index=["New", "Good", "Old", "Poor"].index(
            d.get("machinery_condition", "Good")
        ),
    )

    d["maintenance_program"] = st.selectbox(
        "Maintenance Program",
        ["None", "Reactive", "Preventive", "Predictive"],
        index=["None", "Reactive", "Preventive", "Predictive"].index(
            d.get("maintenance_program", "Preventive")
        ),
    )

    # =========================
    # PROCESS HAZARDS
    # =========================
    d["heat_process"] = st.selectbox(
        "Heat / Open Flame Processes?",
        ["Yes", "No"],
        index=["Yes", "No"].index(d.get("heat_process", "No")),
    )

    d["chemical_use"] = st.selectbox(
        "Use of Chemicals?",
        ["Yes", "No"],
        index=["Yes", "No"].index(d.get("chemical_use", "No")),
    )

    d["dust_generation"] = st.selectbox(
        "Dust Generation (explosion risk)?",
        ["Yes", "No"],
        index=["Yes", "No"].index(d.get("dust_generation", "No")),
    )

    # =========================
    # PROCESS CONTROLS
    # =========================
    d["process_controls"] = st.text_area(
        "Process Controls (safety interlocks, shutdown systems, monitoring)",
        d.get("process_controls", ""),
    )

    d["quality_control"] = st.selectbox(
        "Quality Control System",
        ["None", "Basic", "Advanced"],
        index=["None", "Basic", "Advanced"].index(d.get("quality_control", "Basic")),
    )

    # =========================
    # HUMAN FACTOR
    # =========================
    d["operator_skill"] = st.selectbox(
        "Operator Skill Level",
        ["Low", "Moderate", "High"],
        index=["Low", "Moderate", "High"].index(d.get("operator_skill", "Moderate")),
    )

    # =========================
    # PROCESS DEPENDENCY
    # =========================
    d["critical_process"] = st.selectbox(
        "Is Process Critical to Business?",
        ["Yes", "No"],
        index=["Yes", "No"].index(d.get("critical_process", "Yes")),
    )

    # =========================
    # SMART RISK ALERTS
    # =========================
    if d.get("heat_process") == "Yes":
        st.error("🔥 Heat processes present → Increased fire risk")

    if d.get("chemical_use") == "Yes":
        st.warning("⚠️ Chemical usage → Environmental & safety risk")

    if d.get("dust_generation") == "Yes":
        st.error("💥 Dust explosion risk present")

    if d.get("machinery_condition") in ["Old", "Poor"]:
        st.warning("⚠️ Machinery condition increases breakdown/fire risk")

    if d.get("maintenance_program") == "None":
        st.error("🚨 No maintenance → High failure risk")

    if d.get("critical_process") == "Yes" and d.get("process_controls") == "":
        st.error("🚨 Critical process without controls → Severe risk")

elif section == "Hazardous Substances":
    st.header("Hazardous Substances")

    d["hazardous"] = st.text_area(
        "List hazardous substances (chemicals, fuels, gases)", d.get("hazardous", "")
    )

    d["storage_controls"] = st.text_area(
        "Storage & handling controls (MSDS, ventilation, segregation)",
        d.get("storage_controls", ""),
    )

    d["ppe"] = st.text_area(
        "Personal Protective Equipment (PPE) used", d.get("ppe", "")
    )

    d["spill_measures"] = st.text_area(
        "Spill / emergency response measures", d.get("spill_measures", "")
    )
elif section == "Unions":
    st.header("Unions & Industrial Relations")

    d["union_presence"] = st.selectbox(
        "Is there a workers union?",
        ["No", "Yes"],
        index=0 if d.get("union_presence", "No") == "No" else 1,
    )

    d["union_activity"] = st.text_area(
        "Union activity / history of strikes / disputes", d.get("union_activity", "")
    )

    d["labor_risk"] = st.text_area(
        "Labor-related risks (e.g. unrest, turnover, disputes)", d.get("labor_risk", "")
    )
elif section == "Losses Report":
    st.header("Loss History / Claims Experience")

    d["loss_history"] = st.text_area(
        "Past Losses (Fire, Theft, Liability, etc.)", d.get("loss_history", "")
    )

    d["loss_frequency"] = st.selectbox(
        "Frequency of Losses",
        ["None", "Rare", "Occasional", "Frequent"],
        index=["None", "Rare", "Occasional", "Frequent"].index(
            d.get("loss_frequency", "None")
        ),
    )

    d["largest_loss"] = st.text_input(
        "Largest Loss Recorded (KES)", d.get("largest_loss", "")
    )

    d["loss_cause"] = st.text_area("Main Causes of Losses", d.get("loss_cause", ""))

    d["preventive_measures"] = st.text_area(
        "Measures Taken to Prevent Recurrence", d.get("preventive_measures", "")
    )

elif section == "Interruption Analysis":
    st.header("Business Interruption Analysis")

    # =========================
    # FINANCIAL DATA
    # =========================
    d["annual_turnover"] = st.number_input(
        "Annual Turnover (KES)", value=float(d.get("annual_turnover", 0))
    )

    d["gross_profit"] = st.number_input(
        "Gross Profit (KES)", value=float(d.get("gross_profit", 0))
    )

    d["fixed_costs"] = st.number_input(
        "Fixed Costs (KES)", value=float(d.get("fixed_costs", 0))
    )

    # =========================
    # MAXIMUM INDEMNITY PERIOD
    # =========================
    d["indemnity_period"] = st.selectbox(
        "Indemnity Period (months)",
        [3, 6, 9, 12, 18, 24],
        index=[3, 6, 9, 12, 18, 24].index(int(d.get("indemnity_period", 12))),
    )

    # =========================
    # DOWNTIME ESTIMATION
    # =========================
    d["estimated_downtime"] = st.number_input(
        "Estimated Downtime (months)", value=float(d.get("estimated_downtime", 0))
    )

    # =========================
    # DEPENDENCIES
    # =========================
    d["key_suppliers"] = st.text_area(
        "Key Suppliers (dependency risk)", d.get("key_suppliers", "")
    )

    d["key_customers"] = st.text_area("Key Customers", d.get("key_customers", ""))

    d["utility_dependency"] = st.selectbox(
        "Dependency on Utilities (power, water)",
        ["Low", "Moderate", "High"],
        index=["Low", "Moderate", "High"].index(d.get("utility_dependency", "High")),
    )

    # =========================
    # BACKUP ARRANGEMENTS
    # =========================
    d["backup_plan"] = st.selectbox(
        "Business Continuity Plan",
        ["None", "Basic", "Comprehensive"],
        index=["None", "Basic", "Comprehensive"].index(d.get("backup_plan", "Basic")),
    )

    d["alternate_site"] = st.selectbox(
        "Alternative Operating Site Available?",
        ["Yes", "No"],
        index=["Yes", "No"].index(d.get("alternate_site", "No")),
    )

    # =========================
    # STOCK / PRODUCTION RECOVERY
    # =========================
    d["recovery_time"] = st.number_input(
        "Estimated Recovery Time (months)", value=float(d.get("recovery_time", 0))
    )

    # =========================
    # CALCULATED BI EXPOSURE
    # =========================
    if d.get("gross_profit") and d.get("indemnity_period"):
        monthly_profit = d["gross_profit"] / 12
        bi_exposure = monthly_profit * d["indemnity_period"]

        st.info(f"💰 Estimated BI Exposure: KES {bi_exposure:,.0f}")

    # =========================
    # RISK ALERTS
    # =========================
    if d.get("backup_plan") == "None":
        st.error("🚨 No continuity plan → High BI risk")

    if d.get("alternate_site") == "No":
        st.warning("⚠️ No alternative site → Longer downtime")

    if d.get("utility_dependency") == "High":
        st.warning("⚠️ High reliance on utilities")

    if d.get("estimated_downtime", 0) > d.get("indemnity_period", 12):
        st.error("🚨 Downtime exceeds indemnity period → Underinsurance risk")

# =========================
# LOSS
# =========================
elif section == "Risk Appraisal":
    st.header("Risk Appraisal")

    # =========================
    # ASSET VALUES
    # =========================
    d["building_value"] = st.number_input(
        "Building Value (KES)", value=safe_float(d.get("building_value", 0))
    )

    d["machinery_value"] = st.number_input(
        "Machinery Value (KES)", value=safe_float(d.get("machinery_value", 0))
    )

    d["stock_value"] = st.number_input(
        "Stock Value (KES)", value=safe_float(d.get("stock_value", 0))
    )

    d["furniture_value"] = st.number_input(
        "Furniture & Fixtures (KES)", value=safe_float(d.get("furniture_value", 0))
    )

    # =========================
    # TOTAL VALUE
    # =========================
    total_value = (
        d["building_value"]
        + d["machinery_value"]
        + d["stock_value"]
        + d["furniture_value"]
    )

    st.info(f"💰 Total Asset Value: KES {total_value:,.0f}")

    # =========================
    # SUM INSURED
    # =========================
    d["sum_insured"] = st.number_input(
        "Declared Sum Insured (KES)", value=float(d.get("sum_insured", total_value))
    )

    # =========================
    # LOSS ESTIMATES
    # =========================
    d["estimated_loss"] = st.number_input(
        "Estimated Likely Loss (KES)", value=float(d.get("estimated_loss", 0))
    )

    d["pml"] = st.number_input(
        "Probable Maximum Loss (PML)", value=float(d.get("pml", 0))
    )

    d["mpl"] = st.number_input(
        "Maximum Possible Loss (MPL)", value=float(d.get("mpl", 0))
    )

    # =========================
    # RISK PROBABILITY
    # =========================
    d["risk_probability"] = st.selectbox(
        "Likelihood of Loss",
        ["Low", "Medium", "High"],
        index=["Low", "Medium", "High"].index(d.get("risk_probability", "Medium")),
    )

    # =========================
    # PROTECTION ADEQUACY
    # =========================
    d["fire_protection_rating"] = st.selectbox(
        "Fire Protection Adequacy",
        ["Poor", "Average", "Good"],
        index=["Poor", "Average", "Good"].index(
            d.get("fire_protection_rating", "Average")
        ),
    )

    d["security_rating"] = st.selectbox(
        "Security Adequacy",
        ["Poor", "Average", "Good"],
        index=["Poor", "Average", "Good"].index(d.get("security_rating", "Average")),
    )

    # =========================
    # UNDERINSURANCE CHECK
    # =========================
    if total_value > 0:
        insurance_ratio = d["sum_insured"] / total_value

        if insurance_ratio < 0.8:
            st.error("🚨 Underinsured! Less than 80% of actual value")
        elif insurance_ratio < 1:
            st.warning("⚠️ Slight underinsurance detected")
        else:
            st.success("✅ Adequately insured")

    # =========================
    # FINAL RISK SCORE
    # =========================
    score = 0

    if d["risk_probability"] == "High":
        score += 3
    elif d["risk_probability"] == "Medium":
        score += 2
    else:
        score += 1

    if d["fire_protection_rating"] == "Poor":
        score += 3
    elif d["fire_protection_rating"] == "Average":
        score += 2
    else:
        score += 1

    if d["security_rating"] == "Poor":
        score += 3
    elif d["security_rating"] == "Average":
        score += 2
    else:
        score += 1

    # =========================
    # RISK LEVEL OUTPUT
    # =========================
    if score >= 8:
        st.error("🔥 HIGH RISK")
    elif score >= 5:
        st.warning("⚠️ MEDIUM RISK")
    else:
        st.success("✅ LOW RISK")

# SUBMIT (FINAL PROFESSIONAL)
# =========================

elif section == "Submit":

    st.header("Generate Final Equity Risk Survey Report")

    if st.button("📄 Generate Final Report"):

        from reportlab.platypus import (
            SimpleDocTemplate,
            Paragraph,
            Spacer,
            Table,
            TableStyle,
            Image,
            PageBreak,
        )
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.pdfgen import canvas

        def add_layout(canvas, doc):
            width, height = doc.pagesize

            # LOGO
            canvas.drawImage(
                "equity_logo.png", 40, height - 70, width=110, height=45, mask="auto"
            )

            # WATERMARK
            canvas.saveState()
            canvas.setFont("Helvetica-Bold", 100)
            canvas.setFillColor(colors.HexColor("#A6192E"))
            canvas.setFillAlpha(0.05)
            canvas.drawCentredString(width / 2, height / 2, "EGIK")
            canvas.restoreState()

            # DATE
            today = datetime.now().strftime("%d %B %Y").upper()
            canvas.setFont("Helvetica-Bold", 12)

            # FOOTER TEXT
            canvas.setFont("Helvetica-Bold", 11)
            canvas.setFillColor(colors.grey)
            canvas.drawCentredString(
                width / 2, 70, "EQUITY GENERAL INSURANCE (KENYA) LTD."
            )

            canvas.setFont("Helvetica", 10)
            canvas.drawCentredString(
                width / 2,
                55,
                "Equity General Insurance (Kenya) Ltd. is regulated by Insurance Regulatory Authority",
            )

            # FOOTER LINE
            canvas.setFillColor(colors.HexColor("#B76E79"))
            canvas.rect(40, 35, width * 0.5, 4, fill=1)

            canvas.setFillColor(colors.grey)
            canvas.rect(40 + width * 0.5, 35, width * 0.4, 4, fill=1)

            # PAGE NUMBER
            canvas.setFont("Helvetica", 10)
            canvas.setFillColor(colors.black)
            canvas.drawCentredString(width / 2, 20, str(doc.page))

        # =========================
        # CONTINUE YOUR CODE
        # =========================

        doc = SimpleDocTemplate("final_equity_report.pdf")
        styles = getSampleStyleSheet()
        normal = styles["Normal"]
        section_title = ParagraphStyle(
            name="section_title",
            fontSize=14,
            leading=16,
            textColor=colors.HexColor("#A6192E"),
            spaceAfter=10,
            spaceBefore=10,
            alignment=0,  # left aligned
        )
        story = []
        
        def add_bookmark(canvas, doc, key):
            canvas.bookmarkPage(key)

        # =========================
        # PAGE 1 — COVER PAGE (FINAL CLEAN)
        # =========================

        story.append(Spacer(1, 80))

        # TITLE
        story.append(
            Paragraph(
                "<b>RISK SURVEY REPORT</b>",
                ParagraphStyle(name="title_center", alignment=1, fontSize=18),
            )
        )

        # SPACE
        story.append(Spacer(1, 25))

        # COVER TEXT
        story.append(
            Paragraph(
                "<b>UPON</b>", ParagraphStyle(name="t2", alignment=1, fontSize=14)
            )
        )
        story.append(
            Paragraph(
                "<b>COVER PHOTO</b>",
                ParagraphStyle(name="t3", alignment=1, fontSize=14),
            )
        )

        # SPACE
        story.append(Spacer(1, 100))

        # CLIENT NAME
        story.append(
            Paragraph(
                "<b>CLIENT NAME:</b>",
                ParagraphStyle(name="t4", alignment=1, fontSize=16),
            )
        )

        # SPACE
        story.append(Spacer(1, 120))

        # DATE (AUTO)
        from datetime import datetime
        
        today = datetime.now().strftime("%d %B %Y, %H:%M")
        
        story.append(
            Paragraph(
                f"<b>{today}</b>", ParagraphStyle(name="t5", alignment=1, fontSize=14)
            )
        )

        story.append(PageBreak())
        
        toc = TableOfContents()

        toc.levelStyles = [
            ParagraphStyle(
                name='TOCHeading1',
                fontSize=12,
                leftIndent=20,
                firstLineIndent=-10,
                spaceBefore=5,
                leading=14
            )
        ]

        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.enums import TA_LEFT
        
        toc_style = ParagraphStyle(
            name="toc_item",
            fontSize=12,
            leading=14,
            leftIndent=40,
            rightIndent=20,
            firstLineIndent=0,
            alignment=TA_LEFT,
            spaceAfter=6,
            tabs=[
                (450, 'right', '.')  # 👈 THIS CREATES DOT LEADER + RIGHT ALIGN
                ]
        )
        
        # =========================
        # PAGE 2 — CONTENTS (FINAL STATIC)
        # =========================

        from reportlab.lib.enums import TA_LEFT, TA_RIGHT

        toc_style = ParagraphStyle(
            name="toc_item",
            fontSize=12,
            leading=14,
            leftIndent=40,
            rightIndent=20,
            alignment=TA_LEFT,
            spaceAfter=6,
            tabs=[TabStop(540, alignment=TA_RIGHT, leader='.')]
        )

        story.append(Spacer(1, 50))
        story.append(Paragraph("<b>CONTENTS</b>", toc_title_style))

        # TITLE (MATCHES WORD STYLE)
        def toc_line(title, page):
            return Paragraph(f"{title}<tab/>{page}", toc_style)

        # CONTENT LIST
        contents = [
            ("1. EXECUTIVE SUMMARY", 3),
            ("2. SCOPE & LIMITATIONS", 4),
            ("3. CONTROL & CONTACT DETAILS", 4),
            ("4. SITE DESCRIPTION & LOCATION", 5),
            ("5. OCCUPANCY & OPERATIONS", 6),
            ("6. BACKGROUND INFORMATION", 7),
            ("7. RISK IMPROVEMENT RECOMMENDATIONS", 8),
            ("8. PROCESS DESCRIPTION & HAZARDS", 9),
            ("9. FIRE PROTECTION SYSTEMS", 10),
            ("10. FIRE & EXPLOSION RISK", 11),
            ("11. ELECTRICAL RISK", 12),
            ("12. SECURITY", 12),
            ("13. UTILITIES", 13),
            ("14. MAINTENANCE & HOUSEKEEPING", 13),
            ("15. EMERGENCY PREPAREDNESS", 14),
            ("16. RISK SCORING MATRIX", 15),
            ("17. OVERALL RISK GRADING", 16),
            ("18. LOSS POTENTIAL (PML)", 17),
            ("19. INSURANCE REVIEW", 18),
            ("20. UNDERWRITING REMARKS", 19),
            ("21. PHOTO APPENDIX", 20),
        ]
        
        for title, page in contents:
            story.append(toc_line(title, page))


        story.append(PageBreak())


        # =========================
        # PAGE 3 — EXECUTIVE SUMMARY
        # =========================
        story.append(Paragraph("1. EXECUTIVE SUMMARY", section_title))
        story.append(Paragraph(clean_text(d.get("summary", "")), normal))
        story.append(PageBreak())


        # =========================
        # PAGE 4 — SCOPE & CONTACT
        # =========================
        story.append(Paragraph("2. SCOPE OF SURVEY & LIMITATIONS", section_title))
        story.append(Paragraph(clean_text(d.get("scope", "")), normal))

        story.append(Spacer(1, 20))

        story.append(Paragraph("3. CONTROL & CONTACT DETAILS", section_title))

        contact_data = [
            ["Insured", d.get("insured", "")],
            ["Location", d.get("location", "")],
            ["Nature of Business", d.get("business", "")],
            ["Employees", d.get("employees", "")],
            ["Survey Conducted By", d.get("surveyors", "")]
        ]

        table = Table(contact_data, colWidths=[180, 300])
        table.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 1, colors.black)]))
        story.append(table)

        story.append(PageBreak())


        # =========================
        # PAGE 5 — SITE & OPERATIONS
        # =========================
        story.append(Paragraph("4. SITE DESCRIPTION & LOCATION", section_title))
        story.append(Paragraph(clean_text(d.get("site", "")), normal))

        story.append(Spacer(1, 20))

        story.append(Paragraph("5. OCCUPANCY & OPERATIONS", section_title))
        story.append(Paragraph(clean_text(d.get("operations", "")), normal))

        story.append(PageBreak())


        # =========================
        # PAGE 6 — BACKGROUND + RIR
        # =========================
        story.append(Paragraph("6. BACKGROUND INFORMATION", section_title))
        story.append(Paragraph(clean_text(d.get("background", "")), normal))

        story.append(Spacer(1, 20))

        story.append(Paragraph("7. RISK IMPROVEMENT RECOMMENDATIONS (SUMMARY)", section_title))

        rir = [["Recommendation", "Description", "Priority"]]
        for r in d.get("rir", []):
            rir.append(r)

        t = Table(rir)
        t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 1, colors.black)]))
        story.append(t)

        story.append(PageBreak())


        # =========================
        # PAGE 7 — PROCESS & FIRE SYSTEMS
        # =========================
        story.append(Paragraph("8. PROCESS DESCRIPTION & HAZARDS ANALYSIS", section_title))
        story.append(Paragraph(clean_text(d.get("process", "")), normal))

        story.append(Spacer(1, 20))

        story.append(Paragraph("9. FIRE PROTECTION SYSTEMS", section_title))
        story.append(Paragraph(clean_text(d.get("fire_protection", "")), normal))

        story.append(PageBreak())


        # =========================
        # PAGE 8 — FIRE + ELECTRICAL
        # =========================
        story.append(Paragraph("10. FIRE & EXPLOSION RISK ASSESSMENT", section_title))
        story.append(Paragraph(clean_text(d.get("fire", "")), normal))

        story.append(Spacer(1, 20))

        story.append(Paragraph("11. ELECTRICAL INSTALLATION & RISK", section_title))
        story.append(Paragraph(clean_text(d.get("electrical", "")), normal))

        story.append(PageBreak())


        # =========================
        # PAGE 9 — SECURITY + UTILITIES
        # =========================
        story.append(Paragraph("12. SECURITY ARRANGEMENTS", section_title))
        story.append(Paragraph(clean_text(d.get("security", "")), normal))

        story.append(Spacer(1, 20))

        story.append(Paragraph("13. UTILITIES & SERVICES", section_title))
        story.append(Paragraph(clean_text(d.get("utilities", "")), normal))

        story.append(PageBreak())


        # =========================
        # PAGE 10 — MAINTENANCE + EMERGENCY
        # =========================
        story.append(Paragraph("14. MAINTENANCE & HOUSEKEEPING", section_title))
        story.append(Paragraph(clean_text(d.get("maintenance", "")), normal))

        story.append(Spacer(1, 20))

        story.append(Paragraph("15. EMERGENCY RESPONSE & PREPAREDNESS", section_title))
        story.append(Paragraph(clean_text(d.get("emergency", "")), normal))

        story.append(PageBreak())


        # =========================
        # PAGE 11 — SCORING + GRADING
        # =========================
        story.append(Paragraph("16. RISK SCORING MATRIX", section_title))
        story.append(Paragraph("Risk Score = Likelihood × Severity", normal))

        story.append(Spacer(1, 20))

        story.append(Paragraph("17. OVERALL RISK GRADING", section_title))
        story.append(Paragraph(clean_text(d.get("grading", "")), normal))

        story.append(PageBreak())


        # =========================
        # PAGE 12 — PML + INSURANCE
        # =========================
        story.append(Paragraph("18. LOSS POTENTIAL (PML)", section_title))
        story.append(Paragraph(clean_text(d.get("pml", "")), normal))

        story.append(Spacer(1, 20))

        story.append(Paragraph("19. INSURANCE PROGRAM REVIEW", section_title))

        ins = [["Class", "Coverage", "Limits"]]
        for i in d.get("insurance", []):
            ins.append(i)

        t = Table(ins)
        t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 1, colors.black)]))
        story.append(t)

        story.append(PageBreak())


        # =========================
        # PAGE 13 — FINAL
        # =========================
        story.append(Paragraph("20. UNDERWRITING REMARKS", section_title))
        story.append(Paragraph(clean_text(d.get("remarks", "")), normal))

        story.append(Spacer(1, 40))

        story.append(Paragraph("<b>Report By: Boniface Ondara</b>", normal))
        story.append(Paragraph("Risk Surveyor", normal))

        story.append(PageBreak())


        # =========================
        # PAGE 14 — PHOTOS
        # =========================
        story.append(Paragraph("21. PHOTOGRAPHIC APPENDIX", section_title))
        story.append(Paragraph("Insert site photographs here.", normal))

        # =========================
        # BUILD PDF
        # =========================
        doc.build(story, onFirstPage=add_layout, onLaterPages=add_layout)

        with open("final_equity_report.pdf", "rb") as f:
            st.download_button("⬇️ Download Final Report", f, "final_equity_report.pdf")

    # =========================
# 🚨 FALLBACK (NO BLANK SCREENS EVER)
# =========================
else:
    st.warning(f"⚠️ Section '{section}' not yet implemented")

# =========================
# NAV BUTTONS
# =========================
c1, c2, c3 = st.columns(3)

with c1:
    if st.session_state.step > 0:
        st.button("⬅️ Previous", on_click=prev_step)

with c3:
    if st.session_state.step < len(sections) - 1:
        st.button("Next ➡️", on_click=next_step)
