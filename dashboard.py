import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Konfigurasi Halaman
st.set_page_config(page_title="PM2.5 Analysis Dashboard", layout="wide")

# Judul
st.title("Projek Analisis Data Python: Dinamika Polutan PM2.5  di Dongsi, Beijing 2013-2017")
st.subheader("Oleh Ahmed Diaz Ravan")

# Sidebar
st.sidebar.title("Navigasi Halaman")
page = st.sidebar.selectbox(
    "Pilih Halaman",
    ["Data Overview", "Data Cleaning", "Exploratory Data Analysis", "Correlation Analysis"]
)

# Load Data Function
@st.cache_data
def load_data():
    import os
    file_path = os.path.join("data", "PRSA_Data_Dongsi_20130301-20170228.csv")
    df = pd.read_csv(file_path)
    return df

# Data Overview
if page == "Data Overview":
    st.header("Data Overview")
    df = load_data()
    st.subheader("Sample Data")
    st.write(df.head())
    
    st.subheader("Initial Assessment")
    st.write("Columns:", df.columns.tolist())
    st.write("Data Types:")
    st.write(df.dtypes)
    
    st.subheader("Insights")
    st.markdown("""
    - Dataset berisi pengukuran kualitas udara per jam dari stasiun pemantauan Dongsi, Beijing, periode 1 Maret 2013 hingga 28 Februari 2017.
    - Variabel utama meliputi konsentrasi polutan (PM2.5, PM10, SO2, NO2, CO, O3), faktor meteorologi (suhu, tekanan, titik embun, kecepatan/arah angin), dan parameter lingkungan lainnya.
    """)

