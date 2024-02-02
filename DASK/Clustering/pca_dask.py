import dask.dataframe as dd
from dask.distributed import Client
from dask_ml.decomposition import PCA
import numpy as np
import time

def perform_dask_pca_on_csv(file_path, num_components=2):
    # Connect to the Dask cluster
    client = Client("tcp://localhost:8786")

    # Load CSV data
    df = dd.read_csv(file_path, header=None, dtype=float)
    print(df.head())
    start = time.time()
    # Convert Dask DataFrame to Dask Array
    X_dask_array = df.to_dask_array(lengths=True)

    # Perform PCA
    pca = PCA(n_components=num_components)
    X_pca_dask = pca.fit(X_dask_array)  #= pca.fit_transform(X_dask_array)

    # Persist the result in memory
    #X_pca_dask = X_pca_dask.persist()
    end = time.time()
    print("Total computation time: ",end-start)
    # Disconnect the client
    client.close()

    return X_pca_dask

# File path to CSV data
file_path = 'new_data.csv'

# Number of principal components
num_components = 2

# Perform PCA and get the result
X_pca_dask = perform_dask_pca_on_csv(file_path, num_components)

# Compute and access the PCA result
#X_pca_dask_result = X_pca_dask.compute()

#Print the result
print(X_pca_dask.explained_variance_ratio_)


