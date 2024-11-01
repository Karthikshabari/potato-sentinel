#!/usr/bin/env python
# coding: utf-8

import joblib
import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import models, layers
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

# Suppress TensorFlow oneDNN warnings and configure for CPU
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Constants
IMAGE_SIZE = 256
BATCH_SIZE = 32
EPOCHS = 5
CHANNELS = 3
CLASS_NAMES = ['Potato___Early_blight', 'Potato___healthy', 'Potato___Late_blight']

# Load dataset (update path for Render.com compatibility)
data_set = tf.keras.preprocessing.image_dataset_from_directory(
    "PlantVillage",  # Use relative path or environment variable if needed
    shuffle=True,
    image_size=(IMAGE_SIZE, IMAGE_SIZE),
    batch_size=BATCH_SIZE,
    label_mode='int'
)

# Display sample images
plt.figure(figsize=(10, 10))
for image_batch, label_batch in data_set.take(1):
    for i in range(10):
        ax = plt.subplot(3, 4, i + 1)
        plt.imshow(image_batch[i].numpy().astype('uint8'))
        plt.title(CLASS_NAMES[label_batch[i]])
        plt.axis("off")

# Partition the dataset
def get_dataset_partition(ds, train_split=0.8, test_split=0.1, val_split=0.1, shuffle=True, shuffle_size=10000):
    ds_size = len(ds)
    if shuffle:
        ds = ds.shuffle(shuffle_size, seed=20)
    train_size = int(train_split * ds_size)
    val_size = int(val_split * ds_size)
    test_size = ds_size - train_size - val_size
    train_ds = ds.take(train_size)
    val_ds = ds.skip(train_size).take(val_size)
    test_ds = ds.skip(train_size + val_size).take(test_size)
    return train_ds, test_ds, val_ds

train_ds, test_ds, val_ds = get_dataset_partition(data_set)

# Data preprocessing and augmentation
preprocess_and_augment = tf.keras.Sequential([
    layers.Resizing(IMAGE_SIZE, IMAGE_SIZE),
    layers.Rescaling(1.0 / 255),
    layers.RandomCrop(height=IMAGE_SIZE, width=IMAGE_SIZE),
    layers.RandomRotation(0.2),
    layers.RandomFlip('horizontal_and_vertical'),
    layers.RandomZoom(0.1),
    layers.RandomBrightness(factor=0.2),
    layers.RandomContrast(factor=0.2)
])

# CNN model creation
def create_cnn_model(input_shape):
    model = models.Sequential([
        layers.Input(shape=input_shape),
        preprocess_and_augment,
        layers.Conv2D(32, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
    ])
    return model

input_shape = (IMAGE_SIZE, IMAGE_SIZE, CHANNELS)
n_classes = len(CLASS_NAMES)

# Create multiple CNN models
cnn_models = [create_cnn_model(input_shape) for _ in range(3)]

# Ensemble model (CNN)
ensemble_input = layers.Input(shape=input_shape)
cnn_outputs = [cnn_model(ensemble_input) for cnn_model in cnn_models]
merged_output = layers.Concatenate()(cnn_outputs)
final_output = layers.Dense(n_classes, activation='softmax')(merged_output)

ensemble_model = models.Model(inputs=ensemble_input, outputs=final_output)
ensemble_model.compile(
    optimizer='adam',
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
    metrics=['accuracy']
)

# Training the model
history = ensemble_model.fit(
    train_ds,
    epochs=EPOCHS,
    validation_data=val_ds,
    verbose=1
)

# Evaluating the model
scores = ensemble_model.evaluate(test_ds)

# Extract features
def extract_features(model, dataset):
    features = []
    labels = []
    for images, lbls in dataset:
        cnn_features = model.predict(images)
        features.append(cnn_features)
        labels.append(lbls)
    return np.vstack(features), np.hstack(labels)

train_features, train_labels = extract_features(ensemble_model, train_ds)
test_features, test_labels = extract_features(ensemble_model, test_ds)

# Standardize the features
scaler = StandardScaler()
train_features = scaler.fit_transform(train_features)
test_features = scaler.transform(test_features)

# Train the Random Forest model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(train_features, train_labels)

# Evaluate the Random Forest model
rf_predictions = rf_model.predict(test_features)
rf_accuracy = accuracy_score(test_labels, rf_predictions)
print(f'Random Forest Model Accuracy: {rf_accuracy}')

# Prediction function using the ensemble of CNN + Random Forest
def predict_ensemble(model, rf_model, image):
    img_array = tf.keras.preprocessing.image.img_to_array(image)
    img_array = tf.expand_dims(img_array, 0)
    cnn_features = model.predict(img_array)
    rf_features = scaler.transform(cnn_features)
    rf_predictions = rf_model.predict(rf_features)
    predicted_class = CLASS_NAMES[rf_predictions[0]]
    return predicted_class

# Save models in TensorFlow SavedModel format for compatibility
ensemble_model.save('ensemble_model', save_format='tf')  # TensorFlow SavedModel format
joblib.dump(rf_model, 'rf_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
