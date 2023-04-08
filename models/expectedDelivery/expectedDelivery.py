import joblib

# Load the encoder from a file
le = joblib.load('encoder.joblib')

# Load the model from a file
model = joblib.load('model.joblib')
    
def getNumberOfDays(destination_pincode):
    # make predictions using the loaded model
    source_pincode = '560068'
    source_pincode_encoded = le.transform([source_pincode])[0]
    destination_pincode_encoded = le.transform([destination_pincode])[0]
    days_pred = model.predict([[source_pincode_encoded, destination_pincode_encoded]])
    return round(days_pred[0])