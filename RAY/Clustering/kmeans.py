import time
import ray
import numpy as np
from ray import tune
from sklearn.datasets import load_svmlight_file
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.metrics import davies_bouldin_score

# Initialize Ray
ray.init(address='auto')

# Load Data and store in Ray object store
X, _ = load_svmlight_file("data.libsvm")
X_id = ray.put(X)


def train_and_evaluate(config):

    X_data = ray.get(X_id).toarray()

    kmeans = KMeans(n_clusters=config["n_clusters"], random_state=42)
    kmeans.fit(X_data)

    # Davies-Bouldin score
    davies_bouldin = davies_bouldin_score(X_data, kmeans.labels_)

    return {"davies_bouldin": davies_bouldin}

# Ray Tune
start = time.time()
analysis = tune.run(
    train_and_evaluate,
    config={"n_clusters": 16},
    num_samples=2,
    resources_per_trial={"cpu": 4},
    local_dir="/home/user/clustering/ray/kappafiles",
)
end = time.time()
print("Tune GridSearch Fit Time:", end - start)

# best config - Davies-Bouldin score
best_config = analysis.get_best_config(metric="davies_bouldin", mode="min")
best_davies_bouldin = analysis.get_best_trial(metric="davies_bouldin", mode="min").last_result["davies_bouldin"]
print("Best Configuration:", best_config)
print("Best Davies-Bouldin Score:", best_davies_bouldin)
