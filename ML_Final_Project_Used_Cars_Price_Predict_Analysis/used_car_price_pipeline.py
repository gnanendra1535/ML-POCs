# cars_price_pipeline.py

import os, json, warnings
warnings.filterwarnings("ignore")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.inspection import permutation_importance
import joblib

# Optional boosters (if installed)
try:
    import xgboost as xgb
except Exception:
    xgb = None

# Config
DATA_PATH = r'c:\\Users\\Gnanendra\\Documents\\my_Projects\\my_python_assignments\\ML_Final_Project_Used_Cars_Price_Predict_Analysis\\cars.csv'  # path to dataset
OUT_DIR = "cars_output"
os.makedirs(OUT_DIR, exist_ok=True)
RANDOM_STATE = 42
HIGH_CARD_TH = 30  # threshold for frequency-encoding

def rmse(y_true, y_pred):
    return float(np.sqrt(mean_squared_error(y_true, y_pred)))

def main():
    #  Load
    print("Loading dataset:", DATA_PATH)
    df = pd.read_csv(DATA_PATH)
    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    print("\nPreview:")
    print(df.head().to_string())

    # Detect target (price)
    target_candidates = [c for c in df.columns if c.lower() in ('price','selling_price','sell_price','selling price')]
    if not target_candidates:
        target_candidates = [c for c in df.columns if 'price' in c.lower()]
    if not target_candidates:
        raise ValueError("No price-like column found. Columns: " + ", ".join(df.columns))
    target_col = target_candidates[0]
    print("Using target:", target_col)

    # Basic target histogram
    plt.figure(figsize=(6,4))
    plt.hist(df[target_col].dropna().values, bins=50)
    plt.title(f"{target_col} distribution")
    plt.xlabel(target_col)
    plt.ylabel("count")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "target_distribution.png"))
    plt.close()

    # Basic missing values
    print("\nMissing values (top 10):")
    print(df.isna().sum().sort_values(ascending=False).head(10).to_string())

    # Split numeric and categorical features
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if target_col in num_cols:
        num_cols.remove(target_col)
    cat_cols = df.select_dtypes(include=['object','category']).columns.tolist()
    print("Numeric columns:", num_cols)
    print("Categorical columns:", cat_cols)

    # Decide encoding strategy for categorical features
    onehot_cats = []
    freq_encode_cats = []
    for c in cat_cols:
        nuniq = df[c].nunique(dropna=True)
        if nuniq <= HIGH_CARD_TH:
            onehot_cats.append(c)
        else:
            freq_encode_cats.append(c)
    print("One-hot cats:", onehot_cats)
    print("Freq-encode cats:", freq_encode_cats)

    # Frequency encode high-cardinality categorical columns
    data = df.copy()
    for c in freq_encode_cats:
        freq = data[c].value_counts(normalize=True)
        data[c + "_freq"] = data[c].map(freq).fillna(0.0)
        num_cols.append(c + "_freq")

    # Preprocessing
    num_pipeline = Pipeline([('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())])
    cat_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value='MISSING')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])
    preprocessor = ColumnTransformer(transformers=[('num', num_pipeline, num_cols), ('cat', cat_pipeline, onehot_cats)], remainder='drop', sparse_threshold=0)

    # Build modeling dataset
    modeling_cols = num_cols + onehot_cats + [target_col]
    model_df = data[modeling_cols].copy()
    model_df = model_df.dropna(subset=[target_col])
    X = model_df.drop(columns=[target_col])
    y = model_df[target_col].values
    print("Model dataset shape:", X.shape)

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE)
    print("Train/Test shapes:", X_train.shape, X_test.shape)

    # Models
    models = {}
    models['Ridge'] = Pipeline([('pre', preprocessor), ('model', Ridge(random_state=RANDOM_STATE))])
    models['RandomForest'] = Pipeline([('pre', preprocessor), ('model', RandomForestRegressor(n_estimators=200, random_state=RANDOM_STATE, n_jobs=-1))])
    if xgb is not None:
        models['XGBoost'] = Pipeline([('pre', preprocessor), ('model', xgb.XGBRegressor(n_estimators=200, random_state=RANDOM_STATE, verbosity=0))])
    else:
        print("XGBoost not installed — skipping XGBoost model.")

    results = []
    for name, pipe in models.items():
        print(f"\nTraining {name} ...")
        pipe.fit(X_train, y_train)
        y_pred = pipe.predict(X_test)
        y_pred_train = pipe.predict(X_train)
        result = {
            'model': name,
            'train_rmse': rmse(y_train, y_pred_train),
            'test_rmse': rmse(y_test, y_pred),
            'test_mae': float(mean_absolute_error(y_test, y_pred)),
            'test_r2': float(r2_score(y_test, y_pred))
        }
        results.append(result)
        print(f"{name} results: test RMSE={result['test_rmse']:.3f}, MAE={result['test_mae']:.3f}, R2={result['test_r2']:.3f}")

    # Save performance
    perf_df = pd.DataFrame(results).sort_values('test_rmse')
    perf_df.to_csv(os.path.join(OUT_DIR, "model_performance.csv"), index=False)
    print("\nSaved model performance to:", os.path.join(OUT_DIR, "model_performance.csv"))
    print(perf_df.to_string(index=False))

    # Best model
    best_name = perf_df.iloc[0]['model']
    best_pipe = models[best_name]
    print("\nBest model:", best_name)

    # Feature names after preprocessing
    pre = best_pipe.named_steps['pre']
    pre.fit(X_train)  # ensure fitted
    num_feats = num_cols
    ohe_names = []
    if onehot_cats:
        ohe = pre.named_transformers_['cat'].named_steps['onehot']
        try:
            ohe_names = list(ohe.get_feature_names_out(onehot_cats))
        except Exception:
            # fallback
            cats = pre.named_transformers_['cat'].named_steps['onehot'].categories_
            for col, cat_list in zip(onehot_cats, cats):
                for val in cat_list:
                    ohe_names.append(f"{col}__{val}")
    feature_names = num_feats + ohe_names
    print("Feature count after preprocessing:", len(feature_names))

    # Permutation importance
    print("\nComputing permutation importance (this may take a little while)...")
    perm = permutation_importance(best_pipe, X_test, y_test, n_repeats=20, random_state=RANDOM_STATE, n_jobs=-1, scoring='neg_root_mean_squared_error')
    idx = perm.importances_mean.argsort()[::-1]
    perm_ser = pd.Series(perm.importances_mean[idx], index=[X.columns[i] for i in idx]).sort_values(ascending=False)
    # Save top importances
    perm_ser.head(50).to_csv(os.path.join(OUT_DIR, f"{best_name}_permutation_importances.csv"))
    print("Saved permutation importances to:", os.path.join(OUT_DIR, f"{best_name}_permutation_importances.csv"))
    print("\nTop permutation importances:")
    print(perm_ser.head(30).to_string())

    # Save best model
    model_path = os.path.join(OUT_DIR, f"best_model_{best_name}.joblib")
    joblib.dump(best_pipe, model_path)
    print("\nSaved best model pipeline to:", model_path)

    # Save a JSON summary
    summary = {'best_model': best_name, 'performance': results, 'feature_count': len(feature_names)}
    with open(os.path.join(OUT_DIR, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print("Saved summary to:", os.path.join(OUT_DIR, "summary.json"))

    print("\nAll done. Outputs saved under:", OUT_DIR)

if __name__ == "__main__":
    main()
