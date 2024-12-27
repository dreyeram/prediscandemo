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
    results = [
        ("LDL", "200", "Hyperlipidemia", "LDL levels are elevated."),
        ("Mean Arterial Blood Pressure", "150", "Hypertension", "Mean arterial blood pressure is elevated."),
        ("eGFR", "98", "Normal", "eGFR levels are normal."),
        ("Fasting Glucose Level", "130", "Diabetes", "Fasting glucose level is elevated."),
        ("C-Reactive Protein (CRP)", "4.5", "Inflammation", "Elevated CRP levels indicate inflammation."),
        ("AST", "35", "Normal", "AST levels are within the normal range."),
        ("ALT", "40", "Normal", "ALT levels are within the normal range.")
    ]

    for result in results:
        st.write(f"**{result[0]}**: {result[1]} - {result[2]} - {result[3]}")
    
    if st.button("Back"):
        st.session_state.step = 2
