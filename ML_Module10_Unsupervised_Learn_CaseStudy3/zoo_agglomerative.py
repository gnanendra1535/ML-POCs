
# zoo_agglomerative.py
import pandas as pd
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error
from sklearn.metrics import confusion_matrix
from scipy.optimize import linear_sum_assignment

# Config
INPUT_CSV = '/zoo.csv'
# If the class column name differs (e.g., 'class' or 'class_type'), update CLASS_COL.
NAME_COL = 'animal_name'   
CLASS_COL = 'class_type'  
# --------------------------------

def load_and_preview(path):
    df = pd.read_csv(path)
    print("=== Data Info ===")
    print(df.info())
    print("\n=== First 5 rows ===")
    print(df.head())
    return df

def get_feature_matrix(df, name_col, class_col):
    # Drop name and class columns to get the intermediate features
    # If your file has columns arranged differently, this logic will drop exactly name & class.
    X = df.drop(columns=[name_col, class_col])
    return X

def map_clusters_to_labels(y_true, y_pred):
    """
    Map cluster labels to true labels using the Hungarian algorithm on the contingency matrix
    so we can compare labels meaningfully. Returns mapped predictions and the mapping dict.
    """
    # Ensure integer labels start at 0
    le = LabelEncoder()
    y_true_enc = le.fit_transform(y_true)
    true_labels = np.unique(y_true_enc)

    # Build contingency / confusion matrix between true labels and cluster labels
    contingency = confusion_matrix(y_true_enc, y_pred)
    # We want to maximize accuracy, so convert to cost for Hungarian (minimize)
    cost_matrix = contingency.max() - contingency
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    # Build mapping from cluster -> true label
    cluster_to_true = {}
    for true_idx, cluster_idx in zip(row_ind, col_ind):
        cluster_to_true[cluster_idx] = true_idx

    # Map predictions
    mapped_pred = np.array([cluster_to_true.get(c, -1) for c in y_pred])
    # In case some clusters weren't matched, mapped_pred may contain -1; handle by assigning a new label (max+1)
    if (mapped_pred == -1).any():
        unmapped_new_label = y_true_enc.max() + 1
        mapped_pred[mapped_pred == -1] = unmapped_new_label

    # Convert mapped_pred back to original class labels using inverse transform
    mapped_pred_labels = le.inverse_transform(mapped_pred.clip(0, y_true_enc.max()))
    return mapped_pred_labels, le

def main():
    df = load_and_preview(INPUT_CSV)

    # Detect name/class columns heuristically if the defaults don't exist
    if NAME_COL not in df.columns or CLASS_COL not in df.columns:
        # Try common names
        possible_name = None
        possible_class = None
        for c in df.columns:
            if c.lower() in ('name', 'animal_name', 'animal', 'animalname'):
                possible_name = c
            if c.lower() in ('class', 'class_type', 'class_type.1', 'class_type.2', 'type', 'label'):
                possible_class = c
        if possible_name and possible_class:
            print(f"Auto-detected name column: {possible_name}, class column: {possible_class}")
            name_col = possible_name
            class_col = possible_class
        else:
            # Assume first column is name and last is class as per problem statement
            name_col = df.columns[0]
            class_col = df.columns[-1]
            print(f"Using first column as name: {name_col}, last column as class: {class_col}")
    else:
        name_col = NAME_COL
        class_col = CLASS_COL

    # Show columns
    print("\nColumns:", df.columns.tolist())

    # Unique number of high-level classes
    unique_classes = df[class_col].unique()
    n_classes = len(unique_classes)
    print(f"\nNumber of unique high-level classes: {n_classes}")
    print("Classes:", sorted(unique_classes))

    # Use the intermediate features and perform agglomerative clustering
    X = get_feature_matrix(df, name_col, class_col)
    print(f"\nFeature matrix shape (should be N x 16): {X.shape}")

    # If any non-numeric columns present in X, try to convert/encode
    if X.dtypes.apply(lambda dt: not np.issubdtype(dt, np.number)).any():
        print("Non-numeric feature columns detected; attempting to convert to numeric using get_dummies.")
        X = pd.get_dummies(X)

    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Agglomerative clustering with number of clusters = number of unique high-level classes
    agg = AgglomerativeClustering(n_clusters=n_classes, affinity='euclidean', linkage='ward')
    cluster_labels = agg.fit_predict(X_scaled)
    df['predicted_cluster'] = cluster_labels

    print("\nCluster label counts:")
    print(pd.Series(cluster_labels).value_counts().sort_index())

    #  Compute MSE by comparing actual class and predicted high-level class
    # We need to map clusters to actual class labels for meaningful comparison
    mapped_pred_labels, label_encoder = map_clusters_to_labels(df[class_col].values, cluster_labels)

    # Convert true and mapped predicted to encoded ints for MSE
    true_encoded = label_encoder.transform(df[class_col].values)
    mapped_pred_encoded = label_encoder.transform(mapped_pred_labels)

    mse = mean_squared_error(true_encoded, mapped_pred_encoded)
    print(f"\nMean Squared Error (after mapping cluster labels to true classes): {mse:.4f}")

    # Optionally print a small mapping and confusion
    # Build mapping from cluster -> mapped true label (encoded)
    # (recompute mapping for clarity)
    contingency = confusion_matrix(true_encoded, cluster_labels)
    print("\nContingency matrix (rows=true labels, cols=cluster labels):\n", contingency)

    # Save outputs
    df.to_csv('/mnt/data/zoo_with_clusters.csv', index=False)
    print("\nSaved clustered data to /mnt/data/zoo_with_clusters.csv")

if __name__ == "__main__":
    main()
