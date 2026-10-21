# DRAVYON - MACHINE LEARNING MODULE
# Performs adulterant classification and purity estimation
# ============================================================
# ===================== LIBRARY MODULE =====================
import pandas as pd # Dataset handling
import numpy as np # Numerical calculations
import matplotlib.pyplot as plt # Graph plotting
from sklearn.model_selection import train_test_split # Train/test splitting
from sklearn.preprocessing import StandardScaler, LabelEncoder # Data preprocessing
from sklearn.svm import SVC # SVM classification model
from sklearn.ensemble import RandomForestRegressor # Random Forest regression model
from sklearn.metrics import (
 accuracy_score, # Classification accuracy
 classification_report, # Precision, recall and F1-score
 confusion_matrix, # Classification error matrix
 r2_score, # Regression goodness-of-fit
 mean_squared_error # Regression error calculation
)
# ============================================================
# DATASET INPUT MODULE
# Loads the sensor dataset collected from the system
# ============================================================
from google.colab import files
uploaded = files.upload() # Upload CSV dataset
filename = list(uploaded.keys())[0] # Get uploaded filename
df = pd.read_csv(filename) # Read CSV into DataFrame
print("Dataset Shape:", df.shape)
print("\nFirst 5 Records:")
display(df.head())
# ============================================================
# DATA PREPROCESSING MODULE
# Removes incomplete sensor records
# ============================================================
df = df.dropna() # Remove missing values
print("\nDataset after removing missing values:")
print(df.shape)
# ============================================================
# FEATURE SELECTION MODULE
# Selects sensor measurements used as ML inputs
# ============================================================
features = [
 "pH",
 "TDS",
 "Red",
 "Green",
 "Blue"
]
X = df[features] # Input feature matrix
# ============================================================
# CLASSIFICATION TARGET MODULE
# Defines adulterant type as classification output
# ============================================================
y_class = df["Adulterant"] # Adulterant category
# ============================================================
# LABEL ENCODING MODULE
# Converts text classes into numerical ML labels
# ============================================================
label_encoder = LabelEncoder()
y_class_encoded = label_encoder.fit_transform(y_class)
print("\nClasses:")
print(label_encoder.classes_)
# ============================================================
# TRAIN-TEST SPLIT MODULE
# Uses 80% data for training and 20% for testing
# ============================================================
X_train, X_test, y_train, y_test = train_test_split(
 X,
 y_class_encoded,
 test_size=0.20,
 random_state=42,
 stratify=y_class_encoded
)
print("\nTraining Samples:", len(X_train))
print("Testing Samples :", len(X_test))
# ============================================================
# FEATURE SCALING MODULE
# Standardizes sensor features before SVM training
# ============================================================
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
# ============================================================
# SVM CLASSIFICATION MODULE
# Classifies the herbal sample/adulterant type
# ============================================================
svm_model = SVC(
 kernel="rbf", # RBF handles nonlinear sensor patterns
 C=10, # Controls classification boundary
 gamma="scale" # Automatically determines kernel influence
)
svm_model.fit(
 X_train_scaled,
 y_train
)
# ============================================================
# CLASSIFICATION PREDICTION MODULE
# Predicts adulterant class for unseen test samples
# ============================================================
y_pred = svm_model.predict(X_test_scaled)
# ============================================================
# CLASSIFICATION EVALUATION MODULE
# Calculates SVM classification performance
# ============================================================
accuracy = accuracy_score(
 y_test,
 y_pred
)
print("\n======================================")
print(" SVM CLASSIFICATION")
print("======================================")
print(
 f"Accuracy: {accuracy * 100:.2f}%"
)
print("\nClassification Report:")
print(
 classification_report(
 y_test,
 y_pred,
 target_names=label_encoder.classes_
 )
)
print("Confusion Matrix:")
print(
 confusion_matrix(
 y_test,
 y_pred
 )
)
# ============================================================
# REGRESSION TARGET MODULE
# Defines purity percentage as continuous output
# ============================================================
y_purity = df["Purity"]
# ============================================================
# REGRESSION DATA SPLIT MODULE
# Creates training and testing data for purity prediction
# ============================================================
X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(
 X,
 y_purity,
 test_size=0.20,
 random_state=42
)
# ============================================================
# RANDOM FOREST REGRESSION MODULE
# Predicts continuous purity percentage
# ============================================================
rf_model = RandomForestRegressor(
 n_estimators=200, # Number of decision trees
 random_state=42 # Makes results reproducible
)
rf_model.fit(
 X_train_r,
 y_train_r
)
# ============================================================
# REGRESSION PREDICTION MODULE
# Predicts purity for unseen test samples
# ============================================================
rf_pred = rf_model.predict(
 X_test_r
)
# ============================================================
# REGRESSION EVALUATION MODULE
# Calculates R² and RMSE performance
# ============================================================
r2 = r2_score(
 y_test_r,
 rf_pred
)
rmse = np.sqrt(
 mean_squared_error(
 y_test_r,
 rf_pred
 )
)
print("\n======================================")
print(" RANDOM FOREST REGRESSION")
print("======================================")
print(
 f"R² Score : {r2:.3f}"
)
print(
 f"RMSE : {rmse:.3f}"
)
# ============================================================
# FEATURE IMPORTANCE MODULE
# Identifies which sensor contributes most to prediction
# ============================================================
importance = pd.Series(
 rf_model.feature_importances_,
 index=features
)
importance = importance.sort_values(
 ascending=False
)
print("\n======================================")
print(" FEATURE IMPORTANCE")
print("======================================")
print(importance)
# Plot sensor feature importance
plt.figure(figsize=(8, 5))
importance.plot(
 kind="bar"
)
plt.title(
 "Dravyon Sensor Feature Importance"
)
plt.xlabel(
 "Sensor Feature"
)
plt.ylabel(
 "Importance"
)
plt.tight_layout()
plt.show()
# ============================================================
# NEW SAMPLE PREDICTION MODULE
# Uses new ESP32 sensor values for final prediction
# ============================================================
print("\n======================================")
print(" NEW SAMPLE PREDICTION")
print("======================================")
# Enter sensor values obtained from ESP32
new_sample = pd.DataFrame(
 [[
 6.35, # pH
 320.0, # TDS in ppm
 125.0, # Red value
 95.0, # Green value
 60.0 # Blue value
 ]],
 columns=features
)
# ============================================================
# SVM PREDICTION MODULE
# Predicts adulterant type of new sample
# ============================================================
new_sample_scaled = scaler.transform(
 new_sample
)
class_prediction = svm_model.predict(
 new_sample_scaled
)
predicted_class = label_encoder.inverse_transform(
 class_prediction
)
print(
 "Predicted Adulterant:",
 predicted_class[0]
)
# ============================================================
# RANDOM FOREST PREDICTION MODULE
# Predicts purity percentage of new sample
# ============================================================
purity_prediction = rf_model.predict(
 new_sample
)
# Restrict output to valid purity range
purity_prediction = np.clip(
 purity_prediction,
 0,
 100
)
print(
 f"Predicted Purity: {purity_prediction[0]:.2f}%"
)
# ============================================================
# FINAL RESULTS MODULE
# Displays the important project performance values
# ============================================================
print("\n======================================")
print(" DRAVYON RESULTS")
print("======================================")
print(
 f"SVM Classification Accuracy : "
 f"{accuracy * 100:.2f}%"
)
print(
 f"Random Forest R² : "
 f"{r2:.3f}"
)
print(
 f"Random Forest RMSE : "
 f"{rmse:.3f}"
)
print(
 f"Most Important Feature : "
 f"{importance.index[0]}"
)
print("======================================")