from prometheus_client import start_http_server, Gauge
import time
import json

# Define custom gauges for metrics
data_drift_gauge = Gauge("data_drift_score", "Data Drift Score")
accuracy_gauge = Gauge("model_accuracy", "Model Accuracy")


def load_metrics():
    # Load metrics from JSON files
    try:
        with open("data_drift_report.json", "r") as drift_file:
            data_drift_report = json.load(drift_file)

        with open("performance_report.json", "r") as perf_file:
            performance_report = json.load(perf_file)

        # Extract specific metrics
        # Here we assume a structure in the JSON output; update paths as per your JSON structure
        data_drift_score = data_drift_report["metrics"][1]["result"][
            "drift_by_columns"
        ]["target"]["drift_score"]
        accuracy = performance_report["metrics"][0]["result"]["current"][
            "accuracy"
        ]

        return data_drift_score, accuracy

    except FileNotFoundError:
        print(
            "JSON files not found. Ensure 'data_drift_report.json' and 'performance_report.json' are available."
        )
        return None, None


def push_metrics():
    # Load Evidently metrics from JSON files
    data_drift_score, accuracy = load_metrics()

    # Update Prometheus Gauges if metrics are loaded
    if data_drift_score is not None and accuracy is not None:
        data_drift_gauge.set(data_drift_score)
        accuracy_gauge.set(accuracy)


if __name__ == "__main__":
    # Start the Prometheus HTTP server on port 8000
    start_http_server(8000)
    while True:
        push_metrics()
        time.sleep(2)  # Push metrics every 60 seconds
