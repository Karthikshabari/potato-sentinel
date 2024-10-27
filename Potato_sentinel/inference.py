import os
import sys
import importlib
import tensorflow as tf
import joblib
import numpy as np

# Remap keras.src to keras
sys.modules['keras.src'] = importlib.import_module('keras')

# Load the models and scaler using relative paths
current_dir = os.path.dirname(__file__)

# Update the path to ensemble_model.keras
ensemble_model_path = os.path.join(current_dir, 'ensemble_model.keras')
ensemble_model = tf.keras.models.load_model(ensemble_model_path)

# Load the scaler and random forest model
rf_model = joblib.load(os.path.join(current_dir, 'rf_model.pkl'))
scaler = joblib.load(os.path.join(current_dir, 'scaler.pkl'))

CLASS_NAMES = ['Potato___Early_blight', 'Potato___healthy', 'Potato___Late_blight']

CLASS_DESCRIPTIONS = {
    'Potato___Early_blight': 'Early blight, caused by the fungal pathogen Alternaria solani, presents a significant challenge to potato cultivation...',
    'Potato___healthy': 'Healthy potato leaves are the hallmark of robust plant growth and development...',
    'Potato___Late_blight': 'Late blight, an exceptionally destructive disease caused by the oomycete Phytophthora infestans, is notorious...'
}

def preprocess_image(img_stream):
    img = tf.keras.preprocessing.image.load_img(img_stream, target_size=(256, 256))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predict_image(img_stream):
    img_array = preprocess_image(img_stream)
    cnn_features = ensemble_model.predict(img_array)
    rf_features = scaler.transform(cnn_features)
    rf_predictions = rf_model.predict(rf_features)
    predicted_class = CLASS_NAMES[rf_predictions[0]]
    return predicted_class

def get_class_description(predicted_class):
    """Get the description of the predicted class."""
    return CLASS_DESCRIPTIONS.get(predicted_class, "Description not available.")
