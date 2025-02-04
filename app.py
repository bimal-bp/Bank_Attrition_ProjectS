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
# Employee Page
def employee_page():
    st.title("Employee Page")
    st.header("Welcome to the Employee Dashboard!")
    st.write("### Customer Retention Prediction")
    prediction_type = st.selectbox("Select Prediction Type", ["Single", "Group"])
    st.session_state.prediction_type = prediction_type

# Single customer prediction
def predict_single_customer(data):
    if best_rf_model is None:
        st.error("Model not loaded. Cannot make predictions.")
        return
    try:
        prediction = best_rf_model.predict(data)
        result_text = "Customer is likely to attrit ✅" if prediction[0] == 1 else "Customer is unlikely to attrit ❌"
        st.markdown(f"### Prediction: {result_text}")
    except Exception as e:
        st.error(f"Prediction error: {e}")

# Group customer prediction
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
        return

    try:
        predictions = best_rf_model.predict(df)
        attrit_count = sum(predictions)
        stay_count = len(predictions) - attrit_count

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie([stay_count, attrit_count], labels=["Stay", "Attrit"], autopct='%1.1f%%', colors=["lightgreen", "lightcoral"],
               startangle=90, wedgeprops={"edgecolor": "black", "linewidth": 1.5, "linestyle": "solid"})
        ax.set_title("Customer Attrition Distribution", fontsize=14, fontweight="bold", color="darkblue")
        st.pyplot(fig)

        for idx, prediction in enumerate(predictions):
            st.write(f"Customer {idx + 1} Prediction: {'Attrit' if prediction == 1 else 'Stay'}")
    except Exception as e:
        st.error(f"Prediction error: {e}")

# Main app function
def main_page():
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.error("Please log in first.")
        return

    st.title("Customer Attrition Prediction")
    st.sidebar.header(f"Welcome, {st.session_state.user_name}")

    prediction_type = st.selectbox("Select Prediction Type", ["Single", "Group"])

    if prediction_type == "Single":
        st.write("### Enter Customer Details")
        customer_age = st.number_input("Customer Age", min_value=18, max_value=100, value=30)
        credit_limit = st.number_input("Credit Limit", min_value=0.0, value=5000.0)
        transactions_count = st.number_input("Total Transactions Count", min_value=0, value=10)
        transaction_amount = st.number_input("Total Transaction Amount", min_value=0.0, value=1000.0)
        inactive_months = st.number_input("Inactive Months (Last 12 Months)", min_value=0, value=2)
        transaction_change = st.number_input("Transaction Count Change Q4 to Q1", value=0.5)
        products_used = st.number_input("Total Products Used", min_value=1, value=2)
        avg_credit_utilization = st.number_input("Average Credit Utilization", value=0.3)
        customer_contacts = st.number_input("Customer Contacts (Last 12 Months)", min_value=0, value=1)
        transaction_amount_change = st.number_input("Transaction Amount Change Q4 to Q1", value=0.2)
        months_as_customer = st.number_input("Months as Customer", min_value=1, value=36)

        # Education Level Selection
        education_level = st.selectbox("Education Level", ['Uneducated', 'High School', 'College', 'Graduate', 'Post-Graduate', 'Doctorate'])
        salary_range = st.selectbox("Salary Range", ['$120K +', '$40K - $60K', '$60K - $80K', '$80K - $120K', 'Less than $40K'])

        # One-hot encoding for education and salary
        education_columns = ['College', 'Doctorate', 'Graduate', 'High School', 'Post-Graduate', 'Uneducated']
        salary_columns = ['$120K +', '$40K - $60K', '$60K - $80K', '$80K - $120K', 'Less than $40K']
        
        education_data = [1 if level == education_level else 0 for level in education_columns]
        salary_data = [1 if salary == salary_range else 0 for salary in salary_columns]

        # Create input data
        input_data = pd.DataFrame({
            'Customer_Age': [customer_age],
            'Credit_Limit': [credit_limit],
            'Total_Transactions_Count': [transactions_count],
            'Total_Transaction_Amount': [transaction_amount],
            'Inactive_Months_12_Months': [inactive_months],
            'Transaction_Count_Change_Q4_Q1': [transaction_change],
            'Total_Products_Used': [products_used],
            'Average_Credit_Utilization': [avg_credit_utilization],
            'Customer_Contacts_12_Months': [customer_contacts],
            'Transaction_Amount_Change_Q4_Q1': [transaction_amount_change],
            'Months_as_Customer': [months_as_customer],
            **dict(zip(education_columns, education_data)),
            **dict(zip(salary_columns, salary_data))
        })

        if st.button("Predict Customer Retention"):
            predict_single_customer(input_data)
    else:
        uploaded_file = st.file_uploader("Upload Customer Data CSV", type=["csv"])
        if uploaded_file:
            process_uploaded_file(uploaded_file)

if __name__ == "__main__":
    main_page()
