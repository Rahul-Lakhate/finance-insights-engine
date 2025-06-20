import os
import re
import pandas as pd
import pdfplumber


def extract_text_from_pdf(file_obj):
    text = ""
    with pdfplumber.open(file_obj) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def parse_transactions(text):
    # Updated regex for IDFC bank statement format:
    # Format: 01-Dec-2024 01-Dec-2024 Description Debit Credit Balance
    pattern = re.compile(
        r"(\d{2}-[A-Za-z]{3}-\d{4})\s+"              # Transaction Date
        r"(\d{2}-[A-Za-z]{3}-\d{4})\s+"              # Value Date
        r"(.+?)\s+"                                   # Description
        r"((?:\d{1,3}(?:,\d{3})*|\d+)?(?:\.\d{2})?)?\s+"  # Debit (optional)
        r"((?:\d{1,3}(?:,\d{3})*|\d+)?(?:\.\d{2})?)?\s+"  # Credit (optional)
        r"(\d{1,3}(?:,\d{3})*(?:\.\d{2}))"                # Balance
    )

    matches = pattern.findall(text)
    data = []

    for tx_date, val_date, desc, debit, credit, _balance in matches:
        try:
            if credit and credit.strip():
                amount = float(credit.replace(",", ""))
            elif debit and debit.strip():
                amount = -float(debit.replace(",", ""))
            else:
                continue  # Skip if both debit and credit are missing

            data.append({
                "Date": pd.to_datetime(tx_date, format="%d-%b-%Y"),
                "Description": desc.strip(),
                "Amount": amount
            })
        except Exception as e:
            print(f"Skipping row due to error: {e}")

    return pd.DataFrame(data)


def load_statement(file_input):
    if hasattr(file_input, 'name'):
        ext = os.path.splitext(file_input.name)[1].lower()
    else:
        ext = os.path.splitext(str(file_input))[1].lower()

    if ext == ".pdf":
        text = extract_text_from_pdf(file_input)
        df = parse_transactions(text)
    elif ext == ".csv":
        df = pd.read_csv(file_input)
    else:
        raise ValueError("Unsupported file format: only .pdf and .csv supported")

    # Fallback if parsing failed
    if df.empty or 'Description' not in df.columns or 'Amount' not in df.columns:
        print("⚠️ No valid transactions found. Check file format.")
        df = pd.DataFrame(columns=["Date", "Description", "Amount"])

    return df


if __name__ == "__main__":
    with open("data/sample_idfc_statement.pdf", "rb") as f:
        df = load_statement(f)
        print(df.head())
