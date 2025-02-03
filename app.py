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

# Caching the feedback list
@st.cache(allow_output_mutation=True)
def get_feedback():
    return []

# Initialize session state for feedback if not present
if 'feedback_list' not in st.session_state:
    st.session_state.feedback_list = get_feedback()

# Home Page (for Login)
def home_page():
    st.title("Welcome to Our Bank Service")

    # Login Selection
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Customer Login"):
            st.session_state.user_type = "Customer"
            st.experimental_rerun()  # Redirect to Customer page

    with col2:
        if st.button("Employee Login"):
            st.session_state.user_type = "Employee"
            st.experimental_rerun()  # Redirect to Employee page

# Customer Page
def customer_page():
    st.title("Customer Page")
    st.header("Welcome, Customer!")
    
    # Select Action in two columns
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Transactions"):
            st.session_state.page = "Transactions"
            st.experimental_rerun()  # Redirect to Transactions section

    with col2:
        if st.button("Submit Feedback"):
            st.session_state.page = "Feedback"
            st.experimental_rerun()  # Redirect to Feedback section

    # Show Transaction or Feedback based on the user's choice
    if 'page' in st.session_state:
        if st.session_state.page == "Transactions":
            transaction_section()
        elif st.session_state.page == "Feedback":
            feedback_section()

# Transaction Section
def transaction_section():
    st.title("Transactions")
    bank = Bank()
    
    action = st.selectbox("Select Action", ["Deposit", "Withdraw", "Check Balance"])
    
    if action == "Deposit":
        amount = st.number_input("Enter amount to deposit", min_value=1)
        if st.button("Deposit"):
            balance = bank.deposit(amount)
            st.success(f"Deposit successful. New Balance: {balance}")
    
    elif action == "Withdraw":
        amount = st.number_input("Enter amount to withdraw", min_value=1)
        if st.button("Withdraw"):
            result = bank.withdraw(amount)
            if isinstance(result, str):
                st.error(result)
            else:
                st.success(f"Withdrawal successful. New Balance: {result}")
    
    elif action == "Check Balance":
        st.info(f"Your current balance is: {bank.check_balance()}")

# Feedback Section
def feedback_section():
    st.title("Submit Feedback")
    
    # Feedback form asking for name, feedback and star rating
    name = st.text_input("Enter your name")
    feedback = st.text_area("Write your feedback here")
    
    # Asking for star rating out of 5
    rating = st.radio("Rate your experience (1 to 5)", [1, 2, 3, 4, 5])
    
    if st.button("Submit Feedback"):
        if name and feedback:
            st.session_state.feedback_list.append((name, feedback, rating))
            st.success("Feedback submitted successfully!")
        else:
            st.error("Please provide your name and feedback.")

# Employee Page (to be updated later)
def employee_page():
    st.title("Employee Page")
    st.header("Welcome, Employee!")
    # Employee functionality will be added here later

# Main code to switch between pages based on user login
if 'user_type' not in st.session_state:
    home_page()
else:
    if st.session_state.user_type == "Customer":
        customer_page()
    elif st.session_state.user_type == "Employee":
        employee_page()
