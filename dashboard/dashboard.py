import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter

# ---------------------------------------------------------
# Helper: Indonesian Number Formatting
# ---------------------------------------------------------
def format_id(val, decimals=0):
    if val is None or pd.isna(val):
        return "-"
    if decimals == 0:
        return f"{int(round(val)):,}".replace(",", ".")
    parts = f"{val:.{decimals}f}".split(".")
    int_part = f"{int(parts[0]):,}".replace(",", ".")
    return f"{int_part},{parts[1]}"

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Capital Bikeshare Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Typography and Layout Styling
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Kurangi padding atas halaman */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
    
    /* Ukuran font angka st.metric agar tidak terpotong */
    div[data-testid="stMetric"] {
        overflow: visible !important;
    }
    div[data-testid="stMetricValue"], 
    div[data-testid="stMetricValue"] * {
        font-size: 1.35rem !important;
        line-height: 1.2 !important;
        overflow: visible !important;
        text-overflow: clip !important;
        white-space: nowrap !important;
    }
    div[data-testid="stMetricLabel"],
    div[data-testid="stMetricLabel"] * {
        font-size: 0.82rem !important;
        color: #475569 !important;
        white-space: nowrap !important;
    }
    
    .page-title {
        font-size: 1.55rem;
        font-weight: 700;
        color: #0f172a;
        letter-spacing: -0.015em;
        margin-bottom: 0.15rem;
    }
    
    .page-subtitle {
        font-size: 0.92rem;
        color: #64748b;
        margin-bottom: 1.25rem;
        line-height: 1.4;
    }
    
    .section-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #1e293b;
        margin-top: 0.6rem;
        margin-bottom: 0.6rem;
    }
    
    .insight-paragraph {
        font-size: 0.88rem;
        color: #334155;
        line-height: 1.6;
        margin-top: 0.6rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Matplotlib and Seaborn Style Configuration
# ---------------------------------------------------------
def apply_plot_style():
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['Segoe UI', 'Arial', 'DejaVu Sans'],
        'font.size': 8.5,
        'axes.titlesize': 10.5,
        'axes.titleweight': 'bold',
        'axes.titlepad': 10,
        'axes.labelsize': 8.5,
        'axes.labelweight': 'normal',
        'xtick.labelsize': 8.0,
        'ytick.labelsize': 8.0,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.spines.left': True,
        'axes.spines.bottom': True,
        'axes.edgecolor': '#cbd5e1',
        'axes.linewidth': 0.8,
        'grid.color': '#f1f5f9',
        'grid.linestyle': '-',
        'grid.linewidth': 0.8,
        'grid.alpha': 1.0,
        'figure.facecolor': '#ffffff',
        'axes.facecolor': '#ffffff'
    })

apply_plot_style()

# ---------------------------------------------------------
# Data Loading
# ---------------------------------------------------------
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    main_path = os.path.join(base_dir, "main_data.csv")
    hour_path = os.path.join(base_dir, "hour_clean.csv")

    if not os.path.exists(main_path):
        main_path = os.path.join(base_dir, "dashboard", "main_data.csv")
    if not os.path.exists(hour_path):
        hour_path = os.path.join(base_dir, "dashboard", "hour_clean.csv")

    day = pd.read_csv(main_path)
    hour = pd.read_csv(hour_path)

    day['dteday'] = pd.to_datetime(day['dteday'])
    hour['dteday'] = pd.to_datetime(hour['dteday'])

    return day, hour

try:
    day_df, hour_df = load_data()
except Exception as e:
    st.error(f"Gagal memuat dataset: {e}")
    st.stop()

