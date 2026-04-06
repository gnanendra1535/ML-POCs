# driver clustering.py

# driver_clustering.py
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# ---------- Configuration ----------
INPUT_CSV = '/driver-data.csv'        
OUTPUT_CSV = '/driver_data_with_clusters.csv'
PLOT_PNG   = '/driver_clusters.png'
K = 3                             
RANDOM_STATE = 42
# -----------------------------------

def main():
    # Load data
    df = pd.read_csv(INPUT_CSV)

    # Select features for clustering (drop id)
    features = ['mean_dist_day', 'mean_over_speed_perc']
    X = df[features].copy()

    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Fit KMeans
    kmeans = KMeans(n_clusters=K, random_state=RANDOM_STATE, n_init=10)
    labels = kmeans.fit_predict(X_scaled)

    # Attach cluster labels to original dataframe
    df['cluster'] = labels

    #  Transform cluster centers back to original scale for interpretation
    centers_original = scaler.inverse_transform(kmeans.cluster_centers_)
    cluster_profiles = pd.DataFrame(centers_original, columns=features)
    cluster_profiles['cluster'] = cluster_profiles.index

    # Save outputs
    df.to_csv(OUTPUT_CSV, index=False)
    cluster_profiles.to_csv('/cluster_profiles.csv', index=False)

    # Print short summary
    print("Cluster counts:")
    print(df['cluster'].value_counts().sort_index())
    print("\nCluster profiles (means for each cluster):")
    print(cluster_profiles)

    # Scatter plot (mean_dist_day vs mean_over_speed_perc)
    plt.figure(figsize=(9,6))
    plt.scatter(df['mean_dist_day'], df['mean_over_speed_perc'],
                c=df['cluster'], s=30, alpha=0.7)   # color by cluster (no explicit color chosen)
    # plot centers
    plt.scatter(cluster_profiles['mean_dist_day'], cluster_profiles['mean_over_speed_perc'],
                marker='X', s=200)
    plt.xlabel('Mean distance driven per day')
    plt.ylabel('Mean over-speed percentage')
    plt.title(f'Driver Clusters (k={K})')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(PLOT_PNG)
    plt.show()

    print(f"\nSaved clustered dataset to: {OUTPUT_CSV}")
    print(f"Saved cluster profiles CSV to: /cluster_profiles.csv")
    print(f"Saved plot to: {PLOT_PNG}")

if __name__ == "__main__":
    main()
