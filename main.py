# https://youtu.be/pI0wQbJwIIs
"""
For training, watch videos (202 and 203): 
    https://youtu.be/qB6h5CohLbs
    https://youtu.be/fyZ9Rxpoz2I

The 7 classes of skin cancer lesions included in this dataset are:
Melanocytic nevi (nv)
Melanoma (mel)
Benign keratosis-like lesions (bkl)
Basal cell carcinoma (bcc) 
Actinic keratoses (akiec)
Vascular lesions (vas)
Dermatofibroma (df)

"""



import numpy as np
from PIL import Image
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import load_model

# Load model once
my_model = load_model("model/HAM10000_100epochs.h5")

# Define classes
classes = ['Actinic keratoses', 'Basal cell carcinoma', 
           'Benign keratosis-like lesions', 'Dermatofibroma', 'Melanoma', 
           'Melanocytic nevi', 'Vascular lesions']
le = LabelEncoder()
le.fit(classes)

# Set confidence threshold (e.g., 0.7 or 70%)
CONFIDENCE_THRESHOLD = 0.68

def getPrediction(filename):
    # Load and preprocess image
    SIZE = 32
    img_path = f'static/images/{filename}'
    img = np.asarray(Image.open(img_path).resize((SIZE, SIZE)))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    # Get prediction and confidence
    pred = my_model.predict(img)
    max_confidence = np.max(pred)
    pred_class = le.inverse_transform([np.argmax(pred)])[0]

    # Check confidence threshold
    if max_confidence < CONFIDENCE_THRESHOLD:
        return {"prediction": "No skin cancer detected"}
    else:
        return {"prediction": pred_class, "confidence": f"{max_confidence * 100:.2f}%"}

