from flask import Flask, request, jsonify
from flask_cors import CORS
from dataset import Dataset, ColumnMeta
from k_anonymity import KAnonymity
from algorithms.ola import OLA

app = Flask(__name__)
app.json.sort_keys = False
CORS(app)

@app.post("/anonymize")
def anonymize():
    body = request.json

    rows = body["dataset"]
    metadata = [ColumnMeta(**m) for m in body["metadata"]]

    dataset = Dataset(rows, metadata)
    k = KAnonymity(dataset)
    ola = OLA(k)

    solutions = ola.run()
    best_levels = solutions[0] if solutions else k.upper_bounds
    anonymized_data = dataset.generalize_dataset(best_levels)

    return jsonify({"dataset": anonymized_data})

if __name__ == "__main__":
    app.run(debug=True)