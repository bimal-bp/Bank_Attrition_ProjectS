import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt

# Load the pre-trained model
try:
    best_rf_model = pickle.load(open("xgb_model.pkl", "rb"))
except FileNotFoundError:
    best_rf_model = None
    st.error("Model file not found. Please ensure 'best_rf_model.pkl' exists.")
except Exception as e:
    best_rf_model = None
    st.error(f"Error loading model: {e}")

# Bank class to handle transactions
class Bank:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            return "Insufficient balance"
        self.balance -= amount
        return self.balance

    def check_balance(self):
        return self.balance

# Initialize session state
if 'feedback_list' not in st.session_state:
    st.session_state.feedback_list = []

if 'bank' not in st.session_state:
    st.session_state.bank = Bank(balance=0)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'user_type' not in st.session_state:
    st.session_state.user_type = ""

if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

# Home Page
def home_page():
    st.title("Welcome to Our Bank Service")
    st.header("Please log in")

    col1, col2 = st.columns(2)

    with col1:
        customer_username = st.text_input("Enter Customer Username", key="customer_username")
        customer_password = st.text_input("Enter Customer Password", type="password", key="customer_password")
        if st.button("Log In as Customer", key="customer_login"):
            if customer_username == "customer" and customer_password == "customer123":
                st.session_state.user_type = "Customer"
                st.session_state.logged_in = True
                st.session_state.user_name = "Customer"
            else:
                st.error("Incorrect username or password. Please try again.")

    with col2:
        employee_username = st.text_input("Enter Employee Username", key="employee_username")
        employee_password = st.text_input("Enter Employee Password", type="password", key="employee_password")
        if st.button("Log In as Employee", key="employee_login"):
            if employee_username == "admin" and employee_password == "admin123":
                st.session_state.user_type = "Employee"
                st.session_state.logged_in = True
                st.session_state.user_name = "Employee"
            else:
                st.error("Incorrect username or password. Please try again.")

# Employee Page Function
def employee_page():
    st.title("Employee Page")
    st.header("Welcome to the Employee Dashboard!")

    prediction_type = st.radio("Select Prediction Type", ["Single", "Group"], horizontal=True)

    if prediction_type == "Single":
        st.info("Provide Customer Details for Prediction")
        customer_age = st.number_input("Customer Age", min_value=18, max_value=100, value=30)
        credit_limit = st.number_input("Credit Limit", min_value=0, value=7000)
        total_transactions_count = st.number_input("Total Transactions Count", min_value=0, value=50)
        total_transaction_amount = st.number_input("Total Transaction Amount", min_value=0, value=5000)
        inactive_months_12_months = st.number_input("Inactive Months (12 Months)", min_value=0, max_value=12, value=2)
        transaction_count_change_q4_q1 = st.number_input("Transaction Count Change (Q4-Q1)", min_value=0.0, value=0.5)
        total_products_used = st.number_input("Total Products Used", min_value=1, value=2)
        average_credit_utilization = st.number_input("Average Credit Utilization", min_value=0.0, max_value=1.0, value=0.2)
        customer_contacts_12_months = st.number_input("Customer Contacts in 12 Months", min_value=0, value=1)
        transaction_amount_change_q4_q1 = st.number_input("Transaction Amount Change (Q4-Q1)", min_value=0.0, value=0.5)
        months_as_customer = st.number_input("Months as Customer", min_value=1, value=12)

        education = st.selectbox("Select Education Level", ["College", "Doctorate", "Graduate", "High School", "Post-Graduate", "Uneducated"])
        income = st.selectbox("Select Income Range", ["$120K +", "$40K - $60K", "$60K - $80K", "$80K - $120K", "Less than $40K"])

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

        if st.button("Predict for Single Customer"):
            try:
                prediction = best_rf_model.predict(input_df)
                prediction_prob = best_rf_model.predict_proba(input_df)
                st.success(f"Prediction: {prediction[0]}")
                st.info(f"Prediction Probability: {prediction_prob}")
            except Exception as e:
                st.error(f"Error during prediction: {e}")

    elif prediction_type == "Group":
        uploaded_file = st.file_uploader("Upload a CSV File for Group Prediction", type=["csv"])
        if uploaded_file:
            try:
                group_data = pd.read_csv(uploaded_file)
                st.write("Data Preview:")
                st.dataframe(group_data)
                
                if st.button("Predict for Group Customers"):
                    predictions = best_rf_model.predict(group_data)
                    prediction_probs = best_rf_model.predict_proba(group_data)
                    group_data["Prediction"] = predictions
                    group_data["Prediction_Probabilities"] = [list(prob) for prob in prediction_probs]
                    st.success("Predictions generated successfully!")
                    st.write("Prediction Results:")
                    st.dataframe(group_data)
                    
                    csv = group_data.to_csv(index=False).encode('utf-8')
                    st.download_button(label="Download Predictions as CSV", data=csv, file_name="predictions.csv")
            except Exception as e:
                st.error(f"Error during group prediction: {e}")

# Main
if st.session_state.logged_in:
    if st.session_state.user_type == "Customer":
        customer_page()
    elif st.session_state.user_type == "Employee":
        employee_page()
else:
    home_page()
