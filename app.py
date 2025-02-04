import joblib
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_name" not in st.session_state:
    st.session_state.user_name = "Guest"
if "prediction_type" not in st.session_state:
    st.session_state.prediction_type = "Single"

# Load pre-trained model
best_rf_model = joblib.load("best_rf_model.pkl")  # Adjust the path to your model

def display_feedback(prediction):
    if prediction == 1:
        st.warning("This customer is likely to attrit. Consider retention strategies.")
    else:
        st.success("This customer is likely to stay. Maintain engagement efforts.")

# Prediction for individual customer
def predict_customer(input_df):
    required_columns = [
        'Inactive_Months_12_Months', 'Transaction_Amount_Change_Q4_Q1', 'Total_Products_Used',
        'Total_Transactions_Count', 'Average_Credit_Utilization', 'Customer_Contacts_12_Months'
    ]
    
    for col in required_columns:
        if col not in input_df.columns:
            input_df[col] = 0  # Set default value if column is missing

    prediction = best_rf_model.predict(input_df)

    if prediction[0] == 1:
        st.markdown("### Prediction: Customer is likely to attrit ✅")
    else:
        st.markdown("### Prediction: Customer is unlikely to attrit ❌")
    
    display_feedback(prediction[0])

# Process uploaded file for group prediction
def process_uploaded_file(uploaded_file):
    df = pd.read_csv(uploaded_file)

    required_columns = [
        'Customer_Age', 'Credit_Limit', 'Total_Transactions_Count', 'Total_Transaction_Amount',
        'Inactive_Months_12_Months', 'Transaction_Count_Change_Q4_Q1', 'Total_Products_Used',
        'Average_Credit_Utilization', 'Customer_Contacts_12_Months', 'Transaction_Amount_Change_Q4_Q1',
        'Months_as_Customer', 'College', 'Doctorate', 'Graduate', 'High School', 'Post-Graduate',
        'Uneducated', '$120K +', '$40K - $60K', '$60K - $80K', '$80K - $120K', 'Less than $40K'
    ]

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"Missing required columns: {', '.join(missing_columns)}")
        return None

    df = df[required_columns]
    predictions = best_rf_model.predict(df)

    attrit_count = sum(predictions)
    stay_count = len(predictions) - attrit_count

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie([stay_count, attrit_count], labels=["Stay", "Attrit"], autopct='%1.1f%%', colors=["lightgreen", "lightcoral"],
           startangle=90, wedgeprops={"edgecolor": "black", "linewidth": 1.5, "linestyle": "solid"})
    ax.set_title("Customer Attrition Distribution", fontsize=14, fontweight="bold", color="darkblue")
    st.pyplot(fig)

    for idx, prediction in enumerate(predictions):
        st.write(f"Customer {idx + 1} Prediction: {'Attrit' if prediction == 1 else 'Stay'}")
        display_feedback(prediction)

# Main App Page
def main_page():
    st.title("Customer Attrition Prediction")
    st.sidebar.header(f"Welcome, {st.session_state.user_name}")
    
    st.sidebar.header('Prediction Type: ' + st.session_state.prediction_type)
    if st.session_state.prediction_type == "Single":
        # Individual customer input fields
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
            "Months_as_Customer": st.sidebar.number_input("Months as Customer", min_value=1, value=12)
        }
        
        education = st.sidebar.selectbox("Select Education Level", ["College", "Doctorate", "Graduate", "High School", "Post-Graduate", "Uneducated"])
        income = st.sidebar.selectbox("Select Income Range", ["$120K +", "$40K - $60K", "$60K - $80K", "$80K - $120K", "Less than $40K"])

        input_data = {**customer_data, education: 1, income: 1}
        input_df = pd.DataFrame([input_data])
        predict_customer(input_df)
    else:
        uploaded_file = st.sidebar.file_uploader("Upload CSV file for Group Prediction", type=["csv"])
        if uploaded_file is not None:
            process_uploaded_file(uploaded_file)

# Login Page
def login_page():
    st.title("Login to Access Prediction App")
    username = st.text_input("Enter your username:")
    password = st.text_input("Enter your password:", type="password")
    if st.button("Login"):
        if username and password:
            st.session_state.logged_in = True
            st.session_state.user_name = username
            st.experimental_rerun()
        else:
            st.error("Please enter valid credentials.")

# Main
if st.session_state.logged_in:
    main_page()
else:
    login_page()
