import streamlit as st
import pandas as pd
from parser import load_statement
from categorizer import predict_categories
from insights import monthly_summary, top_expenses, recurring_transactions, detect_anomalies

st.set_page_config(page_title="Personal Finance Insights", layout="wide")
st.title("📊 Personal Finance Insights Engine")

# Upload section
uploaded_file = st.file_uploader("Upload your bank statement (.pdf or .csv)", type=["pdf", "csv"])

if uploaded_file:
    with st.spinner("📂 Processing your statement..."):
        df = load_statement(uploaded_file)
        df = predict_categories(df)

        st.success("✅ Transactions successfully processed!")

        # Section 1: Raw Data
        st.subheader("🔍 Preview of Transactions")
        st.dataframe(df.head(10), use_container_width=True)

        # Section 2: Monthly Summary
        st.subheader("📅 Monthly Summary by Category")
        summary = monthly_summary(df)
        st.dataframe(summary, use_container_width=True)

        # Section 3: Top Expenses
        st.subheader("💸 Top Expenses")
        top = top_expenses(df)
        st.dataframe(top, use_container_width=True)

        # Section 4: Recurring Transactions
        st.subheader("🔁 Recurring Transactions")
        recurring = recurring_transactions(df)
        st.dataframe(recurring, use_container_width=True)

        # Section 5: Anomaly Detection
        st.subheader("🚨 Anomaly Detection")
        anomalies = detect_anomalies(df)
        st.dataframe(anomalies, use_container_width=True)

        # Download categorized CSV
        st.download_button(
            label="⬇️ Download Categorized CSV",
            data=df.to_csv(index=False),
            file_name="categorized_transactions.csv",
            mime="text/csv"
        )
else:
    st.info("Please upload a PDF or CSV bank statement to get started.")
