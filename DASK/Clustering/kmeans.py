import dask.dataframe as dd
from dask.distributed import Client
from dask_ml.cluster import KMeans
from sklearn.metrics import davies_bouldin_score
import dask_ml.datasets as dask_ml_datasets
import time

def perform_dask_kmeans_on_libsvm(file_path, num_clusters=16):
    # Connect to the Dask cluster
    client = Client("tcp://localhost:8786")

    # Load LIBSVM data
    #X_dask, _ = dd.read_csv('new_file.csv')
    X_dask = dd.read_csv(file_path, header=None, dtype=float)
    # Print the first few rows of the DataFrame
    print(X_dask.head())
    start = time.time()
    # Perform k-means clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(X_dask)

    # Get cluster assignments for each sample
    cluster_labels_dask = kmeans.labels_

    # Compute Davies-Bouldin score
    db_score = davies_bouldin_score(X_dask.compute(), cluster_labels_dask.compute())
    end = time.time()
    print("Total computation time : ",end-start)
    # Disconnect the client
    client.close()

    return cluster_labels_dask, db_score

# File path to LIBSVM data
file_path = 'new_data.csv'

# Number of clusters
num_clusters = 16

# Perform k-means clustering and get Davies-Bouldin score
cluster_labels_dask, db_score = perform_dask_kmeans_on_libsvm(file_path, num_clusters)
# Print the Davies-Bouldin score
print(f"Davies-Bouldin score: {db_score}")