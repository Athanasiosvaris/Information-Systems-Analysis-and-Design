import dask.dataframe as dd
from dask_ml.model_selection import train_test_split
from dask.distributed import Client
from  dask_ml.xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import numpy as np
import dask.array as da
from sklearn.datasets import load_svmlight_file
import time

# connect to the cluster
client = Client("tcp://83.212.74.42:8786")
file_path = 'data.csv'

# Read the CSV file into a Dask DataFrame
column_names = ['Y'] + [f'X{i}' for i in range(1, 21)]  
df = dd.read_csv(file_path, header=None, names=column_names, dtype=float)

Y_dask = df['Y']
X_dask = df.drop(columns=['Y'])
print("I run")

# dataframe to array
X_dask = X_dask.to_dask_array(lengths=True)
Y_dask = Y_dask.to_dask_array(lengths=True)

start = time.time()
# perform train-test split using dask
X_train_dask, X_test_dask, Y_train_dask, Y_test_dask = train_test_split(
    X_dask, Y_dask, test_size=0.2, random_state=42, shuffle=True  
)

classifiers = {
    'XGBoost': XGBClassifier()
}
for clf_name, clf in classifiers.items():
    clf.fit(X_train_dask, Y_train_dask)
    Y_pred_dask = clf.predict(X_test_dask)
    accuracy_dask = accuracy_score(Y_test_dask, Y_pred_dask)
    end = time.time()
    print("Time of train and accuracy computations : ",end - start)
    print(f"{clf_name} Accuracy: {accuracy_dask}")
client.close()

