import streamlit as st
import pandas as pd
import joblib

# Load the trained model
best_rf_model = joblib.load('best_rf_model.pkl')

# Streamlit app header
st.title('Customer Churn Prediction')

# Sidebar for input data
st.sidebar.header('Input Data')

# Define input fields for the user to provide the necessary data
Customer_Age = st.sidebar.number_input('Customer Age', min_value=18, max_value=100, value=30)
Credit_Limit = st.sidebar.number_input('Credit Limit', min_value=0, value=5000)
Total_Transactions_Count = st.sidebar.number_input('Total Transactions Count', min_value=0, value=50)
Total_Transaction_Amount = st.sidebar.number_input('Total Transaction Amount', min_value=0, value=1000)
Inactive_Months_12_Months = st.sidebar.number_input('Inactive Months (12 Months)', min_value=0, value=3)
Transaction_Count_Change_Q4_Q1 = st.sidebar.number_input('Transaction Count Change Q4/Q1', value=0)
Total_Products_Used = st.sidebar.number_input('Total Products Used', min_value=1, value=3)
Average_Credit_Utilization = st.sidebar.number_input('Average Credit Utilization', min_value=0.0, max_value=1.0, value=0.5)
Customer_Contacts_12_Months = st.sidebar.number_input('Customer Contacts (12 Months)', min_value=0, value=1)
Transaction_Amount_Change_Q4_Q1 = st.sidebar.number_input('Transaction Amount Change Q4/Q1', value=0)
Months_as_Customer = st.sidebar.number_input('Months as Customer', min_value=0, value=12)

# For categorical features like education, you can use selectbox
education = st.sidebar.selectbox('Education', ['College', 'Doctorate', 'Graduate', 'High School', 'Post-Graduate', 'Uneducated'])

# For income categories
income = st.sidebar.selectbox('Income', ['$120K +', '$40K - $60K', '$60K - $80K', '$80K - $120K', 'Less than $40K'])

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

# Ensure the column order matches the model's expected input columns
columns = [
    "Customer_Age", "Credit_Limit", "Total_Transactions_Count", "Total_Transaction_Amount", 
    "Inactive_Months_12_Months", "Transaction_Count_Change_Q4_Q1", "Total_Products_Used", 
    "Average_Credit_Utilization", "Customer_Contacts_12_Months", "Transaction_Amount_Change_Q4_Q1", 
    "Months_as_Customer", "College", "Doctorate", "Graduate", "High School", "Post-Graduate", 
    "Uneducated", "$120K +", "$40K - $60K", "$60K - $80K", "$80K - $120K", "Less than $40K"
]

input_df = input_df[columns]

# Prediction
if st.sidebar.button('Predict Churn'):
    prediction = best_rf_model.predict(input_df)
    if prediction[0] == 1:
        st.write("Prediction: Customer is likely to churn.")
    else:
        st.write("Prediction: Customer is unlikely to churn.")
