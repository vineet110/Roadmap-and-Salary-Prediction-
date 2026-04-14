import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
import pickle

# ================= LOAD =================
df = pd.read_csv("dataset.csv")

# ================= CLEAN =================
df = df.dropna(subset=["salary"])
df = df.fillna(0)

# ================= FEATURE ENGINEERING =================
df["projects"] = df["degree_p"] / 10
df["internships"] = df["workex"].map({"Yes": 1, "No": 0}).fillna(0)
df["cgpa"] = df["degree_p"] / 10
df["certifications"] = 1
df["coding_score"] = df["etest_p"]

df = df[[
    "projects",
    "internships",
    "cgpa",
    "certifications",
    "coding_score",
    "salary"
]]

# 🔥 FINAL FIX: SCALE TO LPA
df["salary"] = df["salary"] / 100000   # ✅ CORRECT

# Debug check
print("\nSalary stats after scaling:\n")
print(df["salary"].describe())

# ================= SPLIT =================
X = df.drop("salary", axis=1)
y = df["salary"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ================= MODELS =================
models = {
    "RandomForest": RandomForestRegressor(),
    "XGBoost": xgb.XGBRegressor()
}

best_model = None
best_score = -999

print("\nMODEL PERFORMANCE:\n")

for name, model in models.items():
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    print(f"{name} → MAE: {mae:.2f}, R²: {r2:.2f}")

    if r2 > best_score:
        best_model = model
        best_score = r2

pickle.dump(best_model, open("model.pkl", "wb"))

print("\n✅ Best model saved")