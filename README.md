![AeoLiS Banner](https://github.com/openearth/aeolis-shortcourse/blob/main/Sandmotor/notebooks/logo.png)

Hello, and welcome to the AeoLiS Short Course developed for Coastal Sediments '23! This short course will walk you through various 1D 
and 2D AeoLiS cases to introduce you to the model.AeoLiS is a process-based aeolian sediment transport model that simulates variaitons 
in sediment supply using multiple bed surface properties. The inclusion of bed surface properties such as sediment sorting and armoring, 
soil moisture content, and bed-slope effects make AeoLiS well suited for coastal environments where these conditions are oftern present. 
The use of AeoLiS in coastal environments allows for the modeling of berm feature changes due to the forcing factors of aeolian sediment 
transport and waves (in combination with tide). 

   * **Model source code can be found at:** https://github.com/openearth/aeolis-python

   * **Additional model description and documentation can be found at:** https://aeolis.readthedocs.io/

## AeoLiS Short Course Organization

The short course is organized such that there are two main folders, Sandmotor (2D cases) and **inset second folder name** (1D cases),
where within each folder are additional folders containing all required model input data and documentation for each case. Each of the 
different scenarios included in this short course introduce the includsion of different physical processes effecting aeolian sediment
transport. Each of the 2D and 1D scenarios included in the short course are outlined below.

#### Sandmotor (2D)
      
   1. Base Case 
   2. Grain Size Case 
   3. Grain Size Case with Inclusion of Tides 
   4. Grain Size Case with Inclusion of Tides & Waves 
  
#### Insert Folder Name Here (1D)
      
   1. Base Case 
   2. Inclusion of Surface Moisture
   3. Inclusion of Sand Fences
   4. Inclusion of Vegetation

Prior to starting the short course follow the steps below in Getting Started to download and install AeoLiS to your computer.

## Getting Started

#### Prerequisites

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
