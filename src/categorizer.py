# src/categorizer.py

import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import joblib


# Sample rule-based fallback categories
CATEGORY_KEYWORDS = {
    "Food": ["swiggy", "zomato", "restaurant", "cafe"],
    "Transport": ["uber", "ola", "fuel", "metro"],
    "Groceries": ["bigbasket", "grofers", "supermarket"],
    "Salary": ["salary", "credited", "payroll"],
    "Rent": ["rent", "lease"],
    "Utilities": ["electricity", "water", "bill", "internet"],
    "Entertainment": ["netflix", "prime", "hotstar", "bookmyshow"]
}


def rule_based_categorization(description):
    desc = description.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in desc for keyword in keywords):
            return category
    return "Others"


def train_transaction_classifier(df, model_path="models/transaction_classifier.pkl"):
    df = df.copy()
    if 'Category' not in df.columns:
        raise ValueError("Training requires a 'Category' column in the DataFrame.")

    X_train, X_test, y_train, y_test = train_test_split(df['Description'], df['Category'], test_size=0.2, random_state=42)

    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', MultinomialNB())
    ])

    pipeline.fit(X_train, y_train)
    joblib.dump(pipeline, model_path)
    return pipeline


def load_classifier(model_path="models/transaction_classifier.pkl"):
    return joblib.load(model_path)


def predict_categories(df, model_path="models/transaction_classifier.pkl"):
    if not os.path.exists(model_path):
        df['Category'] = df['Description'].apply(rule_based_categorization)
    else:
        model = load_classifier(model_path)
        df['Category'] = model.predict(df['Description'])
    return df
