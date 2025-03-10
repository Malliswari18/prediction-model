from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load trained model and label encoders
model = joblib.load("model.pkl")
encoders = joblib.load("label_encoders.pkl")

# Define categorical columns
categorical_cols = ["GENDER", "ANXIETY", "DEPRESSION", "SLEEP_ISSUES", 
                    "SOCIAL_WITHDRAWAL", "STRESS_LEVEL", "WORK_STUDY_PRESSURE",
                    "FAMILY_HISTORY", "PHYSICAL_ACTIVITY", "SOCIAL_SUPPORT"]

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json  # Get input data
        df = pd.DataFrame([data])

        # Ensure AGE is numeric
        if "AGE" in df.columns:
            df["AGE"] = pd.to_numeric(df["AGE"], errors="coerce").fillna(25)  # Default age 25 if missing

        # Encode categorical features
        for col in categorical_cols:
            if col in df.columns and col in encoders:
                df[col] = df[col].apply(lambda x: x if x in encoders[col].classes_ else encoders[col].classes_[0])
                df[col] = encoders[col].transform(df[col])

        # Make prediction
        prediction = model.predict(df)
        return jsonify({"predicted_score": int(prediction[0])})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
