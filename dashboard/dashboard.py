import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Konfigurasi Halaman
st.set_page_config(page_title="PM2.5 Analysis Dashboard", layout="wide")

# Judul
st.title("Projek Analisis Data Python: Dinamika Polutan PM2.5 di Dongsi, Beijing 2013-2017")
st.subheader("Oleh Ahmed Diaz Ravan")

# Load Data Function
@st.cache_data
def load_data():
    import os
    file_path = os.path.join("data", "PRSA_Data_Dongsi_20130301-20170228.csv")
    df = pd.read_csv(file_path)
    return df

# Load Data
df = load_data()

# Validasi Kolom
required_columns = ['PM2.5', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    st.error(f"Dataset tidak memiliki kolom berikut: {', '.join(missing_columns)}. Pastikan dataset valid.")
    st.stop()

# Konversi komponen penanggalan ke datetime index
df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
df.set_index('datetime', inplace=True)
df.drop(columns=['No', 'year', 'month', 'day', 'hour'], inplace=True)

# --- Sidebar Navigation ---
st.sidebar.title("Navigasi Halaman")
page_mapping = {
    "Data Overview - Tinjauan Umum Dataset": "Data Overview",
    "Data Cleaning - Pembersihan Data": "Data Cleaning",
    "Exploratory Data Analysis - Analisis Eksploratif": "Exploratory Data Analysis",
    "Correlation Analysis - Analisis Korelasi": "Correlation Analysis"
}
selected_page = st.sidebar.selectbox("Pilih Halaman", list(page_mapping.keys()))
page = page_mapping[selected_page]

# Filter Data untuk Analisis
st.sidebar.header("Filter Data untuk Analisis")

# Convert Timestamp to Python datetime
min_date = df.index.min().to_pydatetime()
max_date = df.index.max().to_pydatetime()

# Define slider
date_range = st.sidebar.slider(
    "Pilih Rentang Tanggal",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="YYYY-MM-DD"
)
st.sidebar.info(f"Menampilkan data dari {date_range[0].date()} hingga {date_range[1].date()}")

# filtering
df_filtered = df.loc[date_range[0]:date_range[1]]

# --- Page Logic ---
if page == "Data Overview":
    st.header("Data Overview")
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

elif page == "Data Cleaning":
    st.header("Data Cleaning")
    st.subheader("Duplikat Row")
    duplicates = df.duplicated().sum()
    st.write(f"Jumlah Row Duplikat: {duplicates}")
    
    st.subheader("Missing Values")
    missing_values = df.isnull().sum()
    st.write(missing_values)
    
    st.subheader("Persentase Missing Values:")
    missing_percentage = (df.isnull().mean() * 100).round(2)
    st.write(missing_percentage)
    
    # Heatmap for Missing Values
    cols_to_plot = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'wd', 'WSPM']
    cols_to_plot = [col for col in cols_to_plot if col in df.columns]
    if cols_to_plot:
        data_missing_plot = df[cols_to_plot].isnull()
        st.subheader("Heatmap Missing Values")
        fig, ax = plt.subplots(figsize=(20, 8))
        sns.heatmap(data_missing_plot.T, cmap='viridis', cbar=False)
        plt.title("Pola Missing Values Secara Berkala (2013-2017)")
        plt.xlabel("Date")
        plt.ylabel("Variable")
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.warning("Tidak ada kolom yang tersedia untuk heatmap missing values.")

    st.subheader("Insights")
    st.markdown("""
    - Terdapat persentase data hilang yang relatif rendah untuk sebagian besar polutan dan variabel cuaca.
    - Tingkat kehilangan data untuk Karbon Monoksida (CO) dan Nitrogen Dioksida (NO2) menunjukkan angka yang cukup tinggi, mencapai sekitar 9.12% dan 4.57%.
    """)

