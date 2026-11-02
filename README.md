# 🚲 Capital Bikeshare Rental Analytics Dashboard

Proyek akhir analisis data untuk kelas **"Belajar Analisis Data dengan Python"** di **Dicoding Indonesia**. Proyek ini mencakup seluruh siklus analisis data mulai dari perumusan pertanyaan bisnis menggunakan metode SMART, data wrangling, exploratory data analysis (EDA), visualisasi data berintegritas tinggi, analisis lanjutan (*clustering* & *binning* non-machine learning), hingga perancangan dashboard interaktif berbasis Streamlit.

---

## 👤 Informasi Mahasiswa
- **Nama:** M Fikkan El Haq
- **Email:** mfikkanel@gmail.com
- **ID Dicoding:** fikkanel
- **Tautan Dashboard Streamlit:** [bike-sharing-analytics-fikkan.streamlit.app](https://bike-sharing-analytics-fikkan.streamlit.app/)

---

## 📂 Struktur Direktori Proyek

Struktur folder submission ini disusun mengikuti standar panduan resmi Dicoding:

```text
submission/
├── dashboard/
│   ├── dashboard.py         # Skrip antarmuka aplikasi dashboard Streamlit
│   ├── main_data.csv        # Dataset harian bersih hasil wrangling untuk visualisasi
│   └── hour_clean.csv       # Dataset per jam bersih untuk analisis pola komuter
├── data/
│   ├── day.csv              # Dataset mentah agregasi harian (Capital Bikeshare)
│   ├── hour.csv             # Dataset mentah agregasi per jam
│   └── Readme.txt           # Dokumentasi lisensi dan definisi fitur dataset
├── notebook.ipynb           # Jupyter Notebook analisis lengkap (sudah dieksekusi)
├── README.md                # Dokumentasi proyek dan panduan instalasi
├── requirements.txt         # Daftar pustaka dependensi Python
└── url.txt                  # Tautan live dashboard Streamlit Cloud
```

---

## 🎯 Pertanyaan Bisnis (SMART Framework)

1. **Pertanyaan 1 (Tren Waktu, Musim & Cuaca):**  
   *Bagaimana tren total penyewaan sepeda bulanan pada periode Januari 2011 hingga Desember 2012, serta pada musim (season) dan kondisi cuaca (weather situation) apa volume penyewaan mencapai angka tertinggi, sebagai dasar penjadwalan perawatan armada dan kesiapan kapasitas?*
2. **Pertanyaan 2 (Pola Pengguna Casual vs Registered):**  
   *Bagaimana perbedaan pola rata-rata penyewaan sepeda antara pengguna kasual (casual) dan pengguna terdaftar (registered) pada hari kerja (workingday) versus hari libur/akhir pekan (weekend/holiday) sepanjang 2011–2012, serta pada rentang jam berapa (hourly peak) lonjakan permintaan terjadi, sebagai dasar perencanaan redistribusi armada antar-stasiun dan promo konversi pengguna kasual?*
3. **Pertanyaan 3 (Analisis Lanjutan - Segmentasi Waktu & Suhu):**  
   *Bagaimana variasi jumlah penyewaan sepeda ketika dikelompokkan ke dalam klaster segmen waktu harian (Part of Day: Dini Hari, Pagi Sibuk, Jam Kerja/Siang, Sore Sibuk, Malam) dan kategori suhu lingkungan (Dingin, Sejuk, Hangat/Ideal, Panas) sepanjang 2011–2012, sebagai dasar penjadwalan logistik dan perawatan di jam sepi?*

---

## 📊 Ringkasan Temuan Utama

1. **Pertumbuhan Masif YoY (+64,88%):**  
   Total peminjaman sepeda melonjak dari **1.243.103 unit** (2011) menjadi **2.049.576 unit** (2012), dengan puncak bulanan tertinggi tercapai pada September 2012 (218.573 unit).
2. **Pengaruh Musim & Cuaca:**  
   Musim Gugur (*Fall*) mencatatkan rata-rata sewa harian tertinggi (**5.644 unit/hari**), disusul Musim Panas (**4.992 unit/hari**). Cuaca cerah mendominasi (**4.877 unit/hari**), sedangkan cuaca hujan/salju menyebabkan penurunan sewa hingga 63,0% (**1.803 unit/hari**).
3. **Karakteristik Pengguna (Hari Kerja vs Akhir Pekan):**  
   - Pada hari kerja, pengguna terdaftar mendominasi hingga **86,77%** dengan rata-rata **3.978 unit/hari** dan lonjakan komuter bimodal pada pukul **08:00** dan **17:00–18:00**.
   - Pada akhir pekan/hari libur, peminjaman kasual melonjak lebih dari dua kali lipat menjadi rata-rata **1.371 unit/hari** (**31,66%**) dengan puncak rekreasi unimodal di siang hari pada rentang **12:00–16:00**.
4. **Analisis Lanjutan:**  
   Segmen Sore Sibuk (16:00–20:00) menyumbang sepertiga beban operasional sistem (rata-rata 377,6 unit/jam), sementara dini hari (00:00–06:00) sangat tenang (24,9 unit/jam), menjadikannya waktu ideal untuk pemeliharaan unit dan redistribusi armada.

---

## 🚀 Panduan Menjalankan Proyek Secara Lokal

### 1. Prasyarat Lingkungan
Pastikan komputer Anda telah terpasang:
- Python 3.9 atau versi yang lebih baru
- Git (opsional)

### 2. Membuka Direktori Proyek
Buka terminal (Command Prompt, PowerShell, atau Terminal macOS/Linux) dan arahkan ke folder `submission`:
```bash
cd "C:\FIKKAN\kuliah\SEMESTER 5\DATA SCIENCE\Assignment\Submission belajar analisis data untuk pemula\submission"
```

### 3. Membuat Virtual Environment (Disarankan)
```bash
# Membuat virtual environment
python -m venv venv

# Mengaktifkan environment di Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Atau di Command Prompt Windows:
.\venv\Scripts\activate.bat

# Atau di Linux/macOS:
source venv/bin/activate
```

### 4. Memasang Dependensi
Pasang semua pustaka yang dibutuhkan melalui file `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 5. Menjalankan Jupyter Notebook
Untuk melihat seluruh proses wrangling, EDA, dan visualisasi:
```bash
jupyter notebook notebook.ipynb
# atau
jupyter lab
```

### 6. Menjalankan Dashboard Streamlit
Jalankan perintah berikut dari direktori root `submission`:
```bash
streamlit run dashboard/dashboard.py
```
Aplikasi dashboard akan otomatis terbuka di browser Anda pada alamat:  
`http://localhost:8501`

---

## ☁️ Panduan Deploy ke Streamlit Community Cloud

1. Buat repositori baru di akun GitHub Anda (misal `bike-sharing-dashboard`).
2. Unggah seluruh isi folder `submission` ke repositori tersebut.
3. Kunjungi [share.streamlit.io](https://share.streamlit.io/) dan masuk dengan akun GitHub Anda.
4. Klik **"New app"**, pilih repositori Anda, tentukan branch `main`, dan set *Main file path* ke:  
   `dashboard/dashboard.py`
5. Klik **"Deploy"** dan salin tautan URL yang dihasilkan ke berkas `url.txt`.
