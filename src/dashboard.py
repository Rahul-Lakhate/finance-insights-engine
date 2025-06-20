import streamlit as st
import pandas as pd
import plotly.express as px
from parser import load_statement
from categorizer import predict_categories
from insights import monthly_summary, top_expenses, recurring_transactions, detect_anomalies

st.set_page_config(page_title="Personal Finance Insights", layout="wide")
st.title("📊 Personal Finance Insights Engine")

uploaded_file = st.file_uploader("Upload your bank statement (.pdf or .csv)", type=["pdf", "csv"])

if uploaded_file:
    with st.spinner("📂 Processing your statement..."):
        try:
            df = load_statement(uploaded_file)
        except Exception as e:
            st.error(f"❌ Failed to load file: {e}")
            st.stop()

        if df.empty or 'Description' not in df.columns or 'Amount' not in df.columns:
            st.error("❌ File format not supported or no transactions extracted. Please upload a valid bank statement.")
            st.stop()

        try:
            df = predict_categories(df)
        except Exception as e:
            st.error(f"❌ Categorization failed: {e}")
            st.stop()

        st.success("✅ Transactions successfully processed!")

        # 📄 Raw Transactions
        st.subheader("🔍 Preview of Transactions")
        st.dataframe(df.head(10), use_container_width=True)

        # 📊 Monthly Summary
        st.subheader("📅 Monthly Summary by Category")
        summary = monthly_summary(df)
        st.dataframe(summary, use_container_width=True)

        # 📊 Monthly Spending Bar Chart
        st.subheader("📊 Monthly Spending Trends")
        df['Month'] = df['Date'].dt.to_period('M').astype(str)
        grouped = df.groupby(['Month', 'Category'])['Amount'].sum().reset_index()
        grouped['Amount'] = grouped['Amount'].abs()

        fig1 = px.bar(
            grouped,
            x="Month",
            y="Amount",
            color="Category",
            barmode="stack",
            title="Monthly Spend by Category",
            labels={"Amount": "₹ Amount"},
            height=400
        )
        st.plotly_chart(fig1, use_container_width=True)

        # 🍩 Category Distribution Donut Chart
        st.subheader("🍩 Spending by Category")
        cat_totals = df.groupby("Category")["Amount"].sum().abs().reset_index()

        fig2 = px.pie(
            cat_totals,
            names="Category",
            values="Amount",
            hole=0.4,
            title="Spending Breakdown by Category",
            height=400
        )
        st.plotly_chart(fig2, use_container_width=True)

        # 💸 Top Expenses
        st.subheader("💸 Top Expenses")
        top = top_expenses(df)
        st.dataframe(top, use_container_width=True)

        # 🔁 Recurring Transactions
        st.subheader("🔁 Recurring Transactions")
        recurring = recurring_transactions(df)
        st.dataframe(recurring, use_container_width=True)

        # 🚨 Anomaly Detection
        st.subheader("🚨 Anomaly Detection")
        anomalies = detect_anomalies(df)
        st.dataframe(anomalies, use_container_width=True)

        # ⬇️ Download
        st.download_button(
            label="⬇️ Download Categorized CSV",
            data=df.to_csv(index=False),
            file_name="categorized_transactions.csv",
            mime="text/csv"
        )
else:
    st.info("📥 Please upload a PDF or CSV bank statement to get started.")
