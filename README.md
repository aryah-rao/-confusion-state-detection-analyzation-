### Understanding and Analyzing Confusion States

This folder contains code for understanding and analyzing confusion states using machine learning. It is built using Python and various machine learning libraries such as Scikit-Learn and TensorFlow. The code is divided into different steps, each with a specific purpose. The steps are:

- **story.ipynb**:
  - Includes plots of gaze direction, head pose, and facial landmarks over time.
  - Generates heatmaps of the correlation between features and confusion/help labels.

- **per_person**:
  - Trains a Random Forest and Neural Network on a dataframe of features for each person.
  - Plots the top n features for each model.
  - Applies t-SNE to visualize the data in 2D.

- **pca.ipynb**:
  - Reduces dimensionality with PCA while retaining 95% of explained variance.
  - Further reduces dimensionality with t-SNE for 2D visualization.
  - Uses scatter plots to visualize the distribution and separation of data points.

- **ml.ipynb**:
  - Loads and prepares the dataset by converting columns to boolean types and filtering features.
  - Analyzes feature importance with Random Forest and Neural Network models.
  - Visualizes data with time-series plots, boxplots, and violin plots.
  - Computes and visualizes the correlation matrix for selected features.
  - Generates classification reports with accuracy and precision metrics.

- **au.ipynb**:
  - Extracts AU intensity and presence data for analysis.
  - Computes mean AU activations for various labels.
  - Visualizes AU intensity differences with heatmaps.


The purpose of this code is to provide insights into the factors that contribute to confusion, and to enable the development of more responsive and adaptive systems.

