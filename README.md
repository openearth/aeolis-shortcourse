![AeoLiS Banner](https://github.com/openearth/aeolis-shortcourse/blob/main/Sandmotor/notebooks/logo.png)

Hello, and welcome to the AeoLiS Short Course developed for Coastal Sediments '23! This short course will walk you through various 1D 
and 2D AeoLiS cases to introduce you to the model. AeoLiS is a process-based aeolian sediment transport model that simulates variations 
in sediment supply using multiple bed surface properties. The inclusion of bed surface properties such as sediment sorting and armoring, 
soil moisture content, and bed-slope effects make AeoLiS well suited for coastal environments where these conditions are often present. 
The use of AeoLiS in coastal environments allows for the modeling of berm feature changes due to the forcing factors of aeolian sediment 
transport and waves (in combination with tide). 

   * **Model source code can be found at:** https://github.com/openearth/aeolis-python

   * **Additional model description and documentation can be found at:** https://aeolis.readthedocs.io/

## AeoLiS Short Course Organization

The short course is organized such that there are two main folders, Sandmotor (2D cases) and Dune In Front of Dike - DIFD (1D cases),
where within each folder are additional folders containing all required model input data and documentation for each case. Each of the 
different scenarios included in this short course introduce the inclusion of different physical processes affecting aeolian sediment
transport. Each of the 2D and 1D scenarios included in the short course are outlined below.

#### Sandmotor (2D)   
   1. Base Case 
   2. Grain Size Case 
   3. Grain Size Case with Inclusion of Tides 
   4. Grain Size Case with Inclusion of Tides & Waves 
  
#### Dune In Front of Dike - DIFD (1D)
   1. Base Case 
   2. Inclusion of Surface Moisture
   3. Inclusion of Sand Fences
   4. Inclusion of Vegetation

Prior to starting the short course follow the steps below in **Getting Started** to download and install AeoLiS to your computer.

## Getting Started

#### Prerequisites

Before starting the short course, please make sure you have Python installed on your computer and access to a terminal window (terminal or Anaconda Prompt). 
It is recommended to have Anaconda installed (https://docs.anaconda.com/anaconda/install/) prior to starting the short course as this program includes all of the necessary programs to install AeoLiS and complete the short course. 
To simplify the process of installing the dependencies needed for this short course, we have prepared a conda environment file. 

#### Installing AeoLiS

1. Open either a terminal window or Anaconda Prompt window
   * If you are using a Linux or Apple computer, open a new terminal window
   * If you are using a Windows computer, open Anaconda Prompt 
2. Download the aeolis short course repository on your computer by going to the URL https://github.com/openearth/aeolis-shortcourse and clicking on the button `Code` -> `Download zip`
3. Unzip the downloaded zip file on your computer at the location of your choice and navigate to the extracted directory in the terminal.
    ```sh
    cd aeolis-shortcourse-main
    ```
4. Create a new conda environment by typing the following into your terminal window
   ```sh
   conda env create -f environment.yml
   ```
   when prompted to proceed type: y

   Alternatively, you could use the Anaconda graphical user interface to import the environment.yml file and create an environment from it.
5. Activate the newly created conda environment with the following command
   ```sh
   conda activate aeolis_env
   ```
   when this step is complete you should see (aeolis_env) on the far left of your terminal command line before your current path.
   
6. You can now run AeoLiS from the command line by running 
   ```sh
   aeolis [configfile]
   ```
   and open the jupyter notebook application by running
   ```sh
   jupyter notebook
   ```
7. Happy modelling!!
