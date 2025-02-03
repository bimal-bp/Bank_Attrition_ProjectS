import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load your trained model
best_rf_model = joblib.load('best_rf_model.pkl')  # Adjust path as necessary

# Function to display feedback based on prediction
def display_feedback(prediction):
    if prediction == 1:
        st.write("This customer is likely to attrit.")
    else:
        st.write("This customer is unlikely to attrit.")

# Prediction for a single customer
def predict_customer(input_df):
    # Extract relevant values from input_df
    inactive_months_12_months = input_df['Inactive_Months_12_Months'][0]
    transaction_amount_change_q4_q1 = input_df['Transaction_Amount_Change_Q4_Q1'][0]
    total_products_used = input_df['Total_Products_Used'][0]
    total_transactions_count = input_df['Total_Transactions_Count'][0]
    average_credit_utilization = input_df['Average_Credit_Utilization'][0]
    customer_contacts_12_months = input_df['Customer_Contacts_12_Months'][0]
    
    # Predict using the trained model
    prediction = best_rf_model.predict(input_df)
    
    if prediction[0] == 1:
        st.markdown(f"### Prediction: Customer is likely to attrit ✅")
        st.subheader("Attrition Risk Insights:")
    else:
        st.markdown(f"### Prediction: Customer is unlikely to attrit ❌")
        st.subheader("Non-Attrition Insights:")
    
    st.write(f"- Inactive Months (12 months): {inactive_months_12_months} months")
    st.write(f"- Transaction Amount Change (Q4-Q1): {transaction_amount_change_q4_q1}")
    st.write(f"- Total Products Used: {total_products_used}")
    st.write(f"- Total Transactions Count: {total_transactions_count}")
    st.write(f"- Average Credit Utilization: {average_credit_utilization}")
    st.write(f"- Customer Contacts in 12 Months: {customer_contacts_12_months}")
    
    display_feedback(prediction[0])  # Pass prediction to display feedback function

# File Upload and Processing for Group Prediction with Pie Chart
def process_uploaded_file(uploaded_file):
    df = pd.read_csv(uploaded_file)
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

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"Missing required columns: {', '.join(missing_columns)}")
        return None

    df = df[required_columns]
    predictions = best_rf_model.predict(df)

    attrit_count = sum(predictions)
    stay_count = len(predictions) - attrit_count

    # Plot Pie Chart with Styling
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie([stay_count, attrit_count], labels=["Stay", "Attrit"], autopct='%1.1f%%', colors=["lightgreen", "lightcoral"],
           startangle=90, wedgeprops={"edgecolor": "black", "linewidth": 1.5, "linestyle": "solid"})
    ax.set_title("Customer Attrition Distribution", fontsize=14, fontweight="bold", color="darkblue")
    st.pyplot(fig)

    for idx, prediction in enumerate(predictions):
        st.write(f"Customer {idx + 1} Prediction: {'Attrit' if prediction == 1 else 'Stay'}")
        display_feedback(prediction)

# Login Page Functionality
def login_page():
    # Initialize session state if not already set
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False  # Default to not logged in
    
    if not st.session_state.logged_in:
        # Logic for showing login form
        user_name = st.text_input("Enter Username")
        password = st.text_input("Enter Password", type='password')

        if st.button("Login"):
            # Check if username and password are correct
            if user_name == 'admin' and password == 'password':  # Replace with your actual logic
                st.session_state.logged_in = True
                st.experimental_rerun()  # This reruns the app after login
            else:
                st.error("Invalid credentials")
    else:
        # After login is successful, show main page
        main_page()

# Main App Page
def main_page():
    st.title("Customer Attrition Prediction")
    st.sidebar.header(f"Welcome, {st.session_state.user_name}")

    st.sidebar.header('Prediction Type: ' + st.session_state.prediction_type)
    if st.session_state.prediction_type == "Single":
        # Individual customer input fields
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
            "Less than $40K": [1 if income == "Less than $40K" else 0]
        }

        input_df = pd.DataFrame(input_data)
        predict_customer(input_df)

    else:  # For Group Prediction
        uploaded_file = st.sidebar.file_uploader("Upload CSV file for Group Prediction", type=["csv"])
        if uploaded_file is not None:
            process_uploaded_file(uploaded_file)

# Main logic to check session state and render login or main page
if 'logged_in' in st.session_state and st.session_state.logged_in:
    main_page()
else:
    login_page()
