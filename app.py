import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt

# Load the pre-trained model
try:
    with open("best_rf_model.pkl", "rb") as file:
        best_rf_model = pickle.load(file)
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
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'prediction_type' not in st.session_state:
    st.session_state.prediction_type = "Single"  # Default prediction type

# Home Page (Login)
def home_page():
    st.title("Welcome to Our Bank Service")
    st.header("Please log in")

    col1, col2 = st.columns(2)

    with col1:
        customer_username = st.text_input("Enter Customer Username")
        customer_password = st.text_input("Enter Customer Password", type="password")
        if st.button("Log In as Customer"):
            if customer_username == "customer" and customer_password == "customer123":
                st.session_state.user_type = "Customer"
                st.session_state.user_name = customer_username # Store username
            else:
                st.error("Incorrect username or password. Please try again.")

    with col2:
        employee_username = st.text_input("Enter Employee Username")
        employee_password = st.text_input("Enter Employee Password", type="password")
        if st.button("Log In as Employee"):
            if employee_username == "admin" and employee_password == "admin123":
                st.session_state.user_type = "Employee"
                st.session_state.user_name = employee_username # Store username
            else:
                st.error("Incorrect username or password. Please try again.")

# Customer Page
def customer_page():
    st.title("Customer Page")
    st.header("Welcome to Your Bank Account!")

    if st.button("Transactions"):
        st.session_state.page = "transactions"
    if st.button("Submit Feedback"):
        st.session_state.page = "feedback"

    if st.session_state.get("page") == "transactions":
        transaction_section()
    elif st.session_state.get("page") == "feedback":
        feedback_section()

# ... (transaction_section and feedback_section - same as before)

# Employee Page
def employee_page():
    st.title("Employee Page")
    st.header("Welcome to the Employee Dashboard!")

    st.write("### Customer Retention Prediction")
    st.session_state.prediction_type = st.selectbox("Select Prediction Type", ["Single", "Group"])

    if st.session_state.prediction_type == "Single":
        single_prediction_section()
    elif st.session_state.prediction_type == "Group":
        group_prediction_section()

def single_prediction_section():
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

    if st.sidebar.button("Predict"):
        predict_customer(input_df)


def group_prediction_section():
    uploaded_file = st.sidebar.file_uploader("Upload a CSV File for Group Prediction", type=["csv"])
    if uploaded_file:
        process_uploaded_file(uploaded_file)

# ... (predict_customer and process_uploaded_file - same as before)

# Main App Page
def main_page():
    if st.session_state.user_type is None:  # Check if user is logged in
        home_page()
        return

    if st.session_state.user_type == "Customer":
