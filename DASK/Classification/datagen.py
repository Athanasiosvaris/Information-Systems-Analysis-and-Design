import argparse
import os
from sklearn.datasets import make_classification
from sklearn.datasets import dump_svmlight_file

def classification_generate_data(num_samples, num_features):
    # Check if data_temp exists and if so, delete it
    if os.path.exists('data_temp.libsvm'):
        os.remove('data_temp.libsvm')
    open('data_temp.libsvm', 'a').close()

    # Empty the file before the new experiment
    if os.path.exists('data.libsvm'):
        os.remove('data.libsvm')
    open('data.libsvm', 'a').close()

    chunk_size = 3 * (10**5)

    # Check if num_samples is greater than 10**6 and if so, create the dataset in chunks
    if num_samples > chunk_size:
        num_chunks = num_samples // chunk_size
        for i in range(num_chunks):
            print("Creating chunk {} of {}".format(i+1, num_chunks))
            X, y = make_classification(
                n_samples=chunk_size,
                n_features=num_features,
                n_informative=num_features // 2,  # Adjust as needed
                n_redundant=num_features // 2,    # Adjust as needed
                n_classes=2  # Default number of classes is 2
            )

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
            print("Creating chunk {} of {}".format(num_chunks+1, num_chunks+1))
            X, y = make_classification(
                n_samples=remainder,
                n_features=num_features,
                n_informative=num_features // 2,  # Adjust as needed
                n_redundant=num_features // 2,    # Adjust as needed
                n_classes=2  # Default number of classes is 2
            )
            dump_svmlight_file(X, y, 'data_temp.libsvm', zero_based=False)
            os.system("cat data_temp.libsvm >> data.libsvm")
            os.system("rm data_temp.libsvm")
        # Write num_samples, num_features, num_labels, and dataset_size to a file
        with open('data.libsvm.meta', 'w') as f:
            f.write('num_samples,{}\n'.format(num_samples))
            f.write('num_features,{}\n'.format(num_features))
            f.write('num_classes,2\n')  # Default number of classes is 2
            f.write('dataset_size,{}'.format(os.path.getsize('data.libsvm')/10**6))
            print("Dataset size is: {} MB".format(os.path.getsize('data.libsvm')/10**6))
            f.close()

        return num_features, num_samples, X, y

    else:
        X, y = make_classification(
            n_samples=num_samples,
            n_features=num_features,
            n_informative=num_features // 2,  # Adjust as needed
            n_redundant=num_features // 2,    # Adjust as needed
            n_classes=2  # Default number of classes is 2
        )
        dump_svmlight_file(X, y, 'data.libsvm', zero_based=False)

        # Write num_samples, num_features, num_labels, and dataset_size to a file
        with open('data.libsvm.meta', 'w') as f:
            f.write('num_samples,{}\n'.format(num_samples))
            f.write('num_features,{}\n'.format(num_features))
            f.write('num_classes,2\n')  # Default number of classes is 2
            f.write('dataset_size,{}'.format(os.path.getsize('data.libsvm')/10**6))
            print("Dataset size is: {} MB".format(os.path.getsize('data.libsvm')/10**6))
            f.close()

        return num_features, num_samples, X, y

def main():
    parser = argparse.ArgumentParser(description='Generate Classification Data.')
    parser.add_argument('--num_samples', type=int, default=10000, help='Number of samples')
    parser.add_argument('--num_features', type=int, default=20, help='Number of features')

    args = parser.parse_args()

    # Call the function with command-line arguments
    classification_generate_data(num_samples=args.num_samples, num_features=args.num_features)

if __name__ == '__main__':
    main()