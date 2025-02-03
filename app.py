import pandas as pd
import joblib
import streamlit as st

# Load the trained model
best_rf_model = joblib.load('best_rf_model.pkl')

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

    # Login Selection
    col1, col2 = st.columns(2)

    with col1:
        customer_username = st.text_input("Enter Customer Username", key="customer_username")
        customer_password = st.text_input("Enter Customer Password", type="password", key="customer_password")
        if st.button("Log In as Customer"):
            # Validate username and password for Customer
            if customer_username == "customer" and customer_password == "customer123":
                st.session_state.user_type = "Customer"
                st.session_state.transition = None  # Reset transition state
            else:
                st.error("Incorrect username or password. Please try again.")

    with col2:
        employee_username = st.text_input("Enter Employee Username", key="employee_username")
        employee_password = st.text_input("Enter Employee Password", type="password", key="employee_password")
        if st.button("Log In as Employee"):
            # Validate username and password for Employee
            if employee_username == "admin" and employee_password == "admin123":
                st.session_state.user_type = "Employee"
                st.session_state.transition = None  # Reset transition state
            else:
                st.error("Incorrect username or password. Please try again.")

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

    # Customer Retention Feature
    if st.button("Check Customer Retention"):
        st.write("Select Customer Retention Type:")
        retention_type = st.radio("Choose Retention Prediction Type", ["Single Customer", "Group of Customers"])
        
        if retention_type == "Single Customer":
            single_customer_prediction()
        elif retention_type == "Group of Customers":
            group_customer_prediction()

# Function to predict customer attrition
def predict_customer(input_df):
    prediction = best_rf_model.predict(input_df)
    if prediction[0] == 1:
        st.markdown("### Prediction: Customer is likely to attrit ✅")
    else:
        st.markdown("### Prediction: Customer is unlikely to attrit ❌")

# Single Customer Prediction
def single_customer_prediction():
    st.title("Single Customer Attrition Prediction")

    # Input fields for individual customer
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

    # Education and Income Dropdowns
    education = st.selectbox("Select Education Level", ["College", "Doctorate", "Graduate", "High School", "Post-Graduate", "Uneducated"])
    income = st.selectbox("Select Income Range", ["$120K +", "$40K - $60K", "$60K - $80K", "$80K - $120K", "Less than $40K"])

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

    if st.button("Predict Customer Attrition"):
        predict_customer(input_df)

# Group Customer Prediction
def group_customer_prediction():
    st.title("Group Customer Attrition Prediction")

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        
        # Check if necessary columns are present
        required_columns = [
            "Customer_Age", "Credit_Limit", "Total_Transactions_Count", "Total_Transaction_Amount",
            "Inactive_Months_12_Months", "Transaction_Count_Change_Q4_Q1", "Total_Products_Used",
            "Average_Credit_Utilization", "Customer_Contacts_12_Months", "Transaction_Amount_Change_Q4_Q1",
            "Months_as_Customer", "Education", "Income"
        ]
        
        if all(col in df.columns for col in required_columns):
            predictions = best_rf_model.predict(df)
            for i, prediction in enumerate(predictions):
                if prediction == 1:
                    st.markdown(f"### Customer {i+1}: Likely to attrit ✅")
                else:
                    st.markdown(f"### Customer {i+1}: Unlikely to attrit ❌")
        else:
            st.error("Uploaded file is missing required columns.")

# Streamlit App Entry Point
def run_app():
    if 'user_type' not in st.session_state:
        st.session_state.user_type = None

    if st.session_state.user_type is None:
        home_page()
    elif st.session_state.user_type == "Customer":
        customer_page()
    elif st.session_state.user_type == "Employee":
        employee_page()

if __name__ == '__main__':
    run_app()