# ---------------------------------------------------------
# Sidebar Filter
# ---------------------------------------------------------
with st.sidebar:
    st.subheader("Capital Bikeshare")
    st.caption("Laporan analitik data 2011-2012")

    min_date = day_df['dteday'].min().date()
    max_date = day_df['dteday'].max().date()

    date_range = st.date_input(
        "Rentang tanggal",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date

    all_seasons = list(day_df['season_label'].unique())
    selected_seasons = st.multiselect(
        "Musim",
        options=all_seasons,
        default=all_seasons
    )

    all_weathers = list(day_df['weather_label'].unique())
    selected_weathers = st.multiselect(
        "Kondisi cuaca",
        options=all_weathers,
        default=all_weathers
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("Informasi analis")
    st.markdown("""
    - Nama: M Fikkan El Haq
    - Email: mfikkanel@gmail.com
    - ID Dicoding: DS284B6Y0938
    """)

# ---------------------------------------------------------
# Filter Application
# ---------------------------------------------------------
mask_day = (
    (day_df['dteday'].dt.date >= start_date) &
    (day_df['dteday'].dt.date <= end_date) &
    (day_df['season_label'].isin(selected_seasons)) &
    (day_df['weather_label'].isin(selected_weathers))
)
filtered_day = day_df[mask_day]

mask_hour = (
    (hour_df['dteday'].dt.date >= start_date) &
    (hour_df['dteday'].dt.date <= end_date) &
    (hour_df['season_label'].isin(selected_seasons)) &
    (hour_df['weather_label'].isin(selected_weathers))
)
filtered_hour = hour_df[mask_hour]

if filtered_day.empty:
    st.info("Tidak ada data yang sesuai dengan kombinasi filter yang dipilih.")
    st.stop()

# ---------------------------------------------------------
# Header and Summary Metrics
# ---------------------------------------------------------
st.markdown('<div class="page-title">Capital Bikeshare Analytics Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Laporan analitik performa operasional, pola komuter, dan pengaruh lingkungan periode 2011-2012.</div>', unsafe_allow_html=True)

total_rentals = filtered_day['cnt'].sum()
total_registered = filtered_day['registered'].sum()
total_casual = filtered_day['casual'].sum()
avg_daily = filtered_day['cnt'].mean()

pct_reg = (total_registered / total_rentals) * 100 if total_rentals > 0 else 0
pct_cas = (total_casual / total_rentals) * 100 if total_rentals > 0 else 0

formatter_y = FuncFormatter(lambda x, pos: format_id(x, 0))

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total penyewaan", value=format_id(total_rentals))
with col2:
    st.metric(label="Pengguna terdaftar", value=format_id(total_registered))
    st.caption(f"{format_id(pct_reg, 1)}% dari total")
with col3:
    st.metric(label="Pengguna kasual", value=format_id(total_casual))
    st.caption(f"{format_id(pct_cas, 1)}% dari total")
with col4:
    st.metric(label="Rata-rata sewa/hari", value=format_id(avg_daily))

st.divider()

# ---------------------------------------------------------
# Navigation Tabs
# ---------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "Tren dan cuaca",
    "Komuter dan rekreasi",
    "Analisis lanjutan"
])

