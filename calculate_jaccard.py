import json

def load_threats(file_path):
    with open(file_path) as f:
        data = json.load(f)
    runs = []
    for scenario in data['scenario_results']:
        # To get actual threats, we might need the raw outputs, but we only have evaluation results.
        # Wait, the evaluation results JSON doesn't contain the raw threats generated, only the metrics (tp, fp, fn, etc.).
        pass
print("Need raw outputs to calculate true Jaccard.")
