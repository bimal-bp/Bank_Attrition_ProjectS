import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pickle

# Load trained model
with open('best_rf_model.pkl', 'rb') as model_file:
    best_rf_model = pickle.load(model_file)

def display_feedback(prediction):
    if prediction == 1:
        st.write("### Suggested Actions: Improve engagement strategies, offer personalized incentives.")
    else:
        st.write("### Suggested Actions: Maintain current engagement level and monitor periodically.")

def predict_customer(input_df):
    prediction = best_rf_model.predict(input_df)
    
    if prediction[0] == 1:
        st.markdown("### Prediction: Customer is likely to attrit ✅")
    else:
        st.markdown("### Prediction: Customer is unlikely to attrit ❌")
    
    display_feedback(prediction[0])

def process_uploaded_file(uploaded_file):
    df = pd.read_csv(uploaded_file)
    required_columns = [
        'Customer_Age', 'Credit_Limit', 'Total_Transactions_Count',
        'Total_Transaction_Amount', 'Inactive_Months_12_Months',
        'Transaction_Count_Change_Q4_Q1', 'Total_Products_Used',
        'Average_Credit_Utilization', 'Customer_Contacts_12_Months',
        'Transaction_Amount_Change_Q4_Q1', 'Months_as_Customer',
        'College', 'Doctorate', 'Graduate', 'High School', 'Post-Graduate',
        'Uneducated', '$120K +', '$40K - $60K', '$60K - $80K', '$80K - $120K',
        'Less than $40K'
    ]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"Missing required columns: {', '.join(missing_columns)}")
        return None
    
    predictions = best_rf_model.predict(df)
    attrit_count = sum(predictions)
    stay_count = len(predictions) - attrit_count
    
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie([stay_count, attrit_count], labels=["Stay", "Attrit"], autopct='%1.1f%%', colors=["lightgreen", "lightcoral"],
           startangle=90, wedgeprops={"edgecolor": "black", "linewidth": 1.5})
    ax.set_title("Customer Attrition Distribution", fontsize=14, fontweight="bold", color="darkblue")
    st.pyplot(fig)

def main_page():
    st.title("Customer Attrition Prediction")
    st.sidebar.header(f"Welcome, {st.session_state.user_name}")
    
    if st.session_state.prediction_type == "Single":
        customer_data = {
            "Customer_Age": st.sidebar.number_input("Customer Age", min_value=18, max_value=100, value=30),
            "Credit_Limit": st.sidebar.number_input("Credit Limit", min_value=0, value=7000),
            "Total_Transactions_Count": st.sidebar.number_input("Total Transactions Count", min_value=0, value=50),
            "Total_Transaction_Amount": st.sidebar.number_input("Total Transaction Amount", min_value=0, value=5000),
            "Inactive_Months_12_Months": st.sidebar.number_input("Inactive Months (12 Months)", min_value=0, max_value=12, value=2),
            "Transaction_Count_Change_Q4_Q1": st.sidebar.number_input("Transaction Count Change (Q4-Q1)", min_value=0.0, value=0.5),
            "Total_Products_Used": st.sidebar.number_input("Total Products Used", min_value=1, value=2),
            "Average_Credit_Utilization": st.sidebar.number_input("Average Credit Utilization", min_value=0.0, max_value=1.0, value=0.2),
            "Customer_Contacts_12_Months": st.sidebar.number_input("Customer Contacts in 12 Months", min_value=0, value=1),
            "Transaction_Amount_Change_Q4_Q1": st.sidebar.number_input("Transaction Amount Change (Q4-Q1)", min_value=0.0, value=0.5),
            "Months_as_Customer": st.sidebar.number_input("Months as Customer", min_value=1, value=12),
            "College": st.sidebar.selectbox("Select Education Level", ["College", "Doctorate", "Graduate", "High School", "Post-Graduate", "Uneducated"]),
            "Income": st.sidebar.selectbox("Select Income Range", ["$120K +", "$40K - $60K", "$60K - $80K", "$80K - $120K", "Less than $40K"])
        }
        
        input_df = pd.DataFrame([{key: 1 if customer_data[key] == value else 0 for key in customer_data}])
        predict_customer(input_df)
    else:
        uploaded_file = st.sidebar.file_uploader("Upload CSV file for Group Prediction", type=["csv"])
        if uploaded_file is not None:
            process_uploaded_file(uploaded_file)

if st.session_state.logged_in:
    main_page()
else:
    st.error("Please log in to access the application.")
