![AeoLiS Banner](https://github.com/openearth/aeolis-shortcourse/blob/main/Sandmotor/notebooks/logo.png)

# AeoLiS Short Course

Hello, and welcome to the AeoLiS Short Course developed for Coastal Sediments '23. This short course will walk you through various 1D and 2D AeoLiS cases to introduce you to the model. 
The short course is organized such that there are two main folders, Sandmotor (2D cases) and **insert second folder name** (1D cases), and within each folder are additional folders containing environmental data, model inputs, and documentation for the different
scenarios included in the course where each scenario introduces the inclusion of different physical processes effecting aeolian sediment transport.



## Getting Started

#### Prerequisits

Before starting the short course, please make sure you have Python installed on your computer and access to a terminal window (terminal or Anaconda Prompt). 
It is recommended to have Anaconda installed prior to starting the short course as this program includes all of the necessary programs to install AeoLiS and complete the short course. 

#### Installing AeoLiS

1. Open either a terminal window or Anaconda Prompt window
   - If you are using a Linux or Apple computer, open a new terminal window
   - If you are using a Windows computer, open Anaconda Prompt 
2. Create a new conda environment by typing the following into your terminal window
   ```sh
   conda create -n aeolis_env python=3.8
   ```
   when prompted to proceed type: y
3. Activate the newly created conda environment with the following command
   ```sh
   conda activate aeolis_env
   ```
   when this step is complete you should see (aeolis_env) on the far left of your terminal command line before your current path
4. Install git to the activated conda environment with the following command
   ```sh
   conda install git
   ```
   when prompted to proceed type: y
5. Download and install AeoLiS from the OpenEarth AeoLiS GitHub
   ```sh
   pip install git+https://github.com/openearth/aeolis-python
   ```
6. Install Python package to run Jupyter notebook for the short course
   ```sh
   pip install notebook
   ```
