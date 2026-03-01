"""Simple ML pipeline using simulated vehicle data

This script demonstrates how you could generate a dataset,
train a classifier to predict health status, and evaluate it.

Usage:
    python vehicle_health_ml.py

Requires scikit-learn:
    pip install scikit-learn pandas

In a real system you would replace the random generator with
recorded data or a simulator, and build more sophisticated features.
"""
import random
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report

# reuse generation and evaluation functions

def generate_vehicle_data(prev_data=None):
    if prev_data is None:
        return {
            'engine_temp': random.uniform(70, 120),
            'battery': random.uniform(11.0, 14.5),
            'rpm': random.uniform(800, 6000),
            'speed': random.uniform(0, 120),
            'fuel': random.uniform(0, 100),
        }
    return {
        'engine_temp': min(120, max(70, prev_data['engine_temp'] + random.uniform(-2, 2))),
        'battery': min(14.5, max(11.0, prev_data['battery'] + random.uniform(-0.1, 0.1))),
        'rpm': min(6000, max(800, prev_data['rpm'] + random.uniform(-100, 100))),
        'speed': min(120, max(0, prev_data['speed'] + random.uniform(-5, 5))),
        'fuel': min(100, max(0, prev_data['fuel'] + random.uniform(-1, 1))),
    }

def evaluate_health(data):
    critical = False
    warnings = 0
    if data['engine_temp'] > 110:
        critical = True
    if data['battery'] < 11.5:
        warnings += 1
    if data['rpm'] > 5000:
        warnings += 1
    if data['fuel'] < 10:
        warnings += 1
    if critical or warnings >= 2:
        return 'Critical'
    if warnings == 1:
        return 'Warning'
    return 'Healthy'

# collect dataset
records = []
prev = None
for _ in range(10000):
    prev = generate_vehicle_data(prev)
    health = evaluate_health(prev)
    records.append({**prev, 'status': health})

df = pd.DataFrame(records)

# features and label
X = df[['engine_temp', 'battery', 'rpm', 'speed', 'fuel']]
y = df['status']

# train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = DecisionTreeClassifier(max_depth=5, random_state=42)
clf.fit(X_train, y_train)

pred = clf.predict(X_test)
print(classification_report(y_test, pred))

# save model for later use (optional)
try:
    import joblib
    joblib.dump(clf, 'vehicle_health_model.pkl')
    print("Model saved to vehicle_health_model.pkl")
except ImportError:
    print("joblib not installed; skipping model save")
