import streamlit as st
import random
from PIL import Image

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

# Step 3: Display the report
if st.session_state.step == 3:
    st.write("Step 3: Report")
    patient_details = {
        "Patient ID": st.session_state.patient_id,
        "Patient Name": st.session_state.patient_name,
        "Age": st.session_state.age,
        "Gender": st.session_state.gender,
        "Alcoholic Status": st.session_state.alcohol_status,
        "Smoking Status": st.session_state.smoking_status,
        "Medical History": st.session_state.medical_history,
        "Family Medical History": st.session_state.family_history
    }

    # Display the entered patient details in a table
    st.subheader("Entered Patient Details")
    st.table(patient_details)

    # Placeholder for health parameters and evaluation
    st.session_state.health_params = {
        "Age": st.session_state.age,
        "Gender": st.session_state.gender,
        "BMI": 25,  # Placeholder value
        "Smoking Status": st.session_state.smoking_status,
        "Alcohol Consumption": st.session_state.alcohol_status,
        "Blood Pressure": 120,  # Placeholder value
        "Fasting Blood Sugar": 90,  # Placeholder value
        "LDL-C": 100,  # Placeholder value
        "hs-CRP": 1,  # Placeholder value
        "eGFR": 90,  # Placeholder value
        "ALT": 30,  # Placeholder value
        "AST": 20  # Placeholder value
    }
    params = st.session_state.health_params

    # Placeholder function for condition evaluation
    def evaluate_conditions(params):
        # Dummy evaluation logic
        conditions = ["Condition A", "Condition B"]
        explanations = ["Explanation for Condition A", "Explanation for Condition B"]
        return conditions, explanations

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
    normal_ranges = {
        "Parameter": ["Age", "BMI", "Blood Pressure", "Fasting Blood Sugar", "LDL-C", "hs-CRP", "eGFR", "ALT", "AST"],
        "Normal Range": ["0-120", "18.5-24.9", "90-120", "70-99", "0-100", "0-3", ">90", "0-40", "0-40"]
    }
    st.subheader("Normal Ranges for Parameters")
    st.table(normal_ranges)

    # Display the input parameters in a table
    st.subheader("Entered Health Parameters")
    st.table(params)
    
    if st.button("Back"):
        st.session_state.step = 2