elif page == "Exploratory Data Analysis":
    st.header("Exploratory Data Analysis")
    if df_filtered.empty:
        st.warning("Data tidak tersedia untuk rentang tanggal yang dipilih.")
    else:
        st.subheader("Summary Statistics")
        st.write(df_filtered.describe())
        
        # Resample filtered data
        hourly_pm25 = df_filtered['PM2.5'].resample('h').mean()
        daily_pm25 = df_filtered['PM2.5'].resample('D').mean()
        monthly_pm25 = df_filtered['PM2.5'].resample('ME').mean()
        yearly_pm25 = df_filtered['PM2.5'].resample('YE').mean()
        
        # Hourly PM2.5 Analysis
        st.subheader("Hourly PM2.5 Analysis")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(x=hourly_pm25.index.hour, y=hourly_pm25.values)
        plt.title("Rata-rata Kadar PM2.5 Berdasarkan Jam (Data Terfilter)")
        plt.xlabel("Jam")
        plt.ylabel("Kadar PM2.5 (μg/m³)")
        st.pyplot(fig)
        plt.close(fig)
        
        # Daily PM2.5 Analysis
        st.subheader("Daily PM2.5 Analysis (Selected Range)")
        fig, ax = plt.subplots(figsize=(12, 6))
        plt.plot(daily_pm25, label="PM2.5")
        plt.title(f"Kadar PM2.5 Harian pada Rentang Terfilter ({date_range[0].date()} - {date_range[1].date()})")
        plt.xlabel("Tanggal")
        plt.ylabel("Kadar PM2.5 (μg/m³)")
        plt.legend()
        st.pyplot(fig)
        plt.close(fig)
        
        # Monthly PM2.5 Analysis
        st.subheader("Kadar PM2.5 Bulanan (Rentang Terfilter)")
        fig, ax = plt.subplots(figsize=(12, 6))
        plt.plot(monthly_pm25, label="PM2.5")
        plt.title("Kadar PM2.5 Bulanan (Rentang Terfilter)")
        plt.xlabel("Bulan")
        plt.ylabel("Kadar PM2.5 (μg/m³)")
        plt.legend()
        st.pyplot(fig)
        plt.close(fig)
        
        # Yearly PM2.5 Analysis
        st.subheader("Rata-rata Kadar PM2.5 Tahunan (Rentang Terfilter)")
        fig, ax = plt.subplots(figsize=(12, 6))
        if (date_range[1] - date_range[0]).days < 365 * 2:
            sns.lineplot(x=yearly_pm25.index, y=yearly_pm25.values)
            plt.xlabel("Tanggal")
        else:
            sns.lineplot(x=yearly_pm25.index.year, y=yearly_pm25.values)
            plt.xlabel("Tahun")
        plt.title("Rata-rata Kadar PM2.5 Tahunan (Rentang Terfilter)")
        plt.ylabel("Kadar PM2.5 (μg/m³)")
        st.pyplot(fig)
        plt.close(fig)

elif page == "Correlation Analysis":
    st.header("Correlation Analysis")
    if df_filtered.empty:
        st.warning("Data tidak tersedia untuk rentang tanggal yang dipilih.")
    else:
        relevant_cols = ['PM2.5', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
        relevant_cols = [col for col in relevant_cols if col in df_filtered.columns and pd.api.types.is_numeric_dtype(df_filtered[col])]

        if not relevant_cols:
            st.warning("Tidak ada kolom numerik yang relevan untuk analisis korelasi dalam data terfilter.")
        else:
            df_corr = df_filtered[relevant_cols]
            correlation_matrix = df_corr.corr()
            
            st.subheader("Matriks Korelasi (Data Terfilter)")
            st.write(correlation_matrix)
            
            st.subheader("Heatmap Korelasi (Data Terfilter)")
            fig, ax = plt.subplots(figsize=(12, 10))
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
            plt.title('Korelasi Antar Variabel Numerik (Data Terfilter)')
            st.pyplot(fig)
            plt.close(fig)
            
            st.subheader("Insights")
            st.markdown("""
            - Faktor-faktor iklim memainkan peran penting dalam memodulasi tingkat polutan.
            - Kecepatan angin (WSPM) umumnya menunjukkan korelasi negatif dengan PM2.5/PM10.
            - Suhu (TEMP) dan Titik Embun (DEWP) dapat berkorelasi dengan PM2.5/O3 tergantung kondisi atmosfer.
            """)

# --- Footer ---
st.sidebar.markdown("---")
st.sidebar.text("Dibuat oleh Ahmed Diaz Ravan")
st.sidebar.text("Email: diazravan@gmail.com")
