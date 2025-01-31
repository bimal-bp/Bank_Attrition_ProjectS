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
if "prediction" not in st.session_state:
    st.session_state.prediction = None

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
    if prediction == 1:  # Customer likely to attrit
        feedback_to_show = random.sample(positive_feedback, 2) + random.sample(negative_feedback, 1)
        st.subheader("Customer Sentiment Insights (Churn Prediction)")
    else:  # Customer unlikely to attrit
        feedback_to_show = random.sample(negative_feedback, 2) + random.sample(positive_feedback, 1)
        st.subheader("Customer Sentiment Insights (Stay Prediction)")

    st.markdown("### **Customer Feedback:**")
    for feedback in feedback_to_show:
        st.write(f"- {feedback}")

# Main App Page
def main_page():
    st.title("Customer Attrition Prediction")
    st.sidebar.header(f"Welcome, {st.session_state.user_name}")

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

    # Education and Income Dropdowns
    education = st.sidebar.selectbox("Select Education Level", ["College", "Doctorate", "Graduate", "High School", "Post-Graduate", "Uneducated"])
    income = st.sidebar.selectbox("Select Income Range", ["$120K +", "$40K - $60K", "$60K - $80K", "$80K - $120K", "Less than $40K"])

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
        "College": [1 if education == "College" else 0],
        "Doctorate": [1 if education == "Doctorate" else 0],
        "Graduate": [1 if education == "Graduate" else 0],
        "High School": [1 if education == "High School" else 0],
        "Post-Graduate": [1 if education == "Post-Graduate" else 0],
        "Uneducated": [1 if education == "Uneducated" else 0],
        "$120K +": [1 if income == "$120K +" else 0],
        "$40K - $60K": [1 if income == "$40K - $60K" else 0],
        "$60K - $80K": [1 if income == "$60K - $80K" else 0],
        "$80K - $120K": [1 if income == "$80K - $120K" else 0],
        "Less than $40K": [1 if income == "Less than $40K" else 0],
    }

    input_df = pd.DataFrame(input_data)

    # Prediction
    if st.sidebar.button("Predict"):
        prediction = best_rf_model.predict(input_df)

        if prediction[0] == 1:
            st.markdown(f"### Prediction: Customer is likely to attrit ✅")
            st.write("Customer will leave.")
            st.subheader("Attrition Risk Insights:")
            st.write(f"- *Inactive Months (12 months):* {inactive_months_12_months} months")
            st.write(f"- *Transaction Amount Change (Q4-Q1):* {transaction_amount_change_q4_q1}")
            st.write(f"- *Total Products Used:* {total_products_used}")
            st.write(f"- *Total Transactions Count:* {total_transactions_count}")
            st.write(f"- *Average Credit Utilization:* {average_credit_utilization}")
            st.write(f"- *Customer Contacts in 12 Months:* {customer_contacts_12_months}")
            st.session_state.prediction = 1
        else:
            st.markdown(f"### Prediction: Customer is unlikely to attrit ❌")
            st.write("Customer will stay.")
            st.subheader("Non-Attrition Insights:")
            st.session_state.prediction = 0

        # Button to Navigate to Customer Feedback Page (Placed below prediction)
        if st.button("See Customer Feedback Insights"):
            display_feedback(st.session_state.prediction)

# App Navigation
if not st.session_state.logged_in:
    login_page()
else:
    main_page()
