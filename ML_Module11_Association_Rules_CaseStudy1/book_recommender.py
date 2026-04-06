# """
# book_recommender.py

# - Loads BX-Book-Ratings.csv (uses a random 10k sample for faster prototyping)
# - Trains a Surprise SVD model on explicit ratings
# - Evaluates with RMSE on a hold-out test set
# - Provides get_top_n_recommendations(user_id, n) to get top-N recommendations (ISBNs + predicted rating)
# - Saves model and scaler (optional)
# """

import os
import random
import pandas as pd
import numpy as np
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise import accuracy
from surprise.model_selection import GridSearchCV
from collections import defaultdict
import joblib

# ---------- Config ----------
INPUT_CSV = 'BX-Book-Ratings.csv'
SAMPLE_SIZE = 10000         
RANDOM_SEED = 42
MODEL_PATH = '/surprise_svd_model.joblib'  # optional save
# ---------------------------

def load_and_sample(csv_path, sample_size=SAMPLE_SIZE, seed=RANDOM_SEED):
    # The book ratings dataset sometimes has weird separators or quote chars.
    
    df = pd.read_csv(csv_path, sep=';', encoding='latin-1', on_bad_lines='skip')
    # normalize column names (common names: 'user_id','isbn','rating')
    # try to find columns heuristically if names differ
    cols_lower = [c.lower() for c in df.columns]
    mapping = {}
    for c in df.columns:
        lc = c.lower()
        if 'user' in lc and 'id' in lc:
            mapping[c] = 'user_id'
        elif c.lower() in ('user_id', 'userid', 'user-id'):
            mapping[c] = 'user_id'
        elif 'isbn' in lc:
            mapping[c] = 'isbn'
        elif 'rating' in lc or 'value' in lc:
            mapping[c] = 'rating'
    df = df.rename(columns=mapping)

    if not {'user_id', 'isbn', 'rating'}.issubset(set(df.columns)):
        raise ValueError("Couldn't find required columns user_id/isbn/rating in the CSV. Columns found: " + str(df.columns))

    # Keep only required columns
    df = df[['user_id', 'isbn', 'rating']].dropna()
    # Convert rating numeric
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df = df.dropna(subset=['rating'])

    # sample (stratified sampling by users/ratings would be better, but random is fine)
    if sample_size is not None and sample_size < len(df):
        df_sampled = df.sample(n=sample_size, random_state=seed).reset_index(drop=True)
    else:
        df_sampled = df.reset_index(drop=True)

    return df_sampled

def train_surprise_svd(df, n_factors=50, n_epochs=20, lr_all=0.005, reg_all=0.02, random_state=RANDOM_SEED):
    # surprise expects a Reader with rating_scale
    reader = Reader(rating_scale=(df['rating'].min(), df['rating'].max()))
    data = Dataset.load_from_df(df[['user_id', 'isbn', 'rating']], reader)

    # train-test split
    trainset, testset = train_test_split(data, test_size=0.2, random_state=random_state)

    # Build SVD model (matrix factorization)
    algo = SVD(n_factors=n_factors, n_epochs=n_epochs, lr_all=lr_all, reg_all=reg_all, random_state=random_state)
    algo.fit(trainset)

    # Evaluate on testset
    predictions = algo.test(testset)
    rmse = accuracy.rmse(predictions, verbose=True)

    return algo, trainset, testset, rmse, predictions

def get_unseen_items(trainset, user_raw_id, all_item_raw_ids):
    """Return list of item raw ids that user hasn't rated yet"""
    # trainset.to_inner_uid throws error if user not in trainset; we accept cold-start by returning all items
    try:
        u_inner = trainset.to_inner_uid(user_raw_id)
    except ValueError:
        # user not in trainset (cold start) -> recommend top-popular items (we will handle outside)
        return list(all_item_raw_ids)
    seen_inner = set([j for (j, _) in trainset.ur[u_inner]])  # set of inner item ids seen
    seen_raw = set([trainset.to_raw_iid(inner) for inner in seen_inner])
    unseen = [iid for iid in all_item_raw_ids if iid not in seen_raw]
    return unseen

def get_top_n_recommendations(algo, trainset, user_raw_id, all_item_raw_ids, n=10):
    
    # If user unknown, use popularity
    try:
        _ = trainset.to_inner_uid(user_raw_id)
        user_known = True
    except ValueError:
        user_known = False

    # Build popularity ranking (item mean rating) for fallback
    item_ratings = defaultdict(list)
    for (uid, iid, r) in trainset.all_ratings():
        item_ratings[trainset.to_raw_iid(iid)].append(r)
    item_mean = {iid: np.mean(rs) for iid, rs in item_ratings.items()}

    if not user_known:
        # Cold-start: return top-n popular items
        sorted_pop = sorted(item_mean.items(), key=lambda x: -x[1])
        return sorted_pop[:n]

    unseen = get_unseen_items(trainset, user_raw_id, all_item_raw_ids)
    preds = []
    for iid in unseen:
        est = algo.predict(user_raw_id, iid).est
        preds.append((iid, est))
    preds.sort(key=lambda x: -x[1])
    return preds[:n]

def build_and_run():
    print("Loading & sampling dataset...")
    df = load_and_sample(INPUT_CSV, sample_size=SAMPLE_SIZE, seed=RANDOM_SEED)
    print("Sample shape:", df.shape)
    print(df.head())

    # Train model
    print("\nTraining SVD model...")
    algo, trainset, testset, rmse, preds = train_surprise_svd(df)
    print(f"Trained SVD; test RMSE = {rmse:.4f}")

    # Prepare list of all item ids in the dataset (raw ids)
    all_item_raw_ids = df['isbn'].unique().tolist()

    # Example: get top-10 recommendations for a random user from the sample
    sample_user = df['user_id'].sample(1, random_state=RANDOM_SEED).iloc[0]
    print(f"\nExample recommendations for user_id = {sample_user}:")
    topn = get_top_n_recommendations(algo, trainset, sample_user, all_item_raw_ids, n=10)
    for rank, (isbn, est) in enumerate(topn, start=1):
        print(f"{rank}. ISBN: {isbn}   Predicted rating: {est:.3f}")

    # Save model for later use
    try:
        joblib.dump(algo, MODEL_PATH)
        print(f"\nSaved trained model to {MODEL_PATH}")
    except Exception as e:
        print("Warning: failed to save model:", e)

    # Return objects if further analysis needed
    return {
        "df_sample": df,
        "algo": algo,
        "trainset": trainset,
        "testset": testset,
        "rmse": rmse
    }

if __name__ == "__main__":
    results = build_and_run()
