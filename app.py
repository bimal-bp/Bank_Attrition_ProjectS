import streamlit as st

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
# Home Page
def home_page():
    st.title("Welcome to Our Bank Service")
    st.header("Please log in")

    # Login Selection (Customer and Employee in the same section)
    user_type = st.radio("Login as", ["Customer", "Employee"])

    if user_type == "Customer":
        st.session_state.user_type = "Customer"
        st.session_state.transition = None  # Reset transition state when logging in as Customer

    elif user_type == "Employee":
        employee_name = st.text_input("Enter your name", key="employee_name")
        employee_password = st.text_input("Enter your password", type="password", key="employee_password")
        if st.button("Employee Login"):
            if employee_name == "admin" and employee_password == "admin123":  # Example credentials
                st.session_state.user_type = "Employee"
                st.session_state.transition = None  # Reset transition state when logging in as Employee
            else:
                st.error("Invalid login credentials. Please try again.")

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

    # Customer Retention Prediction
    retention_option = st.radio("Choose Customer Retention Prediction for:", ["Individual Customer", "Group"])
    
    if retention_option == "Individual Customer":
        customer_id = st.text_input("Enter the customer's ID or Name")
        if st.button("Predict Retention for Customer"):
            # You can integrate your model prediction code here
            st.success(f"Prediction for customer {customer_id}: Retained")
            # Add code to show the prediction results

    elif retention_option == "Group":
        group_id = st.text_input("Enter the group ID")
        if st.button("Predict Retention for Group"):
            # You can integrate your model prediction code here
            st.success(f"Prediction for group {group_id}: Retained")
            # Add code to show the prediction results

    # You can add additional functionality for employees here
    if st.button("Check Customer Retention"):
        st.write("This feature will be developed later for customer retention analysis.")

    if st.button("Customer Feedback Analysis"):
        st.write("This feature will be developed later for analyzing customer feedback.")

    # Example: Option to log out (reset user type)
    if st.button("Log Out"):
        st.session_state.user_type = None  # Reset user type to None to go back to the home page
        st.session_state.transition = None  # Reset transition state
        home_page()  # Redirect to home page

# Main code to switch between pages based on user login
if 'user_type' not in st.session_state:
    home_page()
else:
    if st.session_state.user_type == "Customer":
        customer_page()
    elif st.session_state.user_type == "Employee":
        employee_page()  # Employee page with retention prediction feature
