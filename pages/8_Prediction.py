from __future__ import annotations

import streamlit as st

from modules.prediction import predict_patient

st.set_page_config(page_title="Prediction", layout="wide")

st.title("Diabetes Prediction")
st.markdown("This application is for academic demonstration and is not a medical diagnostic tool.")

with st.form("prediction_form"):
    pregnancies = st.number_input("Number of pregnancies", min_value=0, max_value=20, value=1)
    glucose = st.number_input("Glucose level", min_value=0.0, max_value=300.0, value=120.0)
    blood_pressure = st.number_input("Blood pressure", min_value=0.0, max_value=200.0, value=70.0)
    skin_thickness = st.number_input("Skin thickness", min_value=0.0, max_value=100.0, value=20.0)
    insulin = st.number_input("Insulin", min_value=0.0, max_value=1000.0, value=80.0)
    bmi = st.number_input("BMI", min_value=0.0, max_value=100.0, value=30.0)
    pedigree = st.number_input("Diabetes pedigree function", min_value=0.0, max_value=3.0, value=0.5, step=0.01)
    age = st.number_input("Age", min_value=1, max_value=100, value=35)
    submitted = st.form_submit_button("Predict diabetes risk")

if submitted:
    payload = {
        "Pregnancies": pregnancies,
        "Glucose": glucose,
        "BloodPressure": blood_pressure,
        "SkinThickness": skin_thickness,
        "Insulin": insulin,
        "BMI": bmi,
        "DiabetesPedigreeFunction": pedigree,
        "Age": age,
    }
    result = predict_patient(payload)

    st.subheader("Prediction results")
    col1, col2 = st.columns(2)
    col1.metric("Logistic Regression", "Diabetic" if result["logistic_regression"]["prediction"] == 1 else "Non-Diabetic")
    col2.metric("Random Forest", "Diabetic" if result["random_forest"]["prediction"] == 1 else "Non-Diabetic")
    st.write("Logistic regression probability:", round(result["logistic_regression"]["probability"], 4))
    st.write("Random forest probability:", round(result["random_forest"]["probability"], 4))

    st.subheader("Input summary")
    st.json(payload)

    st.warning(
        "This application is an academic data mining project and is not a medical diagnostic tool. Predictions are based on the training dataset and should not replace professional medical advice."
    )
