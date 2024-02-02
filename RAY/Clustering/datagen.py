from sklearn.datasets import make_swiss_roll
from sklearn.datasets import dump_svmlight_file
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn.metrics import davies_bouldin_score
from sklearn.decomposition import PCA
import argparse

def swiss_roll_generate_data(num_samples, noise):
    # Check if data_temp exists and if so, delete it
    if os.path.exists('data_temp.libsvm'):
        os.remove('data_temp.libsvm')
    open('data_temp.libsvm', 'a').close()

    # Empty the file before the new experiment
    if os.path.exists('data.libsvm'):
        os.remove('data.libsvm')
    open('data.libsvm', 'a').close()

    chunk_size = 10**6

    # Check if num_samples is greater than 10**6 and if so, create the dataset in chunks
    if num_samples > chunk_size:
        num_chunks = num_samples // chunk_size
        for i in range(num_chunks):
            print("Creating chunk {} of {}".format(i + 1, num_chunks))
            X, y = make_swiss_roll(n_samples=chunk_size, noise=noise, random_state=i)
            # Override the existing data in the temp file
            dump_svmlight_file(X, y, 'data_temp.libsvm', zero_based=False)

            # Concatenate the files
            if i == 0:
                os.system("cat data_temp.libsvm >> data.libsvm")
            else:
                os.system("cat data_temp.libsvm >> data.libsvm")
                os.system("rm data_temp.libsvm")

        remainder = num_samples % chunk_size
        if remainder != 0:
            print("Creating chunk {} of {}".format(num_chunks + 1, num_chunks + 1))
            X, y = make_swiss_roll(n_samples=remainder, noise=noise, random_state=num_chunks)
            dump_svmlight_file(X, y, 'data_temp.libsvm', zero_based=False)
            os.system("cat data_temp.libsvm >> data.libsvm")
            os.system("rm data_temp.libsvm")

        with open('data.libsvm.meta', 'w') as f:
            f.write('num_samples,{}\n'.format(num_samples))
            f.write('num_classes,{}\n'.format(len(np.unique(y))))
            f.write('dataset_size,{}'.format(os.path.getsize('data.libsvm') / 10**6))
            print("Dataset size is: {} MB".format(os.path.getsize('data.libsvm') / 10**6))
            f.close()
        return num_samples, noise, X, y

    else:
        X, y = make_swiss_roll(n_samples=num_samples, noise=noise, random_state=42)
        dump_svmlight_file(X, y, 'data.libsvm', zero_based=False)
        with open('data.libsvm.meta', 'w') as f:
            f.write('num_samples,{}\n'.format(num_samples))
            f.write('num_classes,{}\n'.format(len(np.unique(y))))
            f.write('dataset_size,{}'.format(os.path.getsize('data.libsvm') / 10**6))
            print("Dataset size is: {} MB".format(os.path.getsize('data.libsvm') / 10**6))
            f.close()

        return num_samples, noise, X, y


def main():
    parser = argparse.ArgumentParser(description='Generate Swiss Roll Data.')
    parser.add_argument('--num_samples', type=int, default=10000000, help='Number of samples')
    parser.add_argument('--noise', type=float, default=0.3, help='Noise level')

    args = parser.parse_args()

    # Call the function with command-line arguments
    swiss_roll_generate_data(num_samples=args.num_samples, noise=args.noise)

if __name__ == '__main__':
    main()