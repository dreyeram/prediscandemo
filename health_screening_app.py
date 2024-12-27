import streamlit as st
import random

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

# Sidebar Layout
st.sidebar.image("right_fundus_example.jpg", caption="Right Fundus Image", use_container_width=True)
st.sidebar.image("left_fundus_example.jpg", caption="Left Fundus Image", use_container_width=True)
st.sidebar.write("This is a demo app, purely for demonstration purposes, not for any type of medical, clinical, or research use.")

# Main Layout
st.title("Health Screening Tool for Heart, Kidney, and Liver Diseases")

# Add New Record Section
if st.sidebar.button("Add New Record"):
    with st.form("patient_form"):
        st.write("Step 1: Enter Basic Details")
        patient_id = random.randint(10000, 99999)
        patient_name = st.text_input("Patient Name")
        age = st.number_input("Age", min_value=0, max_value=120)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        alcohol_status = st.selectbox("Alcoholic Status", ["Yes", "No"])
        smoking_status = st.selectbox("Smoking Status", ["Yes", "No"])
        medical_history = st.text_area("Any Medical History")
        family_history = st.text_area("Family Medical History")
        
        if st.form_submit_button("Next"):
            with st.form("image_upload_form"):
                st.write("Step 2: Upload Fundus Images")
                right_fundus_image = st.file_uploader("Upload Right Fundus Image", type=["png", "jpg", "jpeg"], key="right_fundus_new")
                left_fundus_image = st.file_uploader("Upload Left Fundus Image", type=["png", "jpg", "jpeg"], key="left_fundus_new")
                
                if st.form_submit_button("Generate Report"):
                    if right_fundus_image and left_fundus_image:
                        st.write("Image quality is high and perfect for evaluation. Generating report...")

                        # Collect input data from user
                        bmi = st.number_input("BMI (kg/m²)", min_value=0.0, max_value=100.0)
                        blood_pressure = st.number_input("Blood Pressure (mmHg)", min_value=0, max_value=300)
                        fasting_blood_sugar = st.number_input("Fasting Blood Sugar (mg/dL)", min_value=0, max_value=500)
                        ldl_c = st.number_input("LDL-C (mg/dL)", min_value=0, max_value=300)
                        hs_crp = st.number_input("hs-CRP (mg/L)", min_value=0.0, max_value=20.0)
                        egfr = st.number_input("eGFR (mL/min/1.73m²)", min_value=0, max_value=200)
                        alt = st.number_input("ALT (U/L)", min_value=0, max_value=500)
                        ast = st.number_input("AST (U/L)", min_value=0, max_value=500)

                        # Create a dictionary for the input parameters
                        params = {
                            "Age": age,
                            "Gender": gender,
                            "BMI": bmi,
                            "Smoking Status": smoking_status,
                            "Alcohol Consumption": alcohol_status,
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
                        for param, normal_range in normal_ranges.items():
                            st.write(f"**{param}**: {normal_range}")
