import pickle

# Load label encoders
with open("label_encoders.pkl", "rb") as f:
    label_encoders = pickle.load(f)

# Print all categories seen during training
for col, encoder in label_encoders.items():
    print(f"Column: {col}, Categories: {list(encoder.classes_)}")
