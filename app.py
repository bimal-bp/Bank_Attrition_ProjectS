import random
import streamlit as st
import pandas as pd
import joblib

# Load the trained model
best_rf_model = joblib.load('best_rf_model.pkl')

# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "account_type" not in st.session_state:
    st.session_state.account_type = ""
if "email" not in st.session_state:
    st.session_state.email = ""

# Login Page
def login_page():
    st.markdown("<h1 style='text-align: center;'>Customer <span style='color: red;'>Attrition </span> - Login</h1>", unsafe_allow_html=True)
    
    # User Name
    user_name = st.text_input("Enter your name:")
    
    # Account Type: Saving or Current
    account_type = st.selectbox("Select Account Type", ["Saving", "Current"])
    
    # Email Address (optional)
    email = st.text_input("Enter your email (optional):")
    
    login_button = st.button("Log In")

    if login_button:
        if user_name.strip():
            # Store additional information in session state
            st.session_state.logged_in = True
            st.session_state.user_name = user_name.strip()
            st.session_state.account_type = account_type
            st.session_state.email = email.strip()
            st.experimental_rerun()  # Refresh to show main page
        else:
            st.error("Name cannot be empty.")

# Customer Feedback Data
positive_feedback = [
    "Excellent customer service and great support!",
    "I'm extremely satisfied with the features offered.",
    "The app is user-friendly and intuitive.",
    "Timely communication from the service team.",
    "Reliable and secure platform for transactions.",
    "Quick response to queries and issues.",
    "Very happy with the product offerings.",
    "Affordable plans and great discounts.",
    "Highly recommended for smooth operations.",
    "A pleasant experience using the service."
]

negative_feedback = [
    "Customer service response is too slow.",
    "The platform crashes frequently.",
    "Hidden charges are frustrating.",
    "Difficult to navigate the website.",
    "Long waiting times for support.",
    "Billing issues need to be resolved.",
    "Product availability is limited.",
    "Lack of proper communication channels.",
    "Refunds take too long to process.",
    "Not enough transparency in pricing."
]

def display_feedback(prediction):
    if prediction == 1:  # Customer likely to attrit (Churn)
        feedback_to_show = random.sample(negative_feedback, 3) + random.sample(positive_feedback, 1)
        st.subheader("Customer Sentiment Insights (Churn Prediction)")
    else:  # Customer unlikely to attrit (Stay)
        feedback_to_show = random.sample(positive_feedback, 3) + random.sample(negative_feedback, 1)
        st.subheader("Customer Sentiment Insights (Stay Prediction)")

    st.markdown("### **Customer Feedback:**")
    for feedback in feedback_to_show:
        st.write(f"- {feedback}")

# File Upload and Processing
def process_uploaded_file(uploaded_file):
    # Read the uploaded file into a pandas DataFrame
    df = pd.read_csv(uploaded_file)

    # Ensure required columns are in the file
    required_columns = [
        'Customer_Age', 'Credit_Limit', 'Total_Transactions_Count',
        'Total_Transaction_Amount', 'Inactive_Months_12_Months',
        'Transaction_Count_Change_Q4_Q1', 'Total_Products_Used',
        'Average_Credit_Utilization', 'Customer_Contacts_12_Months',
        'Transaction_Amount_Change_Q4_Q1', 'Months_as_Customer',
        'College', 'Doctorate', 'Graduate', 'High School', 'Post-Graduate',
        'Uneducated', '$120K +', '$40K - $60K', '$60K - $80K', '$80K - $120K',
        'Less than $40K'
    ]

    # Check for missing columns
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"Missing required columns: {', '.join(missing_columns)}")
        return None

    # Drop any irrelevant columns (e.g., 'Churn_Flag' if it's not part of the input)
    df = df[required_columns]

    # Make predictions
    predictions = best_rf_model.predict(df)

    # Show predictions for each customer
    for idx, prediction in enumerate(predictions):
        st.write(f"Customer {idx + 1} Prediction: {'Attrit' if prediction == 1 else 'Stay'}")
        display_feedback(prediction)

# Main App Page
def main_page():
    st.title("Customer Attrition Prediction")
    st.sidebar.header(f"Welcome, {st.session_state.user_name}")

    # Sidebar Inputs
    st.sidebar.header('Input Data')
    uploaded_file = st.sidebar.file_uploader("Upload a CSV file with customer data", type=["csv"])

    if uploaded_file:
        process_uploaded_file(uploaded_file)

# App Navigation
if not st.session_state.logged_in:
    login_page()
else:
    main_page()
