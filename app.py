import streamlit as st
import pandas as pd
import joblib
import random
from sklearn.preprocessing import StandardScaler

# Load the trained model
best_rf_model = joblib.load('best_rf_model.pkl')

# Customer feedback
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

# Function to display customer feedback
def display_feedback(prediction):
    if prediction == "Likely to Stay":
        feedback_to_show = random.sample(positive_feedback, 2) + random.sample(negative_feedback, 1)
        st.subheader("Customer Sentiment Insights (Stay Prediction)")
    else:
        feedback_to_show = random.sample(negative_feedback, 2) + random.sample(positive_feedback, 1)
        st.subheader("Customer Sentiment Insights (Churn Prediction)")

    st.markdown("### **Customer Feedback:**")
    for feedback in feedback_to_show:
        st.write(f"- {feedback}")

    # Display last feedback based on the prediction
    if prediction == "Likely to Stay":
        st.markdown("### **Last Feedback:**")
        st.write(f"- {positive_feedback[-1]}")
    else:
        st.markdown("### **Last Feedback:**")
        st.write(f"- {negative_feedback[-1]}")

# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "account_type" not in st.session_state:
    st.session_state.account_type = ""

# Function for input preprocessing
def preprocess_inputs(input_df):
    scaler = StandardScaler()  # Assume the same scaler from training was saved
    scaled_data = scaler.fit_transform(input_df)
    return scaled_data

# Simplified Login Page
def login_page():
    st.markdown("<h1 style='text-align: center;'>Customer <span style='color: red;'>Attrition</span> - Login</h1>", unsafe_allow_html=True)
    user_name = st.text_input("Enter your name:")
    account_type = st.selectbox("Select Account Type:", ["Saving", "Current"])

    login_button = st.button("Log In")

    if login_button:
        if user_name.strip():
            st.session_state.logged_in = True
            st.session_state.user_name = user_name.strip()
            st.session_state.account_type = account_type
            st.experimental_rerun()
        else:
            st.error("Please enter your name.")

# Main App Page
def main_page():
    st.title(f"Customer Attrition Prediction")
    st.sidebar.header(f"Welcome, {st.session_state.user_name} ({st.session_state.account_type} Account)")

    # Sidebar Inputs
    st.sidebar.header('Input Data')
    customer_age = st.sidebar.number_input("Customer Age", min_value=18, max_value=100, value=30)
    credit_limit = st.sidebar.number_input("Credit Limit", min_value=0, value=7000)
    total_transactions_count = st.sidebar.number_input("Total Transactions Count", min_value=0, value=50)
    total_transaction_amount = st.sidebar.number_input("Total Transaction Amount", min_value=0, value=5000)
    inactive_months_12_months = st.sidebar.number_input("Inactive Months (12 Months)", min_value=0, max_value=12, value=2)
    transaction_count_change_q4_q1 = st.sidebar.number_input("Transaction Count Change (Q4-Q1)", min_value=0.0, value=0.5)
    total_products_used = st.sidebar.number_input("Total Products Used", min_value=1, value=2)
    average_credit_utilization = st.sidebar.number_input("Average Credit Utilization", min_value=0.0, max_value=1.0, value=0.2)
    customer_contacts_12_months = st.sidebar.number_input("Customer Contacts in 12 Months", min_value=0, value=1)
    transaction_amount_change_q4_q1 = st.sidebar.number_input("Transaction Amount Change (Q4-Q1)", min_value=0.0, value=0.5)
    months_as_customer = st.sidebar.number_input("Months as Customer", min_value=1, value=12)

    # Map education and income to one-hot encoded features
    input_data = {
        "Customer_Age": [customer_age],
        "Credit_Limit": [credit_limit],
        "Total_Transactions_Count": [total_transactions_count],
        "Total_Transaction_Amount": [total_transaction_amount],
        "Inactive_Months_12_Months": [inactive_months_12_months],
        "Transaction_Count_Change_Q4_Q1": [transaction_count_change_q4_q1],
        "Total_Products_Used": [total_products_used],
        "Average_Credit_Utilization": [average_credit_utilization],
        "Customer_Contacts_12_Months": [customer_contacts_12_months],
        "Transaction_Amount_Change_Q4_Q1": [transaction_amount_change_q4_q1],
        "Months_as_Customer": [months_as_customer],
    }

    input_df = pd.DataFrame(input_data)

    # Prediction
    if st.sidebar.button("Predict"):
        prediction = best_rf_model.predict(input_df)

        if prediction[0] == 1:
            display_feedback("Likely to Stay")
        else:
            display_feedback("Likely to Churn")

# Run the app
if not st.session_state.logged_in:
    login_page()
else:
    main_page()
