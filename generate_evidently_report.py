import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, ClassificationPreset

# Load the training and production data
prod_data_encoded = pd.read_csv("prod_data_encoded.csv")
train_data_encoded = pd.read_csv("train_data_encoded.csv")

# Define reports for data drift and model performance
data_drift_report = Report(metrics=[DataDriftPreset()])
performance_report = Report(metrics=[ClassificationPreset()])

# Reference data: Training data, Current data: Production data
data_drift_report.run(reference_data=train_data_encoded, current_data=prod_data_encoded)
performance_report.run(
    reference_data=train_data_encoded, current_data=prod_data_encoded
)

# Export the metrics to JSON for Grafana integration
data_drift_report.save_json("data_drift_report.json")
performance_report.save_json("performance_report.json")
