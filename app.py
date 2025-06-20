# app.py

import argparse
import pandas as pd
from src.parser import load_statement
from src.categorizer import predict_categories
from src.insights import monthly_summary, top_expenses, recurring_transactions, detect_anomalies

def main(file_path):
    print(f"🔍 Loading statement from: {file_path}")
    df = load_statement(file_path)
    
    print("🧠 Categorizing transactions...")
    df = predict_categories(df)
    
    print("\n📅 Monthly Summary:")
    print(monthly_summary(df))
    
    print("\n💸 Top Expenses:")
    print(top_expenses(df))
    
    print("\n🔁 Recurring Transactions:")
    print(recurring_transactions(df))
    
    print("\n🚨 Anomalies Detected:")
    print(detect_anomalies(df))

    # Save categorized version
    output_path = "output_categorized.csv"
    df.to_csv(output_path, index=False)
    print(f"\n✅ Saved categorized transactions to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Personal Finance Insights Engine")
    parser.add_argument("filepath", help="Path to bank statement (.pdf or .csv)")
    args = parser.parse_args()

    main(args.filepath)

