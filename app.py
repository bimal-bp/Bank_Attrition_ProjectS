import streamlit as st

# Initialize session state for user type and login state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'user_type' not in st.session_state:
    st.session_state.user_type = None

# Home Page
def home_page():
    st.title("Welcome to Our Bank Service")
    st.header("Please log in")

    # Login Selection (two buttons: Customer and Employee)
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Customer Login"):
            st.session_state.user_type = "Customer"
            st.session_state.logged_in = True
            st.session_state.transition = None  # Reset transition state when logging in as Customer
            st.experimental_rerun()  # Refresh the page to show customer page

    with col2:
        if st.button("Employee Login"):
            st.session_state.user_type = "Employee"
            st.session_state.logged_in = True
            st.session_state.transition = None  # Reset transition state when logging in as Employee
            st.experimental_rerun()  # Refresh the page to show employee page

# Customer Page
def customer_page():
    st.title("Customer Page")
    st.header("Welcome to Your Bank Account!")

    # Buttons or features specific to the customer
    if st.button("Transactions"):
        st.session_state.transition = "Transactions"  # Set transition to transactions
        st.experimental_rerun()

    if st.button("Submit Feedback"):
        st.session_state.transition = "Feedback"  # Set transition to feedback
        st.experimental_rerun()

# Employee Page
def employee_page():
    st.title("Employee Page")
    st.header("Welcome to the Employee Dashboard!")

    # Buttons or features specific to the employee
    if st.button("Check Customer Retention"):
        st.write("This feature will be developed later for customer retention analysis.")

    if st.button("Customer Feedback Analysis"):
        st.write("This feature will be developed later for analyzing customer feedback.")

# Main code to switch between pages based on user login
if not st.session_state.logged_in:
    home_page()
else:
    if st.session_state.user_type == "Customer":
        customer_page()
    elif st.session_state.user_type == "Employee":
        employee_page()
