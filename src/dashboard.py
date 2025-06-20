# src/dashboard.py

import streamlit as st
import pandas as pd
from parser import load_statement
from categorizer import predict_categories
from insights import monthly_summary, top_expenses, recurring_transactions, detect_anomalies

st.set_page_config(page_title="Personal Finance Insights", layout="wide")

st.title("📊 Personal Finance Insights Engine")

uploaded_file = st.file_uploader("Upload Bank Statement (.pdf or .csv)", type=["pdf", "csv"])

if uploaded_file:
    with st.spinner("Processing..."):
        df = load_statement(uploaded_file)
        df = predict_categories(df)

        st.subheader("📄 Raw Transactions")
        st.dataframe(df.head(10))

        st.subheader("📅 Monthly Summary")
        monthly = monthly_summary(df)
        st.dataframe(monthly)

        st.subheader("💸 Top Expenses")
        top = top_expenses(df)
        st.dataframe(top)

        st.subheader("🔁 Recurring Transactions")
        recurring = recurring_transactions(df)
        st.dataframe(recurring)

        st.subheader("🚨 Anomaly Detection")
        anomalies = detect_anomalies(df)
        st.dataframe(anomalies)

        st.download_button("Download Categorized CSV", data=df.to_csv(index=False), file_name="categorized_transactions.csv", mime="text/csv")
else:
    st.info("Upload a PDF or CSV bank statement to begin.")
