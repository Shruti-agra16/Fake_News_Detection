"""from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app)

model = joblib.load("fake_news_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    text = data["news"]

    vect = vectorizer.transform([text])
    pred = model.predict(vect)[0]

    return jsonify({"result": "REAL" if pred == 1 else "FAKE"})

if __name__ == "__main__":
    app.run(debug=True)"""


from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from datetime import datetime
import csv
import os

app = Flask(__name__)
CORS(app)

model = joblib.load("fake_news_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

FILE_NAME = "predictions.csv"

# Create CSV file with header if it doesn't exist
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["DateTime", "News", "Prediction"])

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    text = data["news"]

    vect = vectorizer.transform([text])
    pred = model.predict(vect)[0]

    result = "REAL" if pred == 1 else "FAKE"

    # Save news and prediction
    with open(FILE_NAME, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), text, result])

    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)
