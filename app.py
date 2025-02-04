import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt

# Load the pre-trained model
try:
    model = pickle.load(open("best_rf_model.pkl", "rb"))
except FileNotFoundError:
    model = None
    st.error("Model file not found. Please ensure 'best_rf_model.pkl' exists.")
except Exception as e:
    model = None
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
            else:
                st.error("Incorrect username or password. Please try again.")

    with col2:
        employee_username = st.text_input("Enter Employee Username", key="employee_username")
        employee_password = st.text_input("Enter Employee Password", type="password", key="employee_password")
        if st.button("Log In as Employee"):
            if employee_username == "admin" and employee_password == "admin123":
                st.session_state.user_type = "Employee"
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
    prediction_type = st.sidebar.selectbox("Select Prediction Type", ["Single", "Group"])

    if prediction_type == "Single":
        st.write("### Individual Customer Retention Prediction")
        customer_data = {
            "Customer_Age": st.sidebar.number_input("Customer Age", min_value=18, max_value=100, value=30),
            "Credit_Limit": st.sidebar.number_input("Credit Limit", min_value=0, value=7000),
            "Total_Transactions_Count": st.sidebar.number_input("Total Transactions Count", min_value=0, value=50),
            "Total_Transaction_Amount": st.sidebar.number_input("Total Transaction Amount", min_value=0, value=5000),
            "Inactive_Months_12_Months": st.sidebar.number_input("Inactive Months (12 Months)", min_value=0, max_value=12, value=2),
            "Transaction_Count_Change_Q4_Q1": st.sidebar.number_input("Transaction Count Change (Q4-Q1)", min_value=0.0, value=0.5),
            "Total_Products_Used": st.sidebar.number_input("Total Products Used", min_value=1, value=2),
            "Average_Credit_Utilization": st.sidebar.number_input("Average Credit Utilization", min_value=0.0, max_value=1.0, value=0.2),
            "Customer_Contacts_12_Months": st.sidebar.number_input("Customer Contacts in 12 Months", min_value=0, value=1),
            "Transaction_Amount_Change_Q4_Q1": st.sidebar.number_input("Transaction Amount Change (Q4-Q1)", min_value=0.0, value=0.5),
            "Months_as_Customer": st.sidebar.number_input("Months as Customer", min_value=1, value=12)
        }

        input_df = pd.DataFrame([customer_data])

        if st.sidebar.button("Predict"):
            if model:
                try:
                    prediction = model.predict(input_df)
                    retention = "Retained" if prediction[0] == 1 else "Churned"
                    st.write(f"Prediction: Customer will be {retention}.")
                except Exception as e:
                    st.error(f"Error during prediction: {e}")
            else:
                st.error("Model is not loaded.")

    elif prediction_type == "Group":
        st.write("### Group Customer Retention Prediction")
        uploaded_file = st.sidebar.file_uploader("Upload a CSV File for Group Prediction", type=["csv"])

        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            required_columns = ["Customer_Age", "Credit_Limit", "Total_Transactions_Count", 
                                "Total_Transaction_Amount", "Inactive_Months_12_Months", 
                                "Transaction_Count_Change_Q4_Q1", "Total_Products_Used", 
                                "Average_Credit_Utilization", "Customer_Contacts_12_Months", 
                                "Transaction_Amount_Change_Q4_Q1", "Months_as_Customer"]

            # Validate required columns
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                st.error(f"Missing required columns: {', '.join(missing_columns)}")
            else:
                st.write("### Data Preview")
                st.dataframe(df.head())

                try:
                    predictions = model.predict(df[required_columns]) if model else []
                    if not model:
                        st.error("Model is not loaded.")
                        return

                    df['Retention_Prediction'] = ["Retained" if p == 1 else "Churned" for p in predictions]

                    # Plot Pie Chart with Styling
                    attrit_count = sum(predictions)
                    stay_count = len(predictions) - attrit_count

                    fig, ax = plt.subplots(figsize=(6, 6))
                    ax.pie([stay_count, attrit_count], labels=["Stay", "Attrit"], autopct='%1.1f%%', colors=["lightgreen", "lightcoral"],
                           startangle=90, wedgeprops={"edgecolor": "black", "linewidth": 1.5, "linestyle": "solid"})
                    ax.set_title("Customer Attrition Distribution", fontsize=14, fontweight="bold", color="darkblue")
                    st.pyplot(fig)

                    st.write("### Prediction Results")
                    st.dataframe(df)

                except Exception as e:
                    st.error(f"Error processing the file: {e}")

    if st.button("Log Out"):
        st.session_state.user_type = None
        home_page()

if 'user_type' not in st.session_state:
    home_page()
else:
    if st.session_state.user_type == "Customer":
        customer_page()
    elif st.session_state.user_type == "Employee":
        employee_page()
