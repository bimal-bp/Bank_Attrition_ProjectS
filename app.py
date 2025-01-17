import streamlit as st
import pandas as pd
import joblib

# Load the trained model
best_rf_model = joblib.load('best_rf_model.pkl')

# Initialize session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# Page navigation logic
if not st.session_state.logged_in:
    # Login Page
    st.title("Customer ATTRITION - Login")
    st.write("Please enter your name to log in.")
    user_name = st.text_input("Enter your name:")
    login_button = st.button("Log In")

    if login_button:
        if user_name.strip():
            st.session_state.logged_in = True
            st.session_state.user_name = user_name.strip()
            st.success(f"Welcome, {user_name}!")
            st.experimental_rerun()  # Reload to navigate to the main page
        else:
            st.error("Name cannot be empty.")
else:
    # Main Page - Input and Output
    st.title("Customer ATTRITION")

    # Display user's name
    st.sidebar.header(f"Welcome, {st.session_state.user_name}!")

    # Input fields in the sidebar
    st.sidebar.header('Input Data')
    Customer_Age = st.sidebar.number_input('Customer Age', min_value=18, max_value=100, value=30)
    Credit_Limit = st.sidebar.number_input('Credit Limit', min_value=0, value=3000)
    Total_Transactions_Count = st.sidebar.number_input('Total Transactions Count', min_value=0, value=50)
    Total_Transaction_Amount = st.sidebar.number_input('Total Transaction Amount', min_value=0, value=5000)
    Inactive_Months_12_Months = st.sidebar.number_input('Inactive Months (12 Months)', min_value=0, value=2)
    Transaction_Count_Change_Q4_Q1 = st.sidebar.number_input('Transaction Count Change Q4/Q1', value=0.50)
    Total_Products_Used = st.sidebar.number_input('Total Products Used', min_value=1, value=2)
    Average_Credit_Utilization = st.sidebar.number_input('Average Credit Utilization', min_value=0.0, max_value=1.0, value=0.2)
    Customer_Contacts_12_Months = st.sidebar.number_input('Customer Contacts (12 Months)', min_value=0, value=1)
    Transaction_Amount_Change_Q4_Q1 = st.sidebar.number_input('Transaction Amount Change Q4/Q1', value=0.50)
    Months_as_Customer = st.sidebar.number_input('Months as Customer', min_value=0, value=12)

    # For categorical features like education and income
    education = st.sidebar.selectbox('Select Education Level', ['Choose an option', 'College', 'Doctorate', 'Graduate', 'High School', 'Post-Graduate', 'Uneducated'])
    income = st.sidebar.selectbox('Select Income Range', ['Choose an option', '$120K +', '$40K - $60K', '$60K - $80K', '$80K - $120K', 'Less than $40K'])

    # Prepare input data for prediction
    input_data = {
        'Customer_Age': [Customer_Age],
        'Credit_Limit': [Credit_Limit],
        'Total_Transactions_Count': [Total_Transactions_Count],
        'Total_Transaction_Amount': [Total_Transaction_Amount],
        'Inactive_Months_12_Months': [Inactive_Months_12_Months],
        'Transaction_Count_Change_Q4_Q1': [Transaction_Count_Change_Q4_Q1],
        'Total_Products_Used': [Total_Products_Used],
        'Average_Credit_Utilization': [Average_Credit_Utilization],
        'Customer_Contacts_12_Months': [Customer_Contacts_12_Months],
        'Transaction_Amount_Change_Q4_Q1': [Transaction_Amount_Change_Q4_Q1],
        'Months_as_Customer': [Months_as_Customer],
        'College': [1 if education == 'College' else 0],
        'Doctorate': [1 if education == 'Doctorate' else 0],
        'Graduate': [1 if education == 'Graduate' else 0],
        'High School': [1 if education == 'High School' else 0],
        'Post-Graduate': [1 if education == 'Post-Graduate' else 0],
        'Uneducated': [1 if education == 'Uneducated' else 0],
        '$120K +': [1 if income == '$120K +' else 0],
        '$40K - $60K': [1 if income == '$40K - $60K' else 0],
        '$60K - $80K': [1 if income == '$60K - $80K' else 0],
        '$80K - $120K': [1 if income == '$80K - $120K' else 0],
        'Less than $40K': [1 if income == 'Less than $40K' else 0],
    }

    # Create a DataFrame for input data
    input_df = pd.DataFrame(input_data)

    # Prediction button in the sidebar
    if st.sidebar.button('Predict Churn'):
        if education == 'Choose an option' or income == 'Choose an option':
            st.sidebar.warning("Please select both Education and Income levels.")
        else:
            # Predict churn based on user inputs
            prediction = best_rf_model.predict(input_df)
            if prediction[0] == 1:
                st.write(f"Prediction: Customer is likely to churn ✔️ (Logged in as {st.session_state.user_name})")
            else:
                st.write(f"Prediction: Customer is unlikely to churn ❌ (Logged in as {st.session_state.user_name})")
