# src/parser.py

import os
import re
import pandas as pd
import pdfplumber


def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


def parse_transactions(text):
    # Very basic regex pattern for demo purposes; adjust per bank format
    transaction_pattern = re.compile(r"(\d{2}/\d{2}/\d{4})\s+(.+?)\s+(-?\d+\.\d{2})")
    matches = transaction_pattern.findall(text)

    data = []
    for match in matches:
        date, description, amount = match
        data.append({
            "Date": pd.to_datetime(date, dayfirst=True, errors='coerce'),
            "Description": description.strip(),
            "Amount": float(amount)
        })

    df = pd.DataFrame(data)
    return df.dropna()


def load_statement(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        text = extract_text_from_pdf(file_path)
        return parse_transactions(text)
    elif ext == ".csv":
        return pd.read_csv(file_path)
    else:
        raise ValueError("Unsupported file format: only .pdf and .csv supported")


if __name__ == "__main__":
    sample_file = "../data/sample_statement.pdf"
    df = load_statement(sample_file)
    print(df.head())
