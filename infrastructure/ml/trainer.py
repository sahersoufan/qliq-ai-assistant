from pathlib import Path

import pandas as pd
import numpy as np
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import os

# Constants
base_dir = Path(__file__).resolve().parents[2]
data_path = base_dir / "data/query_dataset.csv"
model_path = base_dir / "infrastructure/ml/query_classifier_model.pkl"
report_path = base_dir / "infrastructure/ml/query_classifier_report.txt"


def load_data(path: str):
    df_load = pd.read_csv(path)
    df_load = df_load.dropna(subset=["text", "label"])
    return df_load


def train_model(df: pd.DataFrame):
    X = df["text"]
    y = df["label"]
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("clf", LogisticRegression(max_iter=1000, solver='liblinear'))
    ], memory=None)

    pipeline.fit(x_train, y_train)
    y_pred = pipeline.predict(x_test)

    report = classification_report(y_test, y_pred, digits=4)
    matrix = confusion_matrix(y_test, y_pred)

    print("\nClassification Report:\n", report)
    print("\nConfusion Matrix:\n", matrix)

    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(pipeline, model_path)

    with open(report_path, "w") as f:
        f.write("Classification Report:\n")
        f.write(report)
        f.write("\nConfusion Matrix:\n")
        f.write(np.array2string(matrix))

    return pipeline


if __name__ == "__main__":
    df = load_data(data_path)
    train_model(df)
