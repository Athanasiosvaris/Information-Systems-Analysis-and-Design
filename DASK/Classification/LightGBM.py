import dask.dataframe as dd
from dask_ml.model_selection import train_test_split
from dask.distributed import Client
from sklearn.metrics import accuracy_score,mean_absolute_error
import numpy as np
import dask.array as da
from sklearn.datasets import load_svmlight_file
import lightgbm as lgb
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

X_dask = X_dask.to_dask_array(lengths=True) 
Y_dask = Y_dask.to_dask_array(lengths=True) 

start = time.time()
X_train_dask, X_test_dask, Y_train_dask, Y_test_dask = train_test_split(
    X_dask, Y_dask, test_size=0.2, random_state=42, shuffle=True  
)

print("After train and split")

dask_reg = lgb.DaskLGBMRegressor(
        max_depth=5
)

dask_reg.fit(X_train_dask, Y_train_dask)
Y_pred_dask = dask_reg.predict(X_test_dask)
accuracy_dask = mean_absolute_error(Y_test_dask, Y_pred_dask)
end = time.time()
print("Time of train and accuracy computations : ",end - start)
print(f"Accuracy: {accuracy_dask}")

client.close()