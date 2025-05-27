# Python Data Analysis : Dongsi Staton Air Quality Analysis Project

## Dashboard


## Project Overview
Proyek ini, yang diajukan untuk course "Belajar Analisis Data dengan Python" dari Dicoding, berfokus pada analisis data kualitas udara, khususnya tingkat PM2.5, dari stasiun Dongsi. Tujuan utamanya adalah untuk mengamati tren, variasi musiman, dan dampak berbagai kondisi cuaca terhadap kualitas udara.

## Table of Contents
- [Introduction](#introduction)
- [Data Source](#data-source)
- [Libraries Used](#libraries-used)
- [Key Insights](#key-insights)
- [How to Run the Dashboard](#how-to-run-the-dashboard)

## Introduction
Tujuan utama proyek ini adalah untuk menganalisis data kualitas udara, khususnya tingkat polutan PM2.5, serta memahami hubungan mereka dengan berbagai faktor lingkungan. Analisis mencakup identifikasi tren, pola musiman, dan korelasi dengan kondisi cuaca.

## Data Source
Dataset yang digunakan dalam proyek ini mencakup pengukuran kualitas udara dari stasiun Dongsi, dengan fokus pada tingkat PM2.5 dan data lingkungan terkait lainnya.

## Libraries Used
Streamlit : Untuk membuat dashboard interaktif.
Pandas : Untuk manipulasi dan analisis data.
Matplotlib & Seaborn : Untuk visualisasi data.
NumPy : Untuk komputasi numerik.
SciPy & Statsmodels : Untuk analisis statistik lanjutan.

## Key Insights
- Analisis menunjukkan bahwa konsentrasi PM2.5 di Dongsi menunjukkan pola musiman dan diurnal yang jelas. Tingkat PM2.5 yang lebih tinggi secara konsisten diamati selama bulan-bulan musim dingin karena berkurangnya dispersi atmosfer, peningkatan emisi pemanasan, dan kondisi cuaca yang stagnan. Sebaliknya, bulan-bulan musim panas menunjukkan konsentrasi PM2.5 yang lebih rendah, kemungkinan besar karena angin yang lebih kuat dan curah hujan yang lebih banyak membantu penyebaran polutan.
- Faktor-faktor iklim memainkan peran penting dalam memodulasi tingkat PM2.5. Kecepatan angin menunjukkan korelasi negatif yang kuat dengan PM2.5, karena kecepatan angin yang lebih tinggi meningkatkan penyebaran polutan dan mengurangi konsentrasi. Suhu menunjukkan korelasi negatif yang lemah, dengan suhu yang lebih hangat meningkatkan pencampuran atmosfer yang lebih baik dan menurunkan tingkat PM2.5. Suhu titik embun menunjukkan korelasi positif yang sedang, menunjukkan bahwa kelembapan yang lebih tinggi dapat berkontribusi pada pembentukan aerosol sekunder, yang meningkatkan PM2.5. Curah hujan juga berkorelasi negatif dengan PM2.5, yang bertindak sebagai mekanisme pembersihan alami dengan membersihkan materi partikulat. Wawasan ini menggarisbawahi pentingnya faktor meteorologi dalam membentuk dinamika kualitas udara.

## How to Run the Dashboard

Untuk menjalankan Dasbor Analisis Kualitas Udara, ikuti langkah-langkah berikut:

### Mengatur Environment

1. **Buat dan Aktifkan Lingkungan Python**:
   - Jika menggunakan Conda (pastikan [Conda] (https://docs.conda.io/en/latest/) telah terinstal):
     ```
     conda create --name airquality-ds python=3.9
     conda activate airquality-ds
     ```
   - Jika menggunakan venv (alat lingkungan Python standar):
     ```
     python -m venv airquality-ds
     source airquality-ds/bin/activate 
     ```

2. **Instal Paket-paket yang Dibutuhkan**:
   - Paket-paket berikut ini diperlukan untuk menjalankan analisis dan dasbor:
     ```
     pip install pandas numpy scipy matplotlib seaborn streamlit statsmodels
     ```

     atau Anda dapat melakukan
     ```
     pip install -r requirements.txt
     ```
### Menjalankan Aplikasi Streamlit

1. **Arahkan ke Direktori Proyek** di mana `dashboard.py` berada.

2. **Jalankan Aplikasi Streamlit**:
    ```
    streamlit run dashboard.py
    ```
