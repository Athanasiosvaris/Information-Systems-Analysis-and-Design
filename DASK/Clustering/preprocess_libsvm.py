def preprocess_libsvm(input_file, output_file):
    with open(input_file, 'r') as svm_file, open(output_file, 'w') as csv_file:
        for line in svm_file:
            parts = line.strip().split(' ')
            target = parts[0]
            features = [f.split(':')[1] for f in parts[1:]]
            csv_line = ','.join([target] + features)
            csv_file.write(csv_line + '\n')

if __name__ == "__main__":
    input_path = 'data.libsvm'
    output_path = 'data.csv'
    preprocess_libsvm(input_path, output_path)