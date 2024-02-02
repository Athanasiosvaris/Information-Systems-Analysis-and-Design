import time
import ray
from ray import tune
from sklearn.datasets import load_svmlight_file
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score

# Initialize Ray
ray.init(address='auto')

# Load Data and store in Ray object store
X, y = load_svmlight_file("data.libsvm")
X_id = ray.put(X)
y_id = ray.put(y)


def train_and_evaluate(config):

    X_train, X_test, y_train, y_test = train_test_split(ray.get(X_id), ray.get(y_id), test_size=0.2, random_state=42)

    clf = SGDClassifier(**config)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    return {"accuracy": accuracy}

# Ray Tune
start = time.time()
analysis = tune.run(
    train_and_evaluate,
    config={},
    num_samples=2,  # default hyperparameters
    resources_per_trial={"cpu": 4},
    local_dir="/home/user/classification/ray/kappafiles",
)
end = time.time()
print("Tune GridSearch Fit Time:", end - start)

# best config - accuracy
best_config = analysis.get_best_config(metric="accuracy", mode="max")
best_accuracy = analysis.get_best_trial(metric="accuracy", mode="max").last_result["accuracy"]
print("Best Configuration:", best_config)
print("Best Accuracy:", best_accuracy)