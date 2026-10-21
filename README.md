# Dravyon – AI-Based Herbal Adulteration Detection System

## 📌 Project Overview

**Dravyon** is an AI-based Smart E-Tongue system designed to analyze herbal samples using sensor measurements and machine learning techniques. The system collects pH, Total Dissolved Solids (TDS), and RGB color measurements to study the characteristics of herbal samples and identify potential adulteration.

The project integrates an ESP32 microcontroller, multiple sensors, machine learning algorithms, and ThingSpeak cloud connectivity to support sensor data collection, adulterant classification, and purity estimation.

## 🎯 Objectives

- Analyze herbal samples using electronic sensor measurements.
- Collect pH, TDS, and RGB sensor data.
- Classify adulterant categories using machine learning.
- Estimate herbal sample purity as a percentage.
- Upload sensor measurements to the ThingSpeak IoT cloud platform.
- Explore an affordable and portable approach to herbal sample analysis.

## 🛠️ Technologies Used

### Hardware
- ESP32 microcontroller
- pH sensor
- TDS sensor
- TCS34725 RGB color sensor

### Software and Libraries
- Arduino IDE
- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- ThingSpeak
- Wi-Fi and HTTP communication

## ⚙️ System Architecture

The system consists of three main components:

1. **Sensor Data Acquisition:** The ESP32 reads pH and TDS values through its analog input pins and collects red, green, blue, and clear-channel readings from the TCS34725 RGB sensor over I2C.
2. **IoT Data Transmission:** The ESP32 connects to Wi-Fi and sends pH, TDS, red, green, and blue readings to ThingSpeak using HTTP requests.
3. **Machine Learning Analysis:** Python processes sensor data and uses an SVM classifier to predict the adulterant category and a Random Forest regression model to estimate sample purity.

## 🧠 Machine Learning Models

### 1. Support Vector Machine (SVM)

An SVM classifier with an RBF kernel is used to classify adulterant categories from sensor measurements.

**Input features:**
- pH
- TDS
- Red
- Green
- Blue

The model uses standardization to scale the input features before classification.

### 2. Random Forest Regressor

A Random Forest regression model is used to estimate herbal sample purity as a continuous percentage.

The model uses sensor measurements as inputs and the `Purity` column as its target variable.

### Model Evaluation

The Python implementation evaluates the models using:

- **Accuracy:** Measures the proportion of correctly classified samples.
- **Precision, Recall, and F1-score:** Evaluate classification performance.
- **Confusion Matrix:** Summarizes correct and incorrect classifications.
- **R² Score:** Measures regression model fit.
- **RMSE:** Measures the magnitude of regression prediction errors.

