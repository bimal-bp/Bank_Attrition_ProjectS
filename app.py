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

# Employee Page
def employee_page():
    st.title("Employee Page")
    st.header("Welcome to the Employee Dashboard!")

    # You can add additional functionality here
    st.write("Here, employees can manage bank operations such as reviewing customer feedback, viewing transaction history, etc.")

    # Example: A feedback management section
    if st.button("View Customer Feedback"):
        if len(st.session_state.feedback_list) > 0:
            st.write("Customer Feedback:")
            for feedback in st.session_state.feedback_list:
                name, feedback_text, rating = feedback
                st.write(f"Name: {name}, Rating: {rating}/5")
                st.write(f"Feedback: {feedback_text}")
        else:
            st.warning("No feedback available yet.")

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
        employee_page()  # Employee page functionality

