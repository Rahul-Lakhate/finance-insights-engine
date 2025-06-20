# src/insights.py

import pandas as pd


def monthly_summary(df):
    df['Month'] = df['Date'].dt.to_period('M')
    summary = df.groupby(['Month', 'Category'])['Amount'].sum().unstack(fill_value=0)
    return summary


def top_expenses(df, top_n=5):
    expenses = df[df['Amount'] < 0].copy()
    expenses['AbsAmount'] = expenses['Amount'].abs()
    return expenses.nlargest(top_n, 'AbsAmount')[['Date', 'Description', 'Amount']]


def recurring_transactions(df, min_occurrences=3):
    recurring = df.groupby('Description').filter(lambda x: len(x) >= min_occurrences)
    return recurring.sort_values(['Description', 'Date'])


def detect_anomalies(df, threshold=2.5):
    df = df.copy()
    df['ZScore'] = (df['Amount'] - df['Amount'].mean()) / df['Amount'].std()
    return df[df['ZScore'].abs() > threshold][['Date', 'Description', 'Amount', 'ZScore']]


if __name__ == "__main__":
    sample_file = "../data/sample_categorized.csv"
    df = pd.read_csv(sample_file, parse_dates=['Date'])
    print("\nMonthly Summary:")
    print(monthly_summary(df))
    print("\nTop Expenses:")
    print(top_expenses(df))
    print("\nRecurring Transactions:")
    print(recurring_transactions(df))
    print("\nAnomalies:")
    print(detect_anomalies(df))
