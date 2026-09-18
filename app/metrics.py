from prometheus_client import Counter


prediction_counter = Counter(
    "iris_predictions_total",
    "Total number of successful Iris predictions",
    ["prediction_class"]
)