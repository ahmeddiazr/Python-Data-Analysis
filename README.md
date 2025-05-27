# Python Data Analysis : Dongsi Staton Air Quality Analysis Project

## Dashboard


## Project Overview
This project, submitted for the "Learn Data Analysis with Python" course from Dicoding, focuses on analyzing air quality data, particularly PM2.5 levels, from the Dongsi station. The objective is to uncover trends, seasonal variations, and the impact of different weather conditions on air quality.

## Table of Contents
- [Introduction](#introduction)
- [Data Source](#data-source)
- [Libraries Used](#libraries-used)
- [Key Insights](#key-insights)
- [How to Run the Dashboard](#how-to-run-the-dashboard)

## Introduction
The goal of this project is to analyze air quality data, specifically PM2.5 pollutant levels, and understand their relationship with various environmental factors. The analysis includes identifying trends, seasonal patterns, and correlations with weather conditions.

## Data Source
The dataset used in this project includes air quality measurements from the Dongsi station, with a focus on PM2.5 levels and other related environmental data.

## Libraries Used
- Streamlit
- Pandas
- Matplotlib
- Seaborn
- NumPy
- SciPy
- Statsmodels

## Key Insights
- Analisis menunjukkan bahwa konsentrasi PM2.5 di Dongsi menunjukkan pola musiman dan diurnal yang jelas. Tingkat PM2.5 yang lebih tinggi secara konsisten diamati selama bulan-bulan musim dingin karena berkurangnya dispersi atmosfer, peningkatan emisi pemanasan, dan kondisi cuaca yang stagnan. Sebaliknya, bulan-bulan musim panas menunjukkan konsentrasi PM2.5 yang lebih rendah, kemungkinan besar karena angin yang lebih kuat dan curah hujan yang lebih banyak membantu penyebaran polutan.
- Faktor-faktor iklim memainkan peran penting dalam memodulasi tingkat PM2.5. Kecepatan angin menunjukkan korelasi negatif yang kuat dengan PM2.5, karena kecepatan angin yang lebih tinggi meningkatkan penyebaran polutan dan mengurangi konsentrasi. Suhu menunjukkan korelasi negatif yang lemah, dengan suhu yang lebih hangat meningkatkan pencampuran atmosfer yang lebih baik dan menurunkan tingkat PM2.5. Suhu titik embun menunjukkan korelasi positif yang sedang, menunjukkan bahwa kelembapan yang lebih tinggi dapat berkontribusi pada pembentukan aerosol sekunder, yang meningkatkan PM2.5. Curah hujan juga berkorelasi negatif dengan PM2.5, yang bertindak sebagai mekanisme pembersihan alami dengan membersihkan materi partikulat. Wawasan ini menggarisbawahi pentingnya faktor meteorologi dalam membentuk dinamika kualitas udara.

## How to Run the Dashboard

To run the Air Quality Analysis Dashboard, follow these steps:

### Setup Environment

1. **Create and Activate a Python Environment**:
   - If using Conda (ensure [Conda](https://docs.conda.io/en/latest/) is installed):
     ```
     conda create --name airquality-ds python=3.9
     conda activate airquality-ds
     ```
   - If using venv (standard Python environment tool):
     ```
     python -m venv airquality-ds
     source airquality-ds/bin/activate  # On Windows use `airquality-ds\Scripts\activate`
     ```

2. **Install Required Packages**:
   - The following packages are necessary for running the analysis and the dashboard:
     ```
     pip install pandas numpy scipy matplotlib seaborn streamlit statsmodels
     ```

     or you can do
     ```
     pip install -r requirements.txt
     ```
### Run the Streamlit App

1. **Navigate to the Project Directory** where `dashboard.py` is located.

2. **Run the Streamlit App**:
    ```
    streamlit run dashboard.py
    ```
