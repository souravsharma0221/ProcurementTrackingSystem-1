import joblib
import numpy as np

loaded_model=joblib.load("models/review_analysis/model.pkl")
loaded_stop=joblib.load("models/review_analysis/stopwords.pkl") 
loaded_vec=joblib.load("models/review_analysis/vectorizer.pkl")

def classify(document):
    # label = {0: 'negative', 1: 'positive'}
    X = loaded_vec.transform([document])
    y = loaded_model.predict(X)[0]
    proba = np.max(loaded_model.predict_proba(X))
    return y, proba

 