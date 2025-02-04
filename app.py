import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt

# Load the pre-trained model
try:
    best_rf_model = pickle.load(open("xgb_model.pkl", "rb"))
except FileNotFoundError:
    best_rf_model = None
    st.error("Model file not found. Please ensure 'xgb_model.pkl' exists in the directory.")
except Exception as e:
    best_rf_model = None
    st.error(f"Error loading model: {e}")

# Bank class to handle transactions
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


# Initialize session state for feedback list and bank balance
if 'feedback_list' not in st.session_state:
    st.session_state.feedback_list = []

if 'bank' not in st.session_state:
    st.session_state.bank = Bank(balance=0)

# Home Page
# Home Page
def home_page():
    st.title("Welcome to Our Bank Service")
    st.header("Please log in")

    col1, col2 = st.columns(2)

    with col1:
        customer_username = st.text_input("Enter Customer Username", key="customer_username")
        customer_password = st.text_input("Enter Customer Password", type="password", key="customer_password")
        if st.button("Log In as Customer"):
            if customer_username == "customer" and customer_password == "customer123":
                st.session_state.user_type = "Customer"
                st.session_state.prediction_type = "Single"  # Default prediction type for customer
            else:
                st.error("Incorrect username or password. Please try again.")

    with col2:
        employee_username = st.text_input("Enter Employee Username", key="employee_username")
        employee_password = st.text_input("Enter Employee Password", type="password", key="employee_password")
        if st.button("Log In as Employee"):
            if employee_username == "admin" and employee_password == "admin123":
                st.session_state.user_type = "Employee"
                st.session_state.prediction_type = "Single"  # Default prediction type for employee
            else:
                st.error("Incorrect username or password. Please try again.")


# Customer Page
def customer_page():
    st.title("Customer Page")
    st.header("Welcome to Your Bank Account!")

    # Select Action in two columns
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Transactions"):
            st.session_state.transition = "Transactions"  # Set transition to transactions
            
    with col2:
        if st.button("Submit Feedback"):
            st.session_state.transition = "Feedback"  # Set transition to feedback

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
            # Storing feedback with rating properly
            st.session_state.feedback_list.append((name, feedback, rating))
            st.success(f"Feedback submitted successfully! Rating: {rating}/5")
            
            # Display the thank you message
            st.info("Thank you for your feedback! We will work on it.")
            
            # Optionally reset form (if you want to clear the inputs)
            # st.session_state.transition = None  # Uncomment this line if needed

        else:
            st.error("Please provide your name and feedback.")


# Employee Page Function
def employee_page():
    st.title("Employee Page")
    st.header("Welcome to the Employee Dashboard!")

    prediction_type = st.radio("Select Prediction Type", ["Single", "Group"], horizontal=True)

    if prediction_type == "Single":
        st.info("Provide Customer Details for Prediction")
        customer_age = st.number_input("Customer Age", min_value=18, max_value=100, value=30)
        credit_limit = st.number_input("Credit Limit", min_value=0, value=7000)
        total_transactions_count = st.number_input("Total Transactions Count", min_value=0, value=50)
        total_transaction_amount = st.number_input("Total Transaction Amount", min_value=0, value=5000)
        inactive_months_12_months = st.number_input("Inactive Months (12 Months)", min_value=0, max_value=12, value=2)
        transaction_count_change_q4_q1 = st.number_input("Transaction Count Change (Q4-Q1)", min_value=0.0, value=0.5)
        total_products_used = st.number_input("Total Products Used", min_value=1, value=2)
        average_credit_utilization = st.number_input("Average Credit Utilization", min_value=0.0, max_value=1.0, value=0.2)
        customer_contacts_12_months = st.number_input("Customer Contacts in 12 Months", min_value=0, value=1)
        transaction_amount_change_q4_q1 = st.number_input("Transaction Amount Change (Q4-Q1)", min_value=0.0, value=0.5)
        months_as_customer = st.number_input("Months as Customer", min_value=1, value=12)

        education = st.selectbox("Select Education Level", ["College", "Doctorate", "Graduate", "High School", "Post-Graduate", "Uneducated"])
        income = st.selectbox("Select Income Range", ["$120K +", "$40K - $60K", "$60K - $80K", "$80K - $120K", "Less than $40K"])

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
            "College": [1 if education == "College" else 0],
            "Doctorate": [1 if education == "Doctorate" else 0],
            "Graduate": [1 if education == "Graduate" else 0],
            "High School": [1 if education == "High School" else 0],
            "Post-Graduate": [1 if education == "Post-Graduate" else 0],
            "Uneducated": [1 if education == "Uneducated" else 0],
            "$120K +": [1 if income == "$120K +" else 0],
            "$40K - $60K": [1 if income == "$40K - $60K" else 0],
            "$60K - $80K": [1 if income == "$60K - $80K" else 0],
            "$80K - $120K": [1 if income == "$80K - $120K" else 0],
            "Less than $40K": [1 if income == "Less than $40K" else 0],
        }
        input_df = pd.DataFrame(input_data)

        if st.button("Predict for Single Customer"):
            if best_rf_model:
                try:
                    prediction = best_rf_model.predict(input_df)

                    # Display prediction result
                    if prediction[0] == 1:
                        st.markdown(f"### Prediction: Customer is likely to attrit ✅")
                        st.subheader("Attrition Risk Insights:")
                        st.write(f"- Inactive Months (12 months): {inactive_months_12_months} months")
                        st.write(f"- Transaction Amount Change (Q4-Q1): {transaction_amount_change_q4_q1}")
                        st.write(f"- Total Products Used: {total_products_used}")
                        st.write(f"- Total Transactions Count: {total_transactions_count}")
                        st.write(f"- Average Credit Utilization: {average_credit_utilization}")
                        st.write(f"- Customer Contacts in 12 Months: {customer_contacts_12_months}")
                    else:
                        st.markdown(f"### Prediction: Customer is unlikely to attrit ❌")
                        st.subheader("Non-Attrition Insights:")
                        st.write(f"- Inactive Months (12 months): {inactive_months_12_months} months")
                        st.write(f"- Transaction Amount Change (Q4-Q1): {transaction_amount_change_q4_q1}")
                        st.write(f"- Total Products Used: {total_products_used}")
                        st.write(f"- Total Transactions Count: {total_transactions_count}")
                        st.write(f"- Average Credit Utilization: {average_credit_utilization}")
                        st.write(f"- Customer Contacts in 12 Months: {customer_contacts_12_months}")
                except Exception as e:
                    st.error(f"Error during prediction: {e}")
            else:
                st.error("Model is not loaded. Please check the model file.")

    elif prediction_type == "Group":
        uploaded_file = st.file_uploader("Upload a CSV File for Group Prediction", type=["csv"])
        if uploaded_file:
            try:
                group_data = pd.read_csv(uploaded_file)
                st.write("Data Preview:")
                st.dataframe(group_data)

                if st.button("Predict for Group Customers"):
                    if best_rf_model:
                        try:
                            predictions = best_rf_model.predict(group_data)
                            group_data["Prediction"] = predictions

                            # Count the number of attritions and non-attritions
                            prediction_counts = group_data["Prediction"].value_counts()
                            labels = ["Unlikely to Attrit", "Likely to Attrit"]
                            sizes = [prediction_counts.get(0, 0), prediction_counts.get(1, 0)]

                            # Display a pie chart
                            fig, ax = plt.subplots()
                            ax.pie(
                                sizes,
                                labels=labels,
                                autopct='%1.1f%%',
                                startangle=90,
                                colors=["#4CAF50", "#F44336"],
                            )
                            ax.axis("equal")  # Equal aspect ratio ensures the pie chart is circular.
                            st.pyplot(fig)

                            st.success("Predictions generated successfully!")

                            # Allow the user to download predictions as CSV
                            csv = group_data.to_csv(index=False).encode('utf-8')
                            st.download_button(label="Download Predictions as CSV", data=csv, file_name="predictions.csv")

                        except Exception as e:
                            st.error(f"Error during group prediction: {e}")
                    else:
                        st.error("Model is not loaded. Please check the model file.")
            except Exception as e:
                st.error(f"Error reading the uploaded file: {e}")

# Main function to run the app
def main():
    if 'user_type' not in st.session_state:
        st.session_state.user_type = None

    if st.session_state.user_type == "Customer":
        customer_page()
    elif st.session_state.user_type == "Employee":
        employee_page()
    else:
        home_page()

if __name__ == "__main__":
    main()
