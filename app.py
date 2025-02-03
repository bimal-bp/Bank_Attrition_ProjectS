import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.ensemble import RandomForestClassifier

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

# Dummy RandomForest model for testing purposes
best_rf_model = RandomForestClassifier()

# Home Page
def home_page():
    st.title("Welcome to Our Bank Service")
    st.header("Please log in")

    # Login Selection
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Customer Login"):
            st.session_state.user_type = "Customer"
            st.session_state.transition = None  # Reset transition state when logging in as Customer

    with col2:
        if st.button("Employee Login"):
            st.session_state.user_type = "Employee"
            st.session_state.transition = None  # Reset transition state when logging in as Employee

# Customer Page
def customer_page():
    st.title("Customer Page")
    st.header("Welcome to Your Bank Account!")

    # Select Action in two columns
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Transactions"):
            st.session_state.transition = "Transactions"  # Set transition to transactions
            
    with col2:
        if st.button("Submit Feedback"):
            st.session_state.transition = "Feedback"  # Set transition to feedback

    # Show Transaction or Feedback based on the user's choice
    if st.session_state.transition == "Transactions":
        transaction_section()
    elif st.session_state.transition == "Feedback":
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

def feedback_section():
    st.title("Submit Feedback")
    
    # Feedback form asking for name, feedback, and star rating
    name = st.text_input("Enter your name")
    feedback = st.text_area("Write your feedback here")
    
    # Asking for star rating out of 5
    rating = st.radio("Rate your experience (1 to 5)", [1, 2, 3, 4, 5])
    
    if st.button("Submit Feedback", key="submit_feedback"):
        if name and feedback:
            # Storing feedback with rating properly
            st.session_state.feedback_list.append((name, feedback, rating))
            st.success(f"Feedback submitted successfully! Rating: {rating}/5")
            
            # Display the thank you message
            st.info("Thank you for your feedback! We will work on it.")
            
            # Optionally reset form (if you want to clear the inputs)
            # st.session_state.transition = None  # Uncomment this line if needed

        else:
            st.error("Please provide your name and feedback.")

def employee_page():
    st.title("Employee Page")
    st.header("Welcome to the Employee Dashboard!")

    # You can add additional functionality here
    st.write("Here, employees can manage bank operations.")

    # Customer retention prediction button
    if st.button("Check Customer Retention"):
        customer_retention_analysis()

    if st.button("Customer Feedback Analysis"):
        st.write("This feature will be developed later for analyzing customer feedback.")

    # Example: Option to log out (reset user type)
    if st.button("Log Out"):
        st.session_state.user_type = None  # Reset user type to None to go back to the home page
        st.session_state.transition = None  # Reset transition state
        home_page()  # Redirect to home page

# Customer retention prediction analysis
def customer_retention_analysis():
    st.write("Please upload a CSV file for customer retention analysis.")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    
    if uploaded_file is not None:
        process_uploaded_file(uploaded_file)

def process_uploaded_file(uploaded_file):
    st.write("Processing the uploaded file...")

    try:
        df = pd.read_csv(uploaded_file)
        st.write("File loaded successfully. Here's a preview of the data:")
        st.write(df.head())

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

        df = df[required_columns]
        predictions = best_rf_model.predict(df)

        attrit_count = sum(predictions)
        stay_count = len(predictions) - attrit_count

        fig, ax = plt.subplots(figsize=(8, 8))
        colors = ["#66b3ff", "#ff6666"]

        # Create the pie chart with better styling
        wedges, texts, autotexts = ax.pie([stay_count, attrit_count], labels=["Stay", "Leave"], autopct='%1.1f%%', colors=colors,
                                          startangle=90, wedgeprops={"edgecolor": "black", "linewidth": 1.5, "linestyle": "solid"})

        # Add shadow for depth
        ax.pie([stay_count, attrit_count], labels=["Stay", "Leave"], autopct='%1.1f%%', colors=colors,
               startangle=90, wedgeprops={"edgecolor": "black", "linewidth": 1.5, "linestyle": "solid"}, shadow=True)

        # Title and font styling
        ax.set_title("Customer Attrition Distribution", fontsize=16, fontweight="bold", color="darkblue")

        # Style the labels and percentages for readability
        for text in texts:
            text.set_fontsize(14)
            text.set_fontweight("bold")
            text.set_color("black")

        for autotext in autotexts:
            autotext.set_fontsize(12)
            autotext.set_fontweight("bold")
            autotext.set_color("white")

        # Set aspect ratio to make sure pie is circular
        ax.axis('equal')

        # Show the chart
        st.pyplot(fig)

        # Display predictions for each customer
        for idx, prediction in enumerate(predictions):
            st.write(f"Customer {idx + 1} Prediction: {'Stay' if prediction == 0 else 'Leave'}")

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")

# Main code to switch between pages based on user login
if 'user_type' not in st.session_state:
    home_page()
else:
    if st.session_state.user_type == "Customer":
        customer_page()
    elif st.session_state.user_type == "Employee":
        employee_page()  # Employee page functionality