# Data Cleaning
elif page == "Data Cleaning":
    st.header("Data Cleaning")
    df = load_data()
    
    # Drop Duplikat Row
    st.subheader("Duplikat Row")
    duplicates = df.duplicated().sum()
    st.write(f"Jumlah Row Duplikat: {duplicates}")
    
    # Missing Values
    st.subheader("Missing Values")
    missing_values = df.isnull().sum()
    st.write(missing_values)
    
    # Persentase Missing Values
    missing_percentage = (df.isnull().mean() * 100).round(2)
    st.write("Persentase Missing Values:")
    st.write(missing_percentage)
    
    # Heatmap Missing Values
    cols_to_plot = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'wd', 'WSPM']
    data_missing = df[cols_to_plot].isnull()
    data_missing['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
    data_missing.set_index('datetime', inplace=True)
    st.subheader("Heatmap Missing Values")
    fig, ax = plt.subplots(figsize=(20, 8))
    sns.heatmap(data_missing.T, cmap='viridis', cbar=False)
    plt.title("Pola Missing Values Secara Berkala (2013-2017)")
    plt.xlabel("Date")
    plt.ylabel("Variable")
    st.pyplot(fig)
    
    # Isi missing value numerik dengan mean
    numeric_cols = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
    df[numeric_cols] = df[numeric_cols].apply(lambda x: x.fillna(x.mean()), axis=0) 
    
    # Isi missing value kategorikal dengan modus
    categorical_cols = ['wd']
    df[categorical_cols] = df[categorical_cols].fillna(df[categorical_cols].mode().iloc[0])
    
    st.subheader("Missing Values Setelah Data Cleaning")
    st.write(df.isnull().sum())
    
    st.subheader("Insights")
    st.markdown("""
    - Terdapat persentase data hilang yang relatif rendah untuk sebagian besar polutan dan variabel cuaca. Secara spesifik, PM2.5 memiliki sekitar 2,14% data yang hilang, dan PM10 memiliki sekitar 1,58% data yang hilang.
    - Tingkat kehilangan data untuk Karbon Monoksida (CO) dan Nitrogen Dioksida (NO2) menunjukkan angka yang cukup tinggi dengan persentase masing-masing mencapai sekitar 9,12% dan 4,57%. Kehilangan data ini menunjukkan kemungkinan adanya kendala sistematis dalam mekanisme pengukuran yang memerlukan kajian mendalam.
    """)

# Exploratory Data Analysis
elif page == "Exploratory Data Analysis":
    st.header("Exploratory Data Analysis")
    df = load_data()
    
    # Convert Format ke Datetime
    df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
    df.set_index('datetime', inplace=True)
    df.drop(columns=['No', 'year', 'month', 'day', 'hour'], inplace=True)
    
    # Resample Data
    hourly_pm25 = df['PM2.5'].resample('h').mean()
    daily_pm25 = df['PM2.5'].resample('D').mean()
    monthly_pm25 = df['PM2.5'].resample('ME').mean()
    yearly_pm25 = df['PM2.5'].resample('YE').mean()
    
    # Kalkulasi rata-rata PM2.5 berdasarkan jam
    st.subheader("Hourly PM2.5 Analysis")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x=hourly_pm25.index.hour, y=hourly_pm25.values)
    plt.title("Rata-rata Kadar PM2.5 Berdasarkan Jam")
    plt.xlabel("Jam")
    plt.ylabel("Kadar PM2.5 (μg/m³)")
    st.pyplot(fig)
    
    # Kadar level PM2.5 harian (Studi kasus : January 2017)
    st.subheader("Daily PM2.5 Analysis (January 2017)")
    daily_pm25_january = daily_pm25['2017-01']
    fig, ax = plt.subplots(figsize=(12, 6))
    plt.plot(daily_pm25_january, label="PM2.5")
    plt.title("Kadar PM2.5 Harian pada Januari 2017")
    plt.xlabel("Tanggal")
    plt.ylabel("Kadar PM2.5 (μg/m³)")
    plt.legend()
    st.pyplot(fig)
    
    # Plot PM2.5 bulanan
    st.subheader("Kadar PM2.5 Bulanan (2013–2017)")
    fig, ax = plt.subplots(figsize=(12, 6))
    plt.plot(monthly_pm25, label="PM2.5")
    plt.title("Kadar PM2.5 Bulanan (2013–2017)")
    plt.xlabel("Bulan")
    plt.ylabel("Kadar PM2.5 (μg/m³)")
    plt.legend()
    st.pyplot(fig)
    
    # Plot PM2.5 tahunan
    st.subheader("Rata-rata Kadar PM2.5 Tahunan (2013-2017)")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x=yearly_pm25.index.year, y=yearly_pm25.values)
    plt.title("Rata-rata Kadar PM2.5 Tahunan (2013-2017)")
    plt.xlabel("Tahun")
    plt.ylabel("Kadar PM2.5 (μg/m³)")
    st.pyplot(fig)
    
    # Tabel rata-rata PM2.5 tahunan
    yearly_pm25_table = yearly_pm25.reset_index()
    yearly_pm25_table.columns = ['Tahun', 'Rata-rata PM2.5 (μg/m³)']
    yearly_pm25_table['Tahun'] = yearly_pm25_table['Tahun'].dt.year
    st.subheader("Rata-rata Kadar PM2.5 Tahunan (2013-2017)")
    st.table(yearly_pm25_table)
    
    st.subheader("Insights")
    st.markdown("""
    - Analisis menunjukkan bahwa konsentrasi PM2.5 di Dongsi menunjukkan pola musiman dan diurnal yang jelas. Tingkat PM2.5 yang lebih tinggi secara konsisten diamati selama bulan-bulan musim dingin karena berkurangnya dispersi atmosfer, peningkatan emisi pemanasan, dan kondisi cuaca yang stagnan. Sebaliknya, bulan-bulan musim panas menunjukkan konsentrasi PM2.5 yang lebih rendah, kemungkinan besar karena angin yang lebih kuat dan curah hujan yang lebih banyak membantu penyebaran polutan.
    """)
    
    # Summary Statistics
    st.subheader("Summary Statistics")
    st.write(df.describe())

