# bio_degradable_boosting_pipeline.py
# Requirements:
#   pip install pandas numpy scikit-learn joblib xgboost lightgbm catboost  (install those you want)
# Usage:
#   python bio_degradable_boosting_pipeline.py

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV, StratifiedKFold
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectKBest, mutual_info_classif, RFE
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, roc_auc_score, accuracy_score, confusion_matrix
import joblib
import warnings
warnings.filterwarnings("ignore")

DATA_PATH = "/bio-degradabale-data.csv"
OUT_DIR = "/model_outputs"
os.makedirs(OUT_DIR, exist_ok=True)

#  Load the CSV (this dataset uses semicolon separated fields)
df = pd.read_csv(DATA_PATH, sep=';', header=None)
print("Loaded data (sep=';'). Shape:", df.shape)

#  Assume last column is the target (RB / NRB)
df.columns = [f"c{i}" for i in range(df.shape[1])]
target_col = df.columns[-1]
print("Assuming last column as target:", target_col)
print(df[target_col].value_counts())

#  Build X, y (encode target)
X = df.drop(columns=[target_col]).copy()
y_raw = df[target_col].astype(str).str.strip()
le = LabelEncoder()
y = le.fit_transform(y_raw)
print("Label encoding mapping:", dict(zip(le.classes_, le.transform(le.classes_))))

#  Train/test split (stratified)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)
print("Train/test shapes:", X_train.shape, X_test.shape)

#  Convert columns to numeric where possible (many columns are numeric strings)
for c in X_train.columns:
    X_train[c] = pd.to_numeric(X_train[c], errors='coerce')
    X_test[c] = pd.to_numeric(X_test[c], errors='coerce')

#  Identify numeric and categorical columns
num_cols = X_train.select_dtypes(include=[np.number]).columns.tolist()
cat_cols = X_train.select_dtypes(include=['object','category','bool']).columns.tolist()
print("Numeric cols:", len(num_cols), "Categorical cols:", len(cat_cols))

