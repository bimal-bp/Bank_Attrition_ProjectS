import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt

# Load the pre-trained model
try:
    best_rf_model = pickle.load(open("best_rf_model.pkl", "rb"))
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

# Initialize session state for feedback list and bank balance
if 'feedback_list' not in st.session_state:
    st.session_state.feedback_list = []

if 'bank' not in st.session_state:
    st.session_state.bank = Bank(balance=0)

# Initialize session state for login and user type
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

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
        if st.button("Log In as Customer"):
            if customer_username == "customer" and customer_password == "customer123":
                st.session_state.user_type = "Customer"
                st.session_state.prediction_type = "Single"  # Default prediction type for customer
                st.session_state.logged_in = True
                st.session_state.user_name = "Customer"
            else:
                st.error("Incorrect username or password. Please try again.")

    with col2:
        employee_username = st.text_input("Enter Employee Username", key="employee_username")
        employee_password = st.text_input("Enter Employee Password", type="password", key="employee_password")
        if st.button("Log In as Employee"):
            if employee_username == "admin" and employee_password == "admin123":
                st.session_state.user_type = "Employee"
                st.session_state.prediction_type = "Single"  # Default prediction type for employee
                st.session_state.logged_in = True
                st.session_state.user_name = "Employee"
            else:
                st.error("Incorrect username or password. Please try again.")

# Customer Page
def customer_page():
    st.title("Customer Page")
    st.header("Welcome to Your Bank Account!")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Transactions"):
            transaction_section()
    with col2:
        if st.button("Submit Feedback"):
            feedback_section()

# Transaction Section
def transaction_section():
    st.title("Transactions")
    action = st.selectbox("Select Action", ["Deposit", "Withdraw", "Check Balance"])

    if action == "Deposit":
        amount = st.number_input("Enter amount to deposit", min_value=1)
        if st.button("Deposit"):
            balance = st.session_state.bank.deposit(amount)
            st.success(f"Deposit successful. New Balance: {balance}")

    elif action == "Withdraw":
        amount = st.number_input("Enter amount to withdraw", min_value=1)
        if st.button("Withdraw"):
            result = st.session_state.bank.withdraw(amount)
            if isinstance(result, str):
                st.error(result)
            else:
                st.success(f"Withdrawal successful. New Balance: {result}")

    elif action == "Check Balance":
        balance = st.session_state.bank.check_balance()
        st.info(f"Your current balance is: {balance}")

# Feedback Section
def feedback_section():
    st.title("Submit Feedback")
    name = st.text_input("Enter your name")
    feedback = st.text_area("Write your feedback here")
    rating = st.radio("Rate your experience (1 to 5)", [1, 2, 3, 4, 5])

    if st.button("Submit Feedback", key="submit_feedback"):
        if name and feedback:
            st.session_state.feedback_list.append((name, feedback, rating))
            st.success(f"Feedback submitted successfully! Rating: {rating}/5")
            st.info("Thank you for your feedback! We will work on it.")
        else:
            st.error("Please provide your name and feedback.")

