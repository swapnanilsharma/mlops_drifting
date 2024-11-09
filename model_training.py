import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Load the training and production data
train_data = pd.read_csv("training_data.csv")
prod_data = pd.read_csv("production_data.csv")
ground_truth_data = pd.read_csv("ground_truth_data.csv")

# Step 1: Merge ground_truth_data with prod_data to add the 'Churn' column for evaluation
prod_data_with_truth = pd.merge(
    prod_data, ground_truth_data, on="customerID", how="left"
)

# Step 2: Preprocess categorical data for both train_data and prod_data_with_truth
# Drop the 'customerID' column as it does not provide predictive value
train_data = train_data.drop(columns=["customerID"])
prod_data_with_truth = prod_data_with_truth.drop(columns=["customerID"])

# Convert 'TotalCharges' to numeric for both datasets
train_data["TotalCharges"] = pd.to_numeric(
    train_data["TotalCharges"], errors="coerce"
).fillna(0)
prod_data_with_truth["TotalCharges"] = pd.to_numeric(
    prod_data_with_truth["TotalCharges"], errors="coerce"
).fillna(0)

# Ensure both datasets have the same columns by reindexing prod_data_encoded
prod_data_with_truth = prod_data_with_truth.reindex(
    columns=train_data.columns, fill_value=0
)

prod_data_encoded = pd.get_dummies(
    prod_data_with_truth,
    columns=[
        "gender",
        "Partner",
        "Dependents",
        "PhoneService",
        "MultipleLines",
        "InternetService",
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies",
        "Contract",
        "PaperlessBilling",
        "PaymentMethod",
    ],
)
train_data_encoded = pd.get_dummies(
    train_data,
    columns=[
        "gender",
        "Partner",
        "Dependents",
        "PhoneService",
        "MultipleLines",
        "InternetService",
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies",
        "Contract",
        "PaperlessBilling",
        "PaymentMethod",
    ],
)
prod_data_encoded["Churn"] = prod_data_with_truth["Churn"].apply(
    lambda x: 1 if x == "Yes" else 0
)
train_data_encoded["Churn"] = train_data["Churn"].apply(
    lambda x: 1 if x == "Yes" else 0
)


# Define the target and feature columns for training
target_column = "Churn"
feature_columns = train_data_encoded.columns.drop([target_column])

# Train a model
model = RandomForestClassifier()
model.fit(train_data_encoded[feature_columns], train_data_encoded[target_column])

# Generate predictions on the production data and add required columns
prod_data_encoded["prediction"] = model.predict(prod_data_encoded[feature_columns])
prod_data_encoded["target"] = prod_data_encoded[target_column]
train_data_encoded["prediction"] = model.predict(train_data_encoded[feature_columns])
train_data_encoded["target"] = train_data_encoded[target_column]


train_data_encoded.to_csv("train_data_encoded.csv", index=False)
prod_data_encoded.to_csv("prod_data_encoded.csv", index=False)
