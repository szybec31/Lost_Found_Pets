import tensorflow as tf
import numpy as np
import cv2


# Wczytujemy model MobileNetV2 bez warstwy klasyfikacyjnej
model = tf.keras.applications.MobileNetV2(weights='imagenet', include_top=False, pooling='avg')

def extract_features(img_path):
    """Ekstrakcja cech obrazu za pomocą MobileNetV2"""
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Konwersja do RGB
    img = cv2.resize(img, (224, 224))  # MobileNet wymaga 224x224
    img = np.expand_dims(img, axis=0)  # Dodanie wymiaru batch
    img = tf.keras.applications.mobilenet_v2.preprocess_input(img)  # Normalizacja

    features = model.predict(img)  # Pobranie cech
    return features.flatten()  # Spłaszczony wektor cech