#  Preprocessing pipelines
num_transformer = Pipeline([('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())])
cat_transformer = Pipeline([('imputer', SimpleImputer(strategy='most_frequent')), ('onehot', OneHotEncoder(handle_unknown='ignore', sparse=False))])

preprocessor = ColumnTransformer([
    ('num', num_transformer, num_cols),
    ('cat', cat_transformer, cat_cols)
], remainder='drop', sparse_threshold=0)

preprocessor.fit(X_train)
X_train_proc = preprocessor.transform(X_train)
X_test_proc = preprocessor.transform(X_test)

# build feature names (for interpretability)
ohe_cat_names = []
if len(cat_cols) > 0:
    ohe = preprocessor.named_transformers_['cat'].named_steps['onehot']
    ohe_cat_names = ohe.get_feature_names_out(cat_cols).tolist()
feature_names = num_cols + ohe_cat_names
print("Total features after preprocessing:", len(feature_names))

#  Feature selection: SelectKBest (mutual information)
k = min(30, X_train_proc.shape[1])
skb = SelectKBest(score_func=mutual_info_classif, k=k)
skb.fit(X_train_proc, y_train)
skb_scores = pd.Series(skb.scores_, index=feature_names).sort_values(ascending=False)
print("\nTop features by mutual information:")
print(skb_scores.head(20))

X_train_skb = skb.transform(X_train_proc)
X_test_skb = skb.transform(X_test_proc)

#  Model candidates: try to use XGBoost / LightGBM / CatBoost if available, else fallback to sklearn GB
models = {}
try:
    import xgboost as xgb
    models['xgb'] = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
    print("XGBoost found and will be used.")
except Exception:
    print("XGBoost not installed; skipping.")

try:
    import lightgbm as lgb
    models['lgb'] = lgb.LGBMClassifier(random_state=42)
    print("LightGBM found and will be used.")
except Exception:
    print("LightGBM not installed; skipping.")

try:
    import catboost as cb
    models['cat'] = cb.CatBoostClassifier(verbose=0, random_state=42)
    print("CatBoost found and will be used.")
except Exception:
    print("CatBoost not installed; skipping.")

# Always include scikit-learn GradientBoosting
models['gb'] = GradientBoostingClassifier(random_state=42)
print("Models to evaluate:", list(models.keys()))

#  Lightweight hyperparameter tuning with RandomizedSearchCV on SelectKBest features
cv = StratifiedKFold(n_splits=4, shuffle=True, random_state=42)
results = {}

for name, model in models.items():
    print(f"\nTuning model: {name}")
    if name == 'xgb':
        param_dist = {
            'n_estimators': [50,100,200],
            'max_depth': [3,5,7],
            'learning_rate': [0.01, 0.05, 0.1],
            'subsample': [0.6, 0.8, 1.0]
        }
    elif name == 'lgb':
        param_dist = {
            'n_estimators': [50,100,200],
            'num_leaves': [31,50,80],
            'learning_rate': [0.01, 0.05, 0.1],
            'subsample': [0.6,0.8,1.0]
        }
    elif name == 'cat':
        param_dist = {
            'iterations': [100,200,300],
            'depth': [4,6,8],
            'learning_rate': [0.01, 0.05, 0.1]
        }
    else:  # sklearn gb
        param_dist = {
            'n_estimators': [50,100,200],
            'learning_rate': [0.01,0.05,0.1],
            'max_depth': [3,5]
        }

    rnd = RandomizedSearchCV(model, param_distributions=param_dist, n_iter=8,
                             scoring='roc_auc', cv=cv, random_state=42, n_jobs=-1)
    rnd.fit(X_train_skb, y_train)
    print(" Best params:", rnd.best_params_)
    print(" Best CV ROC AUC:", rnd.best_score_)
    results[name] = {
        'best_estimator': rnd.best_estimator_,
        'best_score': rnd.best_score_,
        'best_params': rnd.best_params_
    }

#  Select best model by CV score and evaluate on test set
best_name = max(results.keys(), key=lambda n: results[n]['best_score'])
best_model = results[best_name]['best_estimator']
print(f"\nSelected best model: {best_name} with CV ROC AUC={results[best_name]['best_score']:.4f}")

best_model.fit(X_train_skb, y_train)
y_pred = best_model.predict(X_test_skb)
y_proba = best_model.predict_proba(X_test_skb)[:,1] if hasattr(best_model, "predict_proba") else None

print("\nTest set metrics:")
print("Accuracy:", accuracy_score(y_test, y_pred))
if y_proba is not None:
    print("ROC AUC:", roc_auc_score(y_test, y_proba))
print(classification_report(y_test, y_pred, target_names=le.classes_))
print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))

#  Model-based selection: RFE with RandomForest
print("\nRunning RFE (RandomForest) to get model-based selected features...")
rf = RandomForestClassifier(n_estimators=200, random_state=42)
rfe_k = min(20, max(2, X_train_proc.shape[1] // 2))
rfe = RFE(estimator=rf, n_features_to_select=rfe_k, step=0.1)
rfe.fit(X_train_proc, y_train)
rfe_selected = [name for name, sel in zip(feature_names, rfe.get_support()) if sel]
print("RFE selected features:", rfe_selected)

# Train best model on RFE features for comparison
X_train_rfe = rfe.transform(X_train_proc)
X_test_rfe = rfe.transform(X_test_proc)
# instantiate same class with best params for fairness
best_cls = best_model.__class__
best_params = results[best_name]['best_params']
best_model_rfe = best_cls(**best_params)
best_model_rfe.fit(X_train_rfe, y_train)
y_pred_rfe = best_model_rfe.predict(X_test_rfe)
y_proba_rfe = best_model_rfe.predict_proba(X_test_rfe)[:,1] if hasattr(best_model_rfe, "predict_proba") else None

print("\nEvaluation on RFE-selected features:")
print("Accuracy:", accuracy_score(y_test, y_pred_rfe))
if y_proba_rfe is not None:
    print("ROC AUC:", roc_auc_score(y_test, y_proba_rfe))
print(classification_report(y_test, y_pred_rfe, target_names=le.classes_))

#  Save artifacts (preprocessor, skb, rfe, label encoder, model)
joblib.dump({
    'preprocessor': preprocessor,
    'select_kbest': skb,
    'rfe_selector': rfe,
    'label_encoder': le,
    'model': best_model,
    'model_name': best_name,
    'model_params': results[best_name]['best_params']
}, os.path.join(OUT_DIR, 'bio_degrade_model_bundle.pkl'))

# Save test predictions
test_pred_df = X_test.reset_index(drop=True).copy()
test_pred_df['true'] = le.inverse_transform(y_test)
test_pred_df['pred'] = le.inverse_transform(y_pred)
if y_proba is not None:
    test_pred_df['proba_1'] = y_proba
test_pred_df.to_csv(os.path.join(OUT_DIR, 'test_predictions.csv'), index=False)

print("\nSaved model bundle and test predictions into:", OUT_DIR)