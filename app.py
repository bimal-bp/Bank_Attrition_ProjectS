import streamlit as st
import pandas as pd
import joblib  # For loading the trained model

# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "prediction_type" not in st.session_state:
    st.session_state.prediction_type = "Single"

# Load the trained model
@st.cache_resource
def load_model():
    return joblib.load("best_rf_model.pkl")  # Replace with your model file

model = load_model()

# Function for login page
def login_page():
    st.title("🔐 User Login")
    
    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")
    
    if st.button("Login"):
        if username == "admin" and password == "password123":  # Replace with actual authentication logic
            st.session_state.logged_in = True
            st.session_state.user_name = username
            st.success("✅ Login successful! Redirecting...")
            st.experimental_rerun()  # Refresh the app
        else:
            st.error("❌ Invalid username or password.")

# Function for single prediction
def single_prediction():
    st.subheader("🔍 Single Customer Prediction")

    age = st.number_input("Age", min_value=18, max_value=100, step=1)
    income = st.number_input("Annual Income ($)", min_value=1000, step=1000)
    credit_score = st.number_input("Credit Score", min_value=300, max_value=850, step=1)
    num_products = st.slider("Number of Products", 1, 5, 1)
    active_member = st.radio("Active Member", ["Yes", "No"])

    active_member = 1 if active_member == "Yes" else 0

    if st.button("Predict"):
        input_data = pd.DataFrame([[age, income, credit_score, num_products, active_member]], 
                                  columns=["Age", "Income", "CreditScore", "NumOfProducts", "IsActiveMember"])
        
        prediction = model.predict(input_data)[0]

        if prediction == 1:
            st.error("⚠️ Customer is likely to churn!")
        else:
            st.success("✅ Customer is likely to stay.")

# Function for batch prediction
def batch_prediction():
    st.subheader("📂 Batch Prediction")

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("📊 Uploaded Data Preview:", df.head())

        if st.button("Predict for Batch"):
            predictions = model.predict(df)
            df["Attrition Prediction"] = ["Churn" if p == 1 else "Stay" for p in predictions]
            st.write("🔍 Prediction Results:")
            st.dataframe(df)

            # Allow user to download the predictions
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download Predictions", csv, "predictions.csv", "text/csv")

# Function for the main page
def main_page():
    st.title("🏦 Bank Attrition Prediction App")
    st.write(f"👋 Welcome, {st.session_state.user_name}!")

    # Logout button
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user_name = ""
        st.experimental_rerun()

    # Prediction type selection
    st.session_state.prediction_type = st.radio("Select Prediction Type", ("Single", "Batch"))

    if st.session_state.prediction_type == "Single":
        single_prediction()
    else:
        batch_prediction()

# Routing based on login status
if st.session_state.logged_in:
    main_page()
else:
    login_page()
