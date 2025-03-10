import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load dataset
df = pd.read_csv("mental_health_data.csv")

# Standardize column names (remove spaces, convert to uppercase)
df.columns = df.columns.str.strip().str.replace(" ", "_").str.upper()

# Print final column names for confirmation
print("Updated Column Names:", df.columns.tolist())

# Fix column name typo
if "SLEEP_ISSUESS" in df.columns:
    df.rename(columns={"SLEEP_ISSUESS": "SLEEP_ISSUES"}, inplace=True)

# Drop rows with missing values
df.dropna(inplace=True)

# Encode categorical variables
label_encoders = {}
categorical_cols = ["GENDER", "ANXIETY", "DEPRESSION", "SLEEP_ISSUES", 
                    "SOCIAL_WITHDRAWAL", "STRESS_LEVEL", "WORK_STUDY_PRESSURE",
                    "FAMILY_HISTORY", "PHYSICAL_ACTIVITY", "SOCIAL_SUPPORT"]

for col in categorical_cols:
    if col in df.columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))  # Convert to string and encode
        label_encoders[col] = le  # Store encoders for later use

# Define features and target
X = df.drop(columns=["SCORE"])  # Use correct uppercase "SCORE"
y = df["SCORE"].astype(float)   # Convert target variable to float

# Split data into train & test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = DecisionTreeRegressor(random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print("\nModel Performance:")
print("Mean Absolute Error (MAE):", round(mean_absolute_error(y_test, y_pred), 4))
print("Mean Squared Error (MSE):", round(mean_squared_error(y_test, y_pred), 4))
print("R-Squared (R²):", round(r2_score(y_test, y_pred), 4))

# Save the model and encoders
with open("model.pkl", "wb") as model_file:
    pickle.dump(model, model_file)

with open("label_encoders.pkl", "wb") as encoder_file:
    pickle.dump(label_encoders, encoder_file)

print("\n✅ Model and encoders saved successfully!")
