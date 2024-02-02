import dask.dataframe as dd
from dask_ml.model_selection import train_test_split
from dask.distributed import Client
from sklearn.metrics import accuracy_score, mean_absolute_error
import numpy as np
import dask.array as da
from sklearn.datasets import load_svmlight_file
from sklearn.linear_model import SGDClassifier
import time
from ray import tune

# connect to the cluster
client = Client("tcp://83.212.74.42:8786")
# the file path
file_path = 'data.csv'

# Read the CSV file into a Dask DataFrame
# Assuming the first column is Y and the next 20 columns are X
column_names = ['Y'] + [f'X{i}' for i in range(1, 11)]  # Adjust column names as needed
df = dd.read_csv(file_path, header=None, names=column_names, dtype=float)

# Separate Y and X columns
Y_dask = df['Y']
X_dask = df.drop(columns=['Y'])
print("I run")

# convert the dataframe to an array
X_dask = X_dask.to_dask_array(lengths=True)  # Data
Y_dask = Y_dask.to_dask_array(lengths=True)  # labels

start = time.time()
# perform train-test split using dask
X_train_dask, X_test_dask, Y_train_dask, Y_test_dask = train_test_split(
    X_dask, Y_dask, test_size=0.2, random_state=42, shuffle=True  # Set shuffle to True
)

# Define hyperparameters for SGDClassifier
hyperparameters = {
    "alpha": tune.loguniform(1e-6, 1e-2),
    "penalty": tune.choice(['none', 'l2', 'l1', 'elasticnet']),
    "loss": tune.choice(['hinge', 'log', 'modified_huber', 'squared_hinge', 'perceptron']),
    "learning_rate": tune.choice(['optimal', 'constant', 'invscaling', 'adaptive'])
}

# Create and train SGDClassifier
sgd_classifier = SGDClassifier(**hyperparameters)

# Train and evaluate the classifier
sgd_classifier.fit(X_train_dask, Y_train_dask)
Y_pred_dask = sgd_classifier.predict(X_test_dask)
accuracy_dask = accuracy_score(Y_test_dask, Y_pred_dask)

end = time.time()
print("Time of train and accuracy computations : ", end - start)
print(f"Accuracy: {accuracy_dask}")

# Disconnect the dask client
client.close()