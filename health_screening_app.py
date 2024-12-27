import streamlit as st
import random
from PIL import Image
import pandas as pd

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
demo_image = load_image("Demo.png")

st.sidebar.image(logo_image, use_container_width=True)
st.sidebar.markdown("<br>", unsafe_allow_html=True)  # Add spacing

col1, col2 = st.sidebar.columns([1, 1])
with col1:
    home_clicked = st.button("Home", key="home")
with col2:
    add_record_clicked = st.button("Add New Record", key="add_record")

st.sidebar.markdown("<br>", unsafe_allow_html=True)  # Add spacing

if right_fundus_image and left_fundus_image:
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.image(right_fundus_image, caption="Right Fundus Image", use_column_width=True)
    with col2:
        st.image(left_fundus_image, caption="Left Fundus Image", use_column_width=True)

st.sidebar.markdown("<br>", unsafe_allow_html=True)  # Add spacing
st.sidebar.write("This is a demo app, purely for demonstration purposes, not for any type of medical, clinical, or research use.")

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1

# Home button functionality
if home_clicked:
    st.session_state.step = "home"

# Add New Record button functionality
if add_record_clicked:
    st.session_state.step = 1

# Home page content
if st.session_state.step == "home":
    if demo_image:
        st.image(demo_image, caption="Demo", use_column_width=True)
    st.write("**About Us**")
    st.write("""
    Prediscan - AI-based cloud medical diagnostic software utilizes simple eye scans to non-invasively detect early signs of non-communicable and chronic diseases.
    
    We are leveraging our AI diagnostic solutions to enhance the value of retinal scans, serving as a gateway to preventive healthcare.
    
    Save billions of lives by non-invasively detecting diseases at their earliest stages.
    """)

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
        {"Parameter": "LDL", "Value": "200", "Diagnosis": "Hyperlipidemia", "Explanation": "LDL levels are elevated."},
        {"Parameter": "Mean Arterial Blood Pressure", "Value": "150", "Diagnosis": "Hypertension", "Explanation": "Mean arterial blood pressure is elevated."},
        {"Parameter": "eGFR", "Value": "98", "Diagnosis": "Normal", "Explanation": "eGFR levels are normal."},
        {"Parameter": "Fasting Glucose Level", "Value": "130", "Diagnosis": "Diabetes", "Explanation": "Fasting glucose level is elevated."},
        {"Parameter": "C-Reactive Protein (CRP)", "Value": "4.5", "Diagnosis": "Inflammation", "Explanation": "Elevated CRP levels indicate inflammation."},
        {"Parameter": "AST", "Value": "35", "Diagnosis": "Normal", "Explanation": "AST levels are within the normal range."},
        {"Parameter": "ALT", "Value": "40", "Diagnosis": "Normal", "Explanation": "ALT levels are within the normal range."}
    ]

    df_results = pd.DataFrame(results)
    st.table(df_results)
    
    if st.button("Back"):
        st.session_state.step = 2
