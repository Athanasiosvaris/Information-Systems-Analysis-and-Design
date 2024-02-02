# Comparison between Python Scaling Frameworks for Big Data Analysis and Machine Learning

Term project for the course 'Information-Systems-Analysis-and-Design' during the 9th semester at NTUA in the School of Electrical and Computer Engineering under the supervision of Professor Dimitrios Tsoumakos.

## Introduction

This project involves comparing two prominent Python scaling frameworks, Ray and Dask, for big data analysis and machine learning tasks. Ray and Dask are open-source frameworks designed to facilitate the parallel execution of Python code for distributed computing tasks. This comparison aims to evaluate their performance, scalability, and ease of use in handling large-scale data analytics and ML workloads.

### Background
Python has emerged as a popular programming language for data analysis and machine learning due to its simplicity, versatility, and extensive ecosystem of libraries and frameworks. However, as datasets continue to grow in size and complexity, traditional single-machine solutions become inadequate for processing and analyzing such data efficiently. This has led to the development of distributed computing frameworks like Ray and Dask, which enable parallel execution across multiple nodes or cores, thereby allowing users to scale their data analysis and ML workflows to handle large-scale datasets.

## Project Objectives

1. **Installation and Setup:** Successfully install and configure Ray and Dask frameworks on local or cloud-based resources.
2. **Data Loading and Preprocessing:** Generate or acquire real-world datasets and load them into Ray and Dask for analysis. Perform necessary preprocessing steps to prepare the data for analysis.
3. **Performance Measurement:** Develop a suite of Python scripts to benchmark the performance of Ray and Dask across various data processing and ML tasks. Evaluate their scalability and efficiency under different workload scenarios.
4. **Comparison Analysis:** Analyze and compare the performance, scalability, and ease of use of Ray and Dask based on the results obtained from the performance measurement phase. Identify the strengths and weaknesses of each framework for different types of tasks and workloads.

## Project Steps

To run the Python scripts, follow these steps:

1. **Installation and Setup of Virtual Machines:**
   - Using Okeanos-documentation, create and set up your virtual machines. In this project, we used a total of 3 VMs with 8 gigabytes of RAM and 30 gigabytes of disk storage and 4 CPUs each (1 master-2 workers).
   - Create a private network with the three VMs.

2. **Framework Installation:**
   - Install Ray and Dask frameworks.
   - Install all necessary libraries.

3. **Data Loading and Preprocessing:**
   - Generate test data using the `datagen.py` function:
     ```
     python3 datagen.py --num_samples <num_samples> --num_features <features>
     ```

4. **Classification:**
   - For Dask:
     - Convert the `data.libsvm` file to a CSV file using the `convert_libsvm_to_csv` function.
     - Run `Dask scheduler` to initiate the Dask cluster.
     - Connect to the worker VMs and run `dask worker tcp://<ip_address:port>`
     - Run the `.py` file.

   - For Ray:
     - Move the `data.libsvm` file to the `ray` folder.
     - Initiate the cluster with `ray start --head --dashboard-host "0.0.0.0"`.
     - Connect to the cluster with a worker node using `ray start --address='ip_address:port'`.
     - Run the `.py` file.

5. **Clustering:**
   - Follow the same steps as in the clustering folder.

## Team Members

- **Athanasios Varis**
- **Georgios Vlachopoulos**
- **Ioannis Nikiforidis**

## References

- [Ray Documentation](https://docs.ray.io/)
- [Dask Documentation](https://docs.dask.org/)
