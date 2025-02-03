import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def employee_page():
    st.title("Employee Page")
    st.header("Welcome to the Employee Dashboard!")

    # You can add additional functionality here
    st.write("Here, employees can manage bank operations.")

    # Buttons for future functionality
    if st.button("Check Customer Retention"):
        customer_retention_options()

    if st.button("Customer Feedback Analysis"):
        st.write("This feature will be developed later for analyzing customer feedback.")

    # Example: Option to log out (reset user type)
    if st.button("Log Out"):
        st.session_state.user_type = None  # Reset user type to None to go back to the home page
        st.session_state.transition = None  # Reset transition state
        home_page()  # Redirect to home page


def customer_retention_options():
    st.write("Choose an option for customer retention analysis:")
    
    # Option to select one customer or a group
    customer_choice = st.radio("Choose Customer Group:", ["One Customer", "Group of Customers"])
    
    # If "One Customer" is selected, show an upload option for a single customer's data
    if customer_choice == "One Customer":
        st.write("Please upload a CSV file for a single customer.")
        uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
        if uploaded_file is not None:
            process_uploaded_file(uploaded_file)
    
    # If "Group of Customers" is selected, show an upload option for multiple customers' data
    elif customer_choice == "Group of Customers":
        st.write("Please upload a CSV file for multiple customers.")
        uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
        if uploaded_file is not None:
            process_uploaded_file(uploaded_file)

def process_uploaded_file(uploaded_file):
    # Read the uploaded CSV file
    df = pd.read_csv(uploaded_file)

    # List of required columns for the retention prediction
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

    # Check for missing columns
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"Missing required columns: {', '.join(missing_columns)}")
        return None

    # Filter the dataframe to only include the required columns
    df = df[required_columns]
    
    # Assuming 'best_rf_model' is pre-loaded or defined elsewhere
    predictions = best_rf_model.predict(df)

    # Calculate attrition and retention counts
    attrit_count = sum(predictions)
    stay_count = len(predictions) - attrit_count

    # Plot Pie Chart with styling improvements
    fig, ax = plt.subplots(figsize=(8, 8))

    # Custom color palette
    colors = ["#66b3ff", "#ff6666"]

    # Create the pie chart with better styling
    wedges, texts, autotexts = ax.pie([stay_count, attrit_count], labels=["Stay", "Leave"], autopct='%1.1f%%', colors=colors,
                                      startangle=90, wedgeprops={"edgecolor": "black", "linewidth": 1.5, "linestyle": "solid"})
    
    # Add shadow for depth
    ax.pie([stay_count, attrit_count], labels=["Stay", "Leave"], autopct='%1.1f%%', colors=colors,
           startangle=90, wedgeprops={"edgecolor": "black", "linewidth": 1.5, "linestyle": "solid"}, shadow=True)

    # Title and font styling
    ax.set_title("Customer Attrition Distribution", fontsize=16, fontweight="bold", color="darkblue")

    # Style the labels and percentages for readability
    for text in texts:
        text.set_fontsize(14)
        text.set_fontweight("bold")
        text.set_color("black")
        
    for autotext in autotexts:
        autotext.set_fontsize(12)
        autotext.set_fontweight("bold")
        autotext.set_color("white")
    
    # Set aspect ratio to make sure pie is circular
    ax.axis('equal')

    # Show the chart
    st.pyplot(fig)

    # Show predictions for each customer
    for idx, prediction in enumerate(predictions):
        st.write(f"Customer {idx + 1} Prediction: {'Stay' if prediction == 0 else 'Leave'}")