# Analisis Hubungan / Korelasi
elif page == "Correlation Analysis":
    st.header("Correlation Analysis")
    df = load_data()
    
    # Kolom Relvan
    relevant_cols = ['PM2.5', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
    df_corr = df[relevant_cols]
    
    # Matriks Korelasi
    correlation_matrix = df_corr.corr()
    st.subheader("Matriks Korelasi")
    st.write(correlation_matrix)
    
    st.subheader("Insights")
    st.markdown("""
    - Faktor-faktor iklim memainkan peran penting dalam memodulasi tingkat PM2.5. Kecepatan angin menunjukkan korelasi negatif yang kuat dengan PM2.5, karena kecepatan angin yang lebih tinggi meningkatkan penyebaran polutan dan mengurangi konsentrasi. Suhu menunjukkan korelasi negatif yang lemah, dengan suhu yang lebih hangat meningkatkan pencampuran atmosfer yang lebih baik dan menurunkan tingkat PM2.5. Suhu titik embun menunjukkan korelasi positif yang sedang, menunjukkan bahwa kelembapan yang lebih tinggi dapat berkontribusi pada pembentukan aerosol sekunder, yang meningkatkan PM2.5. Curah hujan juga berkorelasi negatif dengan PM2.5, yang bertindak sebagai mekanisme pembersihan alami dengan membersihkan materi partikulat. Wawasan ini menggarisbawahi pentingnya faktor meteorologi dalam membentuk dinamika kualitas udara.
    """)

    
    # Scatter Plots
    st.subheader("Scatter Plots")
    with st.expander("Perluas untuk Melihat Plot Sebar"):
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Plot PM2.5 vs Suhu
        sns.scatterplot(data=df, x='TEMP', y='PM2.5', alpha=0.6, ax=axes[0, 0])
        axes[0, 0].set_title("PM2.5 vs Suhu")
        axes[0, 0].set_xlabel("Suhu (°C)")
        axes[0, 0].set_ylabel("Kadar PM2.5 (µg/m³)")
        axes[0, 0].grid(True, linestyle='--', alpha=0.6)
        
        # Plot PM2.5 vs Titik Embun
        sns.scatterplot(data=df, x='DEWP', y='PM2.5', alpha=0.6, ax=axes[0, 1])
        axes[0, 1].set_title("PM2.5 vs Titik Embun")
        axes[0, 1].set_xlabel("Titik Embun (°C)")
        axes[0, 1].set_ylabel("Kadar PM2.5 (µg/m³)")
        axes[0, 1].grid(True, linestyle='--', alpha=0.6)
        
        # Plot PM2.5 vs Curah Hujan
        sns.scatterplot(data=df, x='RAIN', y='PM2.5', alpha=0.6, ax=axes[1, 0])
        axes[1, 0].set_title("PM2.5 vs Curah Hujan")
        axes[1, 0].set_xlabel("Curah Hujan (mm)")
        axes[1, 0].set_ylabel("Kadar PM2.5 (µg/m³)")
        axes[1, 0].grid(True, linestyle='--', alpha=0.6)
        
        # Plot PM2.5 vs Kecepatan Angin
        sns.scatterplot(data=df, x='WSPM', y='PM2.5', alpha=0.6, ax=axes[1, 1])
        axes[1, 1].set_title("PM2.5 vs Kecepatan Angin")
        axes[1, 1].set_xlabel("Kecepatan Angin (m/s)")
        axes[1, 1].set_ylabel("Kadar PM2.5 (µg/m³)")
        axes[1, 1].grid(True, linestyle='--', alpha=0.6)
        
        plt.tight_layout()
        st.pyplot(fig)

# Footer
st.sidebar.markdown("---")
st.sidebar.text("Dibuat oleh Ahmed Diaz Ravan")
st.sidebar.text("Email: diazravan@gmail.com")