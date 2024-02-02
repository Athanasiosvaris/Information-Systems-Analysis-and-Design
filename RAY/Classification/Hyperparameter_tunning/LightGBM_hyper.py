import time
import ray
from ray import tune
from sklearn.datasets import load_svmlight_file
from sklearn.model_selection import train_test_split
import lightgbm as lgb
from sklearn.metrics import accuracy_score

# Initialize Ray
ray.init(address='auto')

# Load Data and store in Ray object store
X, y = load_svmlight_file("../data.libsvm")
X_id = ray.put(X)
y_id = ray.put(y)


def train_and_evaluate(config):

    X_train, X_test, y_train, y_test = train_test_split(ray.get(X_id), ray.get(y_id), test_size=0.3, random_state=42)

    train_data = lgb.Dataset(X_train, label=y_train)
    test_data = lgb.Dataset(X_test, label=y_test)

    clf = lgb.train(config, train_data, valid_sets=[test_data])

    y_pred = clf.predict(X_test)
    y_pred = [round(value) for value in y_pred]  # probabilities to class labels

    accuracy = accuracy_score(y_test, y_pred)

    return {"accuracy": accuracy}

# Ray Tune
start = time.time()
analysis = tune.run(
    train_and_evaluate,
    config={
        "num_leaves": tune.choice([20, 30, 40]),
        "max_depth": tune.choice([3, 4, 5]),
        "learning_rate": tune.loguniform(0.01, 0.1),
        "subsample": tune.uniform(0.5, 1.0),
        "colsample_bytree": tune.uniform(0.5, 1.0),
    },
    num_samples=2,  # Number of trials
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