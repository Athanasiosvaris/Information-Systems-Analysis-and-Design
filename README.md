# Comparison between Python Scaling Frameworks for Big Data Analysis and ML
Term project for the course 'Information-Systems-Analysis-and-Design' during 9th semester at NTUA
s  
# Introduction
This project involves comparing two prominent Python scaling frameworks, Ray and Dask, for big data analysis and machine learning tasks. Ray and Dask are open-source frameworks designed to facilitate the parallel execution of Python code for distributed computing tasks. This comparison aims to evaluate their performance, scalability, and ease of use in handling large-scale data analytics and ML workloads.

# Project Steps
You need to follow the following steps in order to run the python scripts :  

1. Installation and setup of Virtual Machines: Using Okeanos-documentation create and set-up your virtual machines. In this project we used a total of 3 VMs with 8 gigabyte of ram and 30 gigabyte of disk storage and 4 cpus each (1 master-2 workers).
2. Create a private network with the three VMs.
3. Install Ray and Dask frameworks.
4. Install all the necessary libraries.
5. Insert only in <b>master</b> node Ray and Dask folders of this repository.
6. For <b> classification</b> :
   a)Create test data using <b>datagen.py</b> function: python3 datagen.py --num_samples <num_samples> --num_features <features>
   b)
