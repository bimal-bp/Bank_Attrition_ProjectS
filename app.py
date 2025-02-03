import pandas as pd
import joblib
import streamlit as st
import matplotlib.pyplot as plt

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

# Initialize user_name in session state if not already set
if 'user_name' not in st.session_state:
    st.session_state.user_name = "Guest"  # Or any default name

# Prediction Function for Single Customer
def predict_single_customer(input_df):
    # Extract values from input_df
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
        st.write(f"- Inactive Months (12 months): {inactive_months_12_months} months")
        st.write(f"- Transaction Amount Change (Q4-Q1): {transaction_amount_change_q4_q1}")
        st.write(f"- Total Products Used: {total_products_used}")
        st.write(f"- Total Transactions Count: {total_transactions_count}")
        st.write(f"- Average Credit Utilization: {average_credit_utilization}")
        st.write(f"- Customer Contacts in 12 Months: {customer_contacts_12_months}")
        display_feedback(prediction[0])  # Pass prediction to feedback function
    else:
        st.markdown(f"### Prediction: Customer is unlikely to attrit ❌")
        st.subheader("Non-Attrition Insights:")
        st.write(f"- Inactive Months (12 months): {inactive_months_12_months} months")
        st.write(f"- Transaction Amount Change (Q4-Q1): {transaction_amount_change_q4_q1}")
        st.write(f"- Total Products Used: {total_products_used}")
        st.write(f"- Total Transactions Count: {total_transactions_count}")
        st.write(f"- Average Credit Utilization: {average_credit_utilization}")
        st.write(f"- Customer Contacts in 12 Months: {customer_contacts_12_months}")
        display_feedback(prediction[0])  # Pass prediction to feedback function

# Display feedback based on prediction
def display_feedback(prediction):
    feedback = "Thank you for using our service!" if prediction == 0 else "This customer may need intervention."
    st.write(feedback)

# Main page
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
            education: [1],
            income: [1]
        }
        
        input_df = pd.DataFrame(input_data)
        if st.button("Predict Single Customer"):
            predict_single_customer(input_df)

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
                st.session_state.user_name = customer_username  # Set user_name on login
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
                st.session_state.user_name = employee_username  # Set user_name on login
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

# Feedback Section
def feedback_section():
    st.title("Submit Feedback")
    
    # Feedback form asking for name, service rating, and comments
    name = st.text_input("Enter Your Name")
    service_rating = st.selectbox("Rate our service", ["Excellent", "Good", "Fair", "Poor"])
    comments = st.text_area("Your Comments")
    
    if st.button("Submit Feedback"):
        if name and service_rating and comments:
            feedback = {
                "Name": name,
                "Service Rating": service_rating,
                "Comments": comments
            }
            st.session_state.feedback_list.append(feedback)
            st.success("Thank you for your feedback!")

# Main function to display the appropriate page
def app():
    if 'user_type' not in st.session_state:
        st.session_state.user_type = None

    if st.session_state.user_type == "Customer":
        customer_page()
    elif st.session_state.user_type == "Employee":
        main_page()
    else:
        home_page()

if __name__ == "__main__":
    app()
