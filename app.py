import streamlit as st

# Sample credentials for Admin and Customer (replace with actual storage in production)
admin_credentials = {"admin": "adminpassword"}
customer_credentials = {"customer1": "password123"}

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

# Function to handle user login
def login(user_type):
    st.title(f"{user_type} Login")

    # Input fields for username and password
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    login_button = st.button("Login")

    if login_button:
        if user_type == "Admin":
            if username in admin_credentials and admin_credentials[username] == password:
                st.session_state.user_type = "Admin"
                st.session_state.username = username
                st.success("Login successful as Admin!")
                st.session_state.transition = None
                return True  # Return True if login successful
            else:
                st.error("Invalid username or password for Admin")
        elif user_type == "Customer":
            if username in customer_credentials and customer_credentials[username] == password:
                st.session_state.user_type = "Customer"
                st.session_state.username = username
                st.success("Login successful as Customer!")
                st.session_state.transition = None
                return True  # Return True if login successful
            else:
                st.error("Invalid username or password for Customer")
    return False  # Return False if login fails

# Home Page
def home_page():
    st.title("Welcome to Our Bank Service")
    st.header("Please log in")

    # Login Selection
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Admin Login"):
            if login("Admin"):
                admin_page()  # Go to admin page after login

    with col2:
        if st.button("Customer Login"):
            if login("Customer"):
                customer_page()  # Go to customer page after login

# Customer Page
def customer_page():
    st.title("Customer Page")
    st.header(f"Welcome {st.session_state.username}!")

    # Select Action in two columns
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Transactions"):
            st.session_state.transition = "Transactions"
            
    with col2:
        if st.button("Submit Feedback"):
            st.session_state.transition = "Feedback"

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
            st.session_state.feedback_list.append((name, feedback, rating))
            st.success(f"Feedback submitted successfully! Rating: {rating}/5")
            st.info("Thank you for your feedback! We will work on it.")
        else:
            st.error("Please provide your name and feedback.")

def admin_page():
    st.title("Admin Page")
    st.header(f"Welcome Admin!")

    # Admin functionality (For now, placeholder text)
    st.write("Admin Dashboard functionality will be added here.")
    
    # Option to log out (reset user type)
    if st.button("Log Out"):
        st.session_state.user_type = None  # Reset user type to None
        st.session_state.username = None  # Reset username
        home_page()  # Redirect to home page

# Main code to switch between pages based on user login
if 'user_type' not in st.session_state:
    home_page()
else:
    if st.session_state.user_type == "Customer":
        customer_page()
    elif st.session_state.user_type == "Admin":
        admin_page()
