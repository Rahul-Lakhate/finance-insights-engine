import os
import re
import pandas as pd
import pdfplumber
from io import BytesIO


def extract_text_from_pdf(file_obj):
    text = ""
    with pdfplumber.open(file_obj) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def parse_transactions(text):
    # Very basic regex pattern — customize for your bank's format
    transaction_pattern = re.compile(r"(\d{2}/\d{2}/\d{4})\s+(.+?)\s+(-?\d+\.\d{2})")
    matches = transaction_pattern.findall(text)

    data = []
    for date, description, amount in matches:
        data.append({
            "Date": pd.to_datetime(date, dayfirst=True, errors='coerce'),
            "Description": description.strip(),
            "Amount": float(amount)
        })

    df = pd.DataFrame(data)
    return df.dropna()


def load_statement(file_input):
    # Handle both file paths and UploadedFile objects
    if hasattr(file_input, 'name'):  # Streamlit UploadedFile
        ext = os.path.splitext(file_input.name)[1].lower()
    else:  # string file path
        ext = os.path.splitext(str(file_input))[1].lower()

    if ext == ".pdf":
        return parse_transactions(extract_text_from_pdf(file_input))
    elif ext == ".csv":
        return pd.read_csv(file_input)
    else:
        raise ValueError("Unsupported file format: only .pdf and .csv supported")


if __name__ == "__main__":
    sample_file = "data/sample_statement.pdf"
    with open(sample_file, "rb") as f:
        df = load_statement(f)
    print(df.head())
