import streamlit as st
import random
from PIL import Image

# Define normal ranges for each parameter
normal_ranges = {
    "Blood Pressure": "< 120/80 mmHg",
    "Fasting Blood Sugar": "70 - 99 mg/dL",
    "LDL-C": "< 100 mg/dL",
    "hs-CRP": "< 1 mg/L",
    "eGFR": "≥ 90 mL/min/1.73m²",
    "ALT": "7 - 56 U/L",
    "AST": "10 - 40 U/L",
    "BMI": "18.5 - 24.9 kg/m²",
    "Alcohol Consumption": "≤ 2 drinks/day"
}

# Function to evaluate conditions
def evaluate_conditions(params):
    conditions = []
    explanations = []

    # Heart Diseases
    if params["Blood Pressure"] > 140:
        conditions.append("Hypertension")
        explanations.append("High blood pressure indicates Hypertension.")
    if params["LDL-C"] > 160:
        conditions.append("Hyperlipidemia")
        explanations.append("Elevated LDL-C levels indicate Hyperlipidemia.")
    if params["LDL-C"] > 130 and params["hs-CRP"] > 3:
        conditions.append("Coronary Artery Disease (CAD)")
        explanations.append("High LDL-C and hs-CRP levels indicate Coronary Artery Disease (CAD).")
    
    # Kidney Diseases
    if 60 <= params["eGFR"] < 90:
        conditions.append("Mild CKD (Stage 2)")
        explanations.append("eGFR levels indicate mild chronic kidney disease.")
    if 30 <= params["eGFR"] < 60:
        conditions.append("Moderate CKD (Stage 3)")
        explanations.append("eGFR levels indicate moderate chronic kidney disease.")
    if 15 <= params["eGFR"] < 30:
        conditions.append("Severe CKD (Stage 4)")
        explanations.append("eGFR levels indicate severe chronic kidney disease.")
    if params["eGFR"] < 15:
        conditions.append("End-Stage Renal Disease (Stage 5)")
        explanations.append("eGFR levels indicate end-stage renal disease.")
    if params["Fasting Blood Sugar"] > 126 and params["Blood Pressure"] > 130 and params["eGFR"] < 90:
        conditions.append("Diabetic Nephropathy")
        explanations.append("Elevated fasting blood sugar and reduced eGFR with high blood pressure indicate Diabetic Nephropathy.")
    
    # Liver Diseases
    if params["ALT"] > 40 and params["AST"] > 40 and params["BMI"] > 30 and params["Alcohol Consumption"] <= 2:
        conditions.append("Non-Alcoholic Fatty Liver Disease (NAFLD)")
        explanations.append("Elevated liver enzymes, high BMI, and low alcohol consumption indicate Non-Alcoholic Fatty Liver Disease (NAFLD).")
    if params["ALT"] > 40 and params["AST"] > 40 and params["Alcohol Consumption"] > 2:
        conditions.append("Alcoholic Liver Disease")
        explanations.append("Elevated liver enzymes and high alcohol consumption indicate Alcoholic Liver Disease.")
    if params["ALT"] > 80 and params["AST"] > 80:
        conditions.append("Liver Fibrosis")
        explanations.append("Severely elevated liver enzymes indicate Liver Fibrosis.")

    return conditions, explanations

# Streamlit interface
st.set_page_config(page_title="Health Screening Tool", layout="wide")

# Function to load image with error handling
def load_image(image_path):
    try:
        return Image.open(image_path)
    except Exception as e:
        st.error(f"Error loading image: {e}")
        return None

# Sidebar Layout
logo_image = load_image("logo.png")
right_fundus_image = load_image("right_fundus_example.jpg")
left_fundus_image = load_image("left_fundus_example.jpg")

if logo_image:
    st.sidebar.image(logo_image, use_container_width=True)
if right_fundus_image:
    st.sidebar.image(right_fundus_image, caption="Right Fundus Image", width=150)
if left_fundus_image:
    st.sidebar.image(left_fundus_image, caption="Left Fundus Image", width=150)

st.sidebar.write("This is a demo app, purely for demonstration purposes, not for any type of medical, clinical, or research use.")

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1

# Add New Record Section
if st.sidebar.button("Add New Record"):
    st.session_state.step = 1

# Step 1: Collect basic details
if st.session_state.step == 1:
    with st.form("patient_form"):
        st.write("Step 1: Enter Basic Details")
        st.session_state.patient_id = random.randint(10000, 99999)
        st.session_state.patient_name = st.text_input("Patient Name")
        st.session_state.age = st.number_input("Age", min_value=0, max_value=120)
        st.session_state.gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        st.session_state.alcohol_status = st.selectbox("Alcoholic Status", ["Yes", "No"])
        st.session_state.smoking_status = st.selectbox("Smoking Status", ["Yes", "No"])
        medical_history_options = ["Diabetes", "Hypertension", "Heart Disease", "Kidney Disease", "Liver Disease", "Other"]
        st.session_state.medical_history = st.multiselect("Any Medical History", medical_history_options)
        family_history_options = ["Diabetes", "Hypertension", "Heart Disease", "Kidney Disease", "Liver Disease", "Other"]
        st.session_state.family_history = st.multiselect("Family Medical History", family_history_options)
        
        if st.form_submit_button("Next"):
            st.session_state.step = 2

# Step 2: Upload fundus images
if st.session_state.step == 2:
    with st.form("image_upload_form"):
        st.write("Step 2: Upload Fundus Images")
        st.session_state.right_fundus_image = st.file_uploader("Upload Right Fundus Image", type=["png", "jpg", "jpeg"], key="right_fundus_new")
        st.session_state.left_fundus_image = st.file_uploader("Upload Left Fundus Image", type=["png", "jpg", "jpeg"], key="left_fundus_new")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.form_submit_button("Back"):
                st.session_state.step = 1
        with col2:
            if st.form_submit_button("Generate Report"):
                if st.session_state.right_fundus_image and st.session_state.left_fundus_image:
                    st.session_state.step = 3
                else:
                    st.error("Please upload both fundus images before proceeding.")

# Step 3: Generate and display the report
if st.session_state.step == 3:
    with st.form("health_parameters_form"):
    
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.form_submit_button("Back"):
                st.session_state.step = 2
        with col2:
            if st.form_submit_button("Generate Report"):
                # Create a dictionary for the input parameters
                params = {
                    "Age": st.session_state.age,
                    "Gender": st.session_state.gender,
                    "BMI": bmi,
                    "Smoking Status": st.session_state.smoking_status,
                    "Alcohol Consumption": st.session_state.alcohol_status,
                    "Blood Pressure": blood_pressure,
                    "Fasting Blood Sugar": fasting_blood_sugar,
                    "LDL-C": ldl_c,
                    "hs-CRP": hs_crp,
                    "eGFR": egfr,
                    "ALT": alt,
                    "AST": ast
                }

                # Evaluate the conditions based on the input parameters
                conditions, explanations = evaluate_conditions(params)

                # Display the results
                st.subheader("Diagnosis Results")
                if conditions:
                    for condition, explanation in zip(conditions, explanations):
                        st.write(f"**{condition}**: {explanation}")
                else:
                    st.write("No conditions diagnosed based on the provided parameters.")

                # Display the normal ranges for reference
                st.subheader("Normal Ranges for Parameters")
                st.table(normal_ranges)

                # Display the input parameters in a table
                st.subheader("Entered Health Parameters")
                st.table(params)
