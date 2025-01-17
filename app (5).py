import streamlit as st
import pandas as pd
import joblib

# Load the trained model
best_rf_model = joblib.load('best_rf_model.pkl')

# Streamlit app header
st.title('Customer Churn Prediction')

# Create input fields for the user to provide the necessary data
customer_age = st.number_input("Customer Age", min_value=18, max_value=100, value=30)
credit_limit = st.number_input("Credit Limit", min_value=0.0, value=3000.0)
total_transactions_count = st.number_input("Total Transactions Count", min_value=0, value=50)
total_transaction_amount = st.number_input("Total Transaction Amount", min_value=0.0, value=5000.0)
inactive_months_12_months = st.number_input("Inactive Months (12 Months)", min_value=0, max_value=12, value=2)
transaction_count_change_q4_q1 = st.number_input("Transaction Count Change (Q4-Q1)", min_value=0.0, value=0.5)
total_products_used = st.number_input("Total Products Used", min_value=1, value=2)
average_credit_utilization = st.number_input("Average Credit Utilization", min_value=0.0, max_value=1.0, value=0.2)
customer_contacts_12_months = st.number_input("Customer Contacts in 12 Months", min_value=0, value=1)
transaction_amount_change_q4_q1 = st.number_input("Transaction Amount Change (Q4-Q1)", min_value=0.0, value=0.5)
months_as_customer = st.number_input("Months as Customer", min_value=1, value=12)

# Dummy categorical features (replace with real inputs for categorical values)
college = st.selectbox("College", [0, 1])
doctorate = st.selectbox("Doctorate", [0, 1])
graduate = st.selectbox("Graduate", [0, 1])
high_school = st.selectbox("High School", [0, 1])
post_graduate = st.selectbox("Post-Graduate", [0, 1])
uneducated = st.selectbox("Uneducated", [0, 1])
salary_120k = st.selectbox("$120K +", [0, 1])
salary_40k_60k = st.selectbox("$40K - $60K", [0, 1])
salary_60k_80k = st.selectbox("$60K - $80K", [0, 1])
salary_80k_120k = st.selectbox("$80K - $120K", [0, 1])
less_than_40k = st.selectbox("Less than $40K", [0, 1])

# Prepare input data for prediction (ensure correct order of columns)
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
    "College": [college],
    "Doctorate": [doctorate],
    "Graduate": [graduate],
    "High School": [high_school],
    "Post-Graduate": [post_graduate],
    "Uneducated": [uneducated],
    "$120K +": [salary_120k],
    "$40K - $60K": [salary_40k_60k],
    "$60K - $80K": [salary_60k_80k],
    "$80K - $120K": [salary_80k_120k],
    "Less than $40K": [less_than_40k]
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
if st.button('Predict Churn'):
    prediction = best_rf_model.predict(input_df)
    if prediction[0] == 1:
        st.write("Prediction: Customer is likely to churn.")
    else:
        st.write("Prediction: Customer is unlikely to churn.")
