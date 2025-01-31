import random
import streamlit as st
import pandas as pd
import joblib

# Load the trained model
best_rf_model = joblib.load('best_rf_model.pkl')

# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "account_type" not in st.session_state:
    st.session_state.account_type = ""
if "email" not in st.session_state:
    st.session_state.email = ""

# Login Page
def login_page():
    st.markdown("<h1 style='text-align: center;'>Customer <span style='color: red;'>Attrition </span> - Login</h1>", unsafe_allow_html=True)
    
    # User Name
    user_name = st.text_input("Enter your name:")
    
    # Account Type: Saving or Current
    account_type = st.selectbox("Select Account Type", ["Saving", "Current"])
    
    # Email Address (optional)
    email = st.text_input("Enter your email (optional):")
    
    login_button = st.button("Log In")

    if login_button:
        if user_name.strip():
            # Store additional information in session state
            st.session_state.logged_in = True
            st.session_state.user_name = user_name.strip()
            st.session_state.account_type = account_type
            st.session_state.email = email.strip()
            st.experimental_rerun()  # Refresh to show main page
        else:
            st.error("Name cannot be empty.")

# Customer Feedback Data
positive_feedback = [
    "Excellent customer service and great support!",
    "I'm extremely satisfied with the features offered.",
    "The app is user-friendly and intuitive.",
    "Timely communication from the service team.",
    "Reliable and secure platform for transactions.",
    "Quick response to queries and issues.",
    "Very happy with the product offerings.",
    "Affordable plans and great discounts.",
    "Highly recommended for smooth operations.",
    "A pleasant experience using the service."
]

negative_feedback = [
    "Customer service response is too slow.",
    "The platform crashes frequently.",
    "Hidden charges are frustrating.",
    "Difficult to navigate the website.",
    "Long waiting times for support.",
    "Billing issues need to be resolved.",
    "Product availability is limited.",
    "Lack of proper communication channels.",
    "Refunds take too long to process.",
    "Not enough transparency in pricing."
]

def display_feedback(prediction):
    if prediction == 1:  # Customer likely to attrit (Churn)
        feedback_to_show = random.sample(negative_feedback, 3) + random.sample(positive_feedback, 1)
        st.subheader("Customer Sentiment Insights (Churn Prediction)")
    else:  # Customer unlikely to attrit (Stay)
        feedback_to_show = random.sample(positive_feedback, 3) + random.sample(negative_feedback, 1)
        st.subheader("Customer Sentiment Insights (Stay Prediction)")

    st.markdown("### **Customer Feedback:**")
    for feedback in feedback_to_show:
        st.write(f"- {feedback}")

# File Upload and Processing
def process_uploaded_file(uploaded_file):
    # Read the uploaded file into a pandas DataFrame
    df = pd.read_csv(uploaded_file)
    
    # Ensure required columns are in the file (this should match your input features)
    required_columns = [
        "Customer_Age", "Credit_Limit", "Total_Transactions_Count", "Total_Transaction_Amount",
        "Inactive_Months_12_Months", "Transaction_Count_Change_Q4_Q1", "Total_Products_Used",
        "Average_Credit_Utilization", "Customer_Contacts_12_Months", "Transaction_Amount_Change_Q4_Q1",
        "Months_as_Customer", "Education", "Income"
    ]
    
    for col in required_columns:
        if col not in df.columns:
            st.error(f"Missing required column: {col}")
            return None

    # Map categorical variables (Education and Income) to one-hot encoded columns
    df["College"] = df["Education"].apply(lambda x: 1 if x == "College" else 0)
    df["Doctorate"] = df["Education"].apply(lambda x: 1 if x == "Doctorate" else 0)
    df["Graduate"] = df["Education"].apply(lambda x: 1 if x == "Graduate" else 0)
    df["High School"] = df["Education"].apply(lambda x: 1 if x == "High School" else 0)
    df["Post-Graduate"] = df["Education"].apply(lambda x: 1 if x == "Post-Graduate" else 0)
    df["Uneducated"] = df["Education"].apply(lambda x: 1 if x == "Uneducated" else 0)
    
    df["$120K +"] = df["Income"].apply(lambda x: 1 if x == "$120K +" else 0)
    df["$40K - $60K"] = df["Income"].apply(lambda x: 1 if x == "$40K - $60K" else 0)
    df["$60K - $80K"] = df["Income"].apply(lambda x: 1 if x == "$60K - $80K" else 0)
    df["$80K - $120K"] = df["Income"].apply(lambda x: 1 if x == "$80K - $120K" else 0)
    df["Less than $40K"] = df["Income"].apply(lambda x: 1 if x == "Less than $40K" else 0)
    
    # Select only the relevant columns
    df = df[required_columns]

    # Predictions
    predictions = best_rf_model.predict(df)

    # Show predictions for each customer
    for idx, prediction in enumerate(predictions):
        st.write(f"Customer {idx + 1} Prediction: {'Attrit' if prediction == 1 else 'Stay'}")
        display_feedback(prediction)

# Main App Page
def main_page():
    st.title("Customer Attrition Prediction")
    st.sidebar.header(f"Welcome, {st.session_state.user_name}")

    # Sidebar Inputs
    st.sidebar.header('Input Data')
    uploaded_file = st.sidebar.file_uploader("Upload a CSV file with customer data", type=["csv"])

    if uploaded_file:
        process_uploaded_file(uploaded_file)

# App Navigation
if not st.session_state.logged_in:
    login_page()
else:
    main_page()
