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

# Initialize session state for feedback if not present
if 'feedback_list' not in st.session_state:
    st.session_state.feedback_list = []

# Home Page
st.title("Customer Retention")

# Login Selection
col1, col2 = st.columns(2)

with col1:
    if st.button("Customer Login"):
        st.session_state.user_type = "Customer"

with col2:
    if st.button("Employee Login"):
        st.session_state.user_type = "Employee"

if 'user_type' in st.session_state:
    if st.session_state.user_type == "Customer":
        st.header("Customer Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            st.success("Login successful")
            bank = Bank()
            action = st.selectbox("Select Action", ["Deposit", "Withdraw", "Check Balance", "Give Feedback"])
            
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
            
            elif action == "Give Feedback":
                feedback = st.text_area("Enter your feedback")
                if st.button("Submit Feedback"):
                    st.session_state.feedback_list.append((username, feedback))
                    st.success("Feedback submitted successfully")
    
    elif st.session_state.user_type == "Employee":
        st.header("Employee Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            st.success("Login successful")
            st.header("Customer Feedback")
            for i, (cust, fb) in enumerate(st.session_state.feedback_list):
                st.write(f"**{cust}:** {fb}")
                sentiment = st.radio(f"Classify feedback {i+1}", ["Positive", "Negative"], key=f"sentiment_{i}")
                if st.button(f"Submit Classification {i+1}"):
                    st.success(f"Feedback classified as {sentiment}")