# ---------------------------------------------------------
# TAB 1: Tren dan cuaca
# ---------------------------------------------------------
with tab1:
    apply_plot_style()
    
    # 1. Monthly Trend Plot
    monthly_trend = filtered_day.groupby(['year_label', 'month_label', 'mnth']).agg({'cnt': 'sum'}).reset_index().sort_values(by=['year_label', 'mnth'])
    
    fig_trend, ax_trend = plt.subplots(figsize=(11, 3.8))
    has_2011 = 2011 in monthly_trend['year_label'].values
    has_2012 = 2012 in monthly_trend['year_label'].values

    if has_2011:
        sub_2011 = monthly_trend[monthly_trend['year_label'] == 2011]
        ax_trend.plot(sub_2011['month_label'], sub_2011['cnt'], marker='o', markersize=4, linewidth=1.8, color='#94a3b8', label='2011')
    
    if has_2012:
        sub_2012 = monthly_trend[monthly_trend['year_label'] == 2012]
        ax_trend.plot(sub_2012['month_label'], sub_2012['cnt'], marker='o', markersize=4, linewidth=2.2, color='#1d4ed8', label='2012')

    ax_trend.set_title("Penyewaan 2012 lebih tinggi di semua bulan dibanding 2011", loc='left')
    ax_trend.set_xlabel("Bulan")
    ax_trend.set_ylabel("Total sewa")
    ax_trend.yaxis.set_major_formatter(formatter_y)
    ax_trend.legend(frameon=False)
    ax_trend.grid(axis='y')
    st.pyplot(fig_trend)
    plt.close(fig_trend)

    # 2. Season and Weather Comparison
    col_season, col_weather = st.columns(2)

    with col_season:
        season_agg = filtered_day.groupby('season_label').agg(avg=('cnt', 'mean')).reset_index()
        season_order = [s for s in ['Fall', 'Summer', 'Winter', 'Spring'] if s in season_agg['season_label'].values]
        season_agg = season_agg.set_index('season_label').reindex(season_order).reset_index()

        max_season = season_agg.loc[season_agg['avg'].idxmax(), 'season_label'] if not season_agg.empty else ""
        palette_s = {s: ('#1d4ed8' if s == max_season else '#cbd5e1') for s in season_order}

        fig_s, ax_s = plt.subplots(figsize=(5.5, 3.5))
        sns.barplot(data=season_agg, x='season_label', y='avg', hue='season_label', palette=palette_s, legend=False, ax=ax_s)
        ax_s.set_title("Musim gugur mencatat rata-rata harian tertinggi", loc='left')
        ax_s.set_xlabel("Musim")
        ax_s.set_ylabel("Rata-rata sewa per hari")
        ax_s.yaxis.set_major_formatter(formatter_y)
        for p in ax_s.patches:
            val = p.get_height()
            if not np.isnan(val) and val > 0:
                ax_s.annotate(format_id(val, 0), (p.get_x() + p.get_width() / 2., val),
                              ha='center', va='bottom', xytext=(0, 3), textcoords='offset points', fontsize=7.5)
        ax_s.grid(axis='y')
        st.pyplot(fig_s)
        plt.close(fig_s)

    with col_weather:
        weather_agg = filtered_day.groupby('weather_label').agg(avg=('cnt', 'mean')).reset_index()
        weather_order = [w for w in ['Clear/Partly Cloudy', 'Misty/Cloudy', 'Light Snow/Rain'] if w in weather_agg['weather_label'].values]
        weather_agg = weather_agg.set_index('weather_label').reindex(weather_order).reset_index()

        palette_w = {w: ('#1d4ed8' if w == 'Clear/Partly Cloudy' else '#cbd5e1') for w in weather_order}

        fig_w, ax_w = plt.subplots(figsize=(5.5, 3.5))
        sns.barplot(data=weather_agg, x='weather_label', y='avg', hue='weather_label', palette=palette_w, legend=False, ax=ax_w)
        ax_w.set_title("Cuaca cerah mendominasi volume penyewaan", loc='left')
        ax_w.set_xlabel("Kondisi cuaca")
        ax_w.set_ylabel("Rata-rata sewa per hari")
        ax_w.yaxis.set_major_formatter(formatter_y)
        ax_w.tick_params(axis='x', rotation=10)
        for p in ax_w.patches:
            val = p.get_height()
            if not np.isnan(val) and val > 0:
                ax_w.annotate(format_id(val, 0), (p.get_x() + p.get_width() / 2., val),
                              ha='center', va='bottom', xytext=(0, 3), textcoords='offset points', fontsize=7.5)
        ax_w.grid(axis='y')
        st.pyplot(fig_w)
        plt.close(fig_w)

    # Dynamic Insight Calculation
    tot_2011 = filtered_day[filtered_day['year_label'] == 2011]['cnt'].sum()
    tot_2012 = filtered_day[filtered_day['year_label'] == 2012]['cnt'].sum()
    yoy_text = ""
    if tot_2011 > 0 and tot_2012 > 0:
        growth_rate = ((tot_2012 - tot_2011) / tot_2011) * 100
        sign = "+" if growth_rate > 0 else ""
        yoy_text = f"Total penyewaan meningkat dari {format_id(tot_2011)} pada 2011 menjadi {format_id(tot_2012)} pada 2012 ({sign}{format_id(growth_rate, 1)}%)."
    elif tot_2012 > 0:
        yoy_text = f"Total penyewaan tahun 2012 tercatat sebanyak {format_id(tot_2012)}."
    elif tot_2011 > 0:
        yoy_text = f"Total penyewaan tahun 2011 tercatat sebanyak {format_id(tot_2011)}."

    top_s_name = season_agg.iloc[0]['season_label'] if not season_agg.empty else "-"
    top_s_val = season_agg.iloc[0]['avg'] if not season_agg.empty else 0
    low_s_name = season_agg.iloc[-1]['season_label'] if not season_agg.empty else "-"
    low_s_val = season_agg.iloc[-1]['avg'] if not season_agg.empty else 0

    clear_val = weather_agg[weather_agg['weather_label'] == 'Clear/Partly Cloudy']['avg'].values
    rain_val = weather_agg[weather_agg['weather_label'] == 'Light Snow/Rain']['avg'].values
    weather_text = ""
    if len(clear_val) > 0 and len(rain_val) > 0:
        diff_pct = ((clear_val[0] - rain_val[0]) / clear_val[0]) * 100
        weather_text = f"Rata-rata sewa saat cuaca cerah mencapai {format_id(clear_val[0], 0)} per hari, lalu turun menjadi {format_id(rain_val[0], 0)} per hari saat hujan atau salju ({format_id(diff_pct, 1)}% lebih rendah)."

    st.markdown(f"""
    <div class="insight-paragraph">
        <strong>Temuan utama:</strong><br>
        1. {yoy_text}<br>
        2. Musim dengan rata-rata sewa tertinggi adalah {top_s_name} ({format_id(top_s_val, 0)} sewa/hari), sedangkan terendah adalah {low_s_name} ({format_id(low_s_val, 0)} sewa/hari).<br>
        3. {weather_text}
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 2: Komuter dan rekreasi
# ---------------------------------------------------------
with tab2:
    apply_plot_style()

    col_hourly, col_ratio = st.columns([2.4, 1.0])

    work_hr = filtered_hour[filtered_hour['workingday_label'] == 'Workingday'].groupby('hr')[['casual', 'registered']].mean().reset_index()
    rest_hr = filtered_hour[filtered_hour['workingday_label'] == 'Weekend/Holiday'].groupby('hr')[['casual', 'registered']].mean().reset_index()

    with col_hourly:
        fig_h, ax_h = plt.subplots(figsize=(8.5, 3.8))
        if not work_hr.empty:
            ax_h.plot(work_hr['hr'], work_hr['registered'], color='#1d4ed8', linewidth=2.0, label='Terdaftar (hari kerja)')
            ax_h.plot(work_hr['hr'], work_hr['casual'], color='#1d4ed8', linewidth=1.2, linestyle='--', label='Kasual (hari kerja)')
        if not rest_hr.empty:
            ax_h.plot(rest_hr['hr'], rest_hr['registered'], color='#94a3b8', linewidth=1.8, label='Terdaftar (akhir pekan/libur)')
            ax_h.plot(rest_hr['hr'], rest_hr['casual'], color='#94a3b8', linewidth=1.2, linestyle='--', label='Kasual (akhir pekan/libur)')

        ax_h.set_title("Pengguna terdaftar memiliki dua puncak jam komuter di hari kerja", loc='left')
        ax_h.set_xlabel("Jam (0-23)")
        ax_h.set_ylabel("Rata-rata sewa per jam")
        ax_h.set_xticks(range(0, 24, 2))
        ax_h.yaxis.set_major_formatter(formatter_y)
        ax_h.legend(frameon=False)
        ax_h.grid(axis='y')
        st.pyplot(fig_h)
        plt.close(fig_h)

    with col_ratio:
        fig_prop, ax_prop = plt.subplots(figsize=(3.5, 3.8))
        categories = ['Terdaftar', 'Kasual']
        shares = [pct_reg, pct_cas]
        colors = ['#1d4ed8', '#cbd5e1']

        bars = ax_prop.bar(categories, shares, color=colors, width=0.55)
        ax_prop.set_title("Proporsi pengguna", loc='left')
        ax_prop.set_ylabel("Persentase (%)")
        ax_prop.set_ylim(0, 100)
        ax_prop.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f"{int(round(x))}%"))
        for b in bars:
            h = b.get_height()
            ax_prop.annotate(f"{format_id(h, 1)}%", (b.get_x() + b.get_width() / 2., h),
                             ha='center', va='bottom', xytext=(0, 3), textcoords='offset points', fontsize=8.0)
        ax_prop.grid(axis='y')
        st.pyplot(fig_prop)
        plt.close(fig_prop)

    # Dynamic Insight Calculation for Tab 2
    peak_morn_val = work_hr[work_hr['hr'] == 8]['registered'].values[0] if (not work_hr.empty and 8 in work_hr['hr'].values) else 0
    peak_eve_val = work_hr[work_hr['hr'] == 17]['registered'].values[0] if (not work_hr.empty and 17 in work_hr['hr'].values) else 0
    wknd_afternoon_val = rest_hr[(rest_hr['hr'] >= 12) & (rest_hr['hr'] <= 16)]['casual'].mean() if not rest_hr.empty else 0

    st.markdown(f"""
    <div class="insight-paragraph">
        <strong>Temuan utama:</strong><br>
        1. Pada hari kerja, aktivitas pengguna terdaftar terpusat pada jam berangkat kerja pukul 08:00 ({format_id(peak_morn_val, 0)} sewa/jam) dan jam pulang kerja pukul 17:00 ({format_id(peak_eve_val, 0)} sewa/jam).<br>
        2. Pada akhir pekan dan hari libur, pengguna kasual mendominasi siang hari antara pukul 12:00 hingga 16:00 dengan rata-rata {format_id(wknd_afternoon_val, 0)} sewa per jam.<br>
        3. Secara total dalam filter terpilih, {format_id(pct_reg, 1)}% sewa berasal dari pengguna terdaftar dan {format_id(pct_cas, 1)}% dari pengguna kasual.
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 3: Analisis lanjutan
# ---------------------------------------------------------
with tab3:
    apply_plot_style()
    st.caption("Metode segmentasi data: pengelompokan manual 24 jam ke dalam lima periode hari, serta binning interval untuk temperatur dan kelembapan udara.")

    col_pod, col_matrix = st.columns([1.1, 1.3])

    with col_pod:
        pod_agg = filtered_hour.groupby('part_of_day').agg(avg=('cnt', 'mean')).reset_index()
        pod_order = ['Sore Sibuk (16-20)', 'Jam Kerja/Siang (10-16)', 'Pagi Sibuk (06-10)', 'Malam (20-24)', 'Dini Hari (00-06)']
        pod_order = [p for p in pod_order if p in pod_agg['part_of_day'].values]
        pod_agg = pod_agg.set_index('part_of_day').reindex(pod_order).reset_index()

        top_pod = pod_agg.iloc[0]['part_of_day'] if not pod_agg.empty else ""
        palette_pod = {p: ('#1d4ed8' if p == top_pod else '#cbd5e1') for p in pod_order}

        fig_pod, ax_pod = plt.subplots(figsize=(5.5, 3.6))
        sns.barplot(data=pod_agg, x='part_of_day', y='avg', hue='part_of_day', palette=palette_pod, legend=False, ax=ax_pod)
        ax_pod.set_title("Sore hari mencatat rata-rata sewa per jam tertinggi", loc='left')
        ax_pod.set_xlabel("Segmen hari")
        ax_pod.set_ylabel("Rata-rata sewa per jam")
        ax_pod.yaxis.set_major_formatter(formatter_y)
        ax_pod.tick_params(axis='x', rotation=15)
        for p in ax_pod.patches:
            val = p.get_height()
            if not np.isnan(val) and val > 0:
                ax_pod.annotate(format_id(val, 1), (p.get_x() + p.get_width() / 2., val),
                                ha='center', va='bottom', xytext=(0, 3), textcoords='offset points', fontsize=7.5)
        ax_pod.grid(axis='y')
        st.pyplot(fig_pod)
        plt.close(fig_pod)

    with col_matrix:
        pivot_data = filtered_day.pivot_table(index='temp_category', columns='hum_category', values='cnt', aggfunc='mean')
        
        temp_order = [t for t in ['Panas (>28°C)', 'Hangat/Ideal (20-28°C)', 'Sejuk (10-20°C)', 'Dingin (<10°C)'] if t in pivot_data.index]
        hum_order = [h for h in ['Kering (<45%)', 'Ideal (45-70%)', 'Lembap/Basah (>70%)'] if h in pivot_data.columns]
        pivot_data = pivot_data.reindex(index=temp_order, columns=hum_order)

        # Formatted annotations for heatmap
        annot_matrix = pivot_data.map(lambda v: format_id(v, 0) if pd.notna(v) else "")

        fig_heat, ax_heat = plt.subplots(figsize=(6.2, 3.6))
        sns.heatmap(pivot_data, annot=annot_matrix, fmt='', cmap='Blues', cbar=False, ax=ax_heat)
        ax_heat.set_title("Interaksi suhu dan kelembapan terhadap sewa harian", loc='left')
        ax_heat.set_xlabel("Kategori kelembapan")
        ax_heat.set_ylabel("Kategori suhu")
        st.pyplot(fig_heat)
        plt.close(fig_heat)

    # Dynamic calculations for Tab 3
    eve_avg = pod_agg[pod_agg['part_of_day'].str.contains('Sore')]['avg'].values[0] if any(pod_agg['part_of_day'].str.contains('Sore')) else 0
    night_avg = pod_agg[pod_agg['part_of_day'].str.contains('Dini')]['avg'].values[0] if any(pod_agg['part_of_day'].str.contains('Dini')) else 0

    st.markdown(f"""
    <div class="insight-paragraph">
        <strong>Temuan utama:</strong><br>
        1. Segmen sore hari (16:00-20:00) memiliki intensitas tertinggi dengan rata-rata {format_id(eve_avg, 1)} sewa per jam.<br>
        2. Segmen dini hari (00:00-06:00) memiliki aktivitas terendah ({format_id(night_avg, 1)} sewa per jam), sesuai untuk periode pemeliharaan unit sepeda dan stasiun.<br>
        3. Suhu hangat (20-28 derajat Celsius) dengan kelembapan ideal (45-70%) menghasilkan tingkat sewa harian tertinggi.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Rekomendasi tindakan</div>', unsafe_allow_html=True)
    
    recommendations_data = pd.DataFrame({
        "Rencana aksi": [
            "Redistribusi armada sepeda terfokus pada jam komuter",
            "Peningkatan kapasitas di stasiun wisata pada akhir pekan",
            "Penjadwalan perawatan berkala saat musim dingin",
            "Penyesuaian operasional saat cuaca buruk"
        ],
        "Dasar data": [
            "Penyewaan hari kerja terkonsentrasi pada pukul 08:00 dan 17:00-18:00.",
            "Pengguna kasual aktif di siang hari antara pukul 12:00 dan 16:00.",
            "Rata-rata sewa musim dingin dan semi berada pada titik terendah tahunan.",
            "Kondisi hujan atau salju menurunkan rata-rata sewa harian lebih dari 60%."
        ]
    })
    st.table(recommendations_data)

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.divider()
st.caption("Capital Bikeshare Analytics | Analis: M Fikkan El Haq (DS284B6Y0938) | Dicoding Indonesia 2026")
