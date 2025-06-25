import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import squarify
import numpy as np

st.set_page_config(page_title="World Happiness Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("world_happiness_clean.csv")

df = load_data()

# Judul Dashboard
st.title("🌍 World Happiness Dashboard (2015 - 2019)")
st.markdown("""
Dashboard interaktif untuk mengeksplorasi World Happiness Report 2015–2019.   
Visualisasi oleh: **Delastrada Dian Puspita**
""")

# Sidebar Navigasi
st.sidebar.title("🔍 Navigasi")
menu = st.sidebar.radio("Pilih Visualisasi", [
    "Negara Paling Bahagia Tiap Tahun",
    "Rata-Rata Skor per Tahun",
    "Distribusi Skor Kebahagiaan Dunia",
    "Komposisi Faktor Penyumbang Skor",
    "Tren Skor Negara Tertentu",
    "Proporsi Skor Tiap Negara"
])

# Filter global
years = sorted(df['Year'].unique())
countries = sorted(df['Country'].unique())

if menu in ["Negara Paling Bahagia Tiap Tahun", "Rata-Rata Skor per Tahun", "Distribusi Skor Kebahagiaan Dunia", "Komposisi Faktor Penyumbang Skor"]:
    year_selected = st.sidebar.selectbox("Pilih Tahun", years)
elif menu in ["Tren Skor Negara Tertentu", "Proporsi Skor Tiap Negara"]:
    year_selected = st.sidebar.selectbox("Pilih Tahun", years)
    country_selected = st.sidebar.selectbox("Pilih Negara", countries)

# Ukuran visualisasi default
figsize_line = (7, 4)
figsize_pie = (6, 6)
figsize_bar = (8, 5)

# Visualisasi 1: 5 Negara Paling Bahagia Tiap Tahun
if menu == "Negara Paling Bahagia Tiap Tahun":
    st.header(f"🏆 Top 5 Negara Paling Bahagia - Tahun {year_selected}")
    st.caption("Mengidentifikasi negara-negara dengan tingkat kebahagiaan tertinggi pada tahun tertentu. Visualisasi ini memberi gambaran negara mana yang secara konsisten unggul dalam kebahagiaan global, sekaligus memungkinkan perbandingan cepat antar negara teratas.")

    top5 = df[df["Year"] == year_selected].sort_values("Happiness Score", ascending=False).head(5)

    # Lollipop Chart
    fig, ax = plt.subplots(figsize=figsize_bar)
    ax.hlines(y=top5["Country"], xmin=0, xmax=top5["Happiness Score"], color='skyblue', linewidth=3)
    ax.plot(top5["Happiness Score"], top5["Country"], "o", markersize=8, color='blue', alpha=0.8)
    ax.set_xlabel("Skor Kebahagiaan")
    ax.set_title("Top 5 Negara Paling Bahagia (Lollipop Chart Style)")
    ax.grid(True, axis='x', linestyle='--', alpha=0.5)
    st.pyplot(fig)

# Visualisasi 2: Rata-Rata Skor Kebahagiaan Dunia per Tahun
elif menu == "Rata-Rata Skor per Tahun":
    st.header("📈 Rata-Rata Skor Kebahagiaan Dunia per Tahun")
    st.caption("Menampilkan tren rata-rata kebahagiaan global dari tahun ke tahun. Dari visualisasi ini, kita bisa melihat apakah secara global dunia menjadi lebih bahagia atau justru mengalami penurunan kesejahteraan subjektif selama periode 2015–2019.")

    avg_score = df.groupby("Year")["Happiness Score"].mean().reset_index()
    fig, ax = plt.subplots(figsize=figsize_line)
    sns.lineplot(data=avg_score, x="Year", y="Happiness Score", marker="o", ax=ax)
    ax.axvline(year_selected, color="red", linestyle="--", label="Tahun Dipilih")
    ax.set_ylabel("Rata-rata Skor")
    ax.legend()
    st.pyplot(fig)

# Visualisasi 3: Distribusi Skor Kebahagiaan Dunia per Tahun
elif menu == "Distribusi Skor Kebahagiaan Dunia":
    st.header("🌐 Distribusi Skor Kebahagiaan Dunia per Tahun")
    st.caption("Memahami sebaran tingkat kebahagiaan antar negara di dunia pada tahun tertentu. Distribusi ini menunjukkan apakah kebahagiaan terpusat di negara-negara tertentu atau tersebar merata, serta mengungkap adanya negara-negara dengan skor sangat rendah atau sangat tinggi.")

    yearly_data = df[df['Year'] == year_selected]
    fig, ax = plt.subplots(figsize=figsize_bar)
    sns.histplot(yearly_data["Happiness Score"], bins=20, kde=True, color="skyblue", ax=ax)
    ax.set_title(f"Distribusi Skor Kebahagiaan Dunia - Tahun {year_selected}")
    st.pyplot(fig)

# Visualisasi 4: Komposisi Faktor Penyumbang Skor
elif menu == "Komposisi Faktor Penyumbang Skor":
    st.header("🧩 Komposisi Faktor Penyumbang Skor")
    st.caption("Menunjukkan proporsi rata-rata dari faktor-faktor pembentuk skor kebahagiaan di dunia untuk tahun tertentu. Dari sini kita dapat mengamati faktor mana yang paling berpengaruh terhadap kebahagiaan secara global, seperti apakah dukungan sosial lebih berpengaruh daripada pendapatan atau kebebasan.")

    factor_cols = [
        'GDP per capita', 'Social support', 'Healthy life expectancy',
        'Freedom to make life choices', 'Generosity', 'Perceptions of corruption', 'Dystopia Residual'
    ]
    avg_factors = df[df['Year'] == year_selected][factor_cols].mean().dropna()
    fig, ax = plt.subplots(figsize=figsize_pie)
    colors = sns.color_palette('pastel')
    ax.pie(avg_factors, labels=avg_factors.index, colors=colors, autopct='%1.1f%%', startangle=140, wedgeprops={'width':0.4})
    ax.set_title(f"Komposisi Faktor Skor Kebahagiaan Tahun {year_selected}")
    st.pyplot(fig)

# Visualisasi 5: Tren Skor Negara Tertentu
elif menu == "Tren Skor Negara Tertentu":
    st.header(f"📊 Tren Skor Kebahagiaan - {country_selected}")
    st.caption("Melacak perubahan tingkat kebahagiaan suatu negara dari tahun ke tahun. Visualisasi ini memberikan wawasan apakah kebijakan dan kondisi sosial-ekonomi di negara tersebut berdampak positif atau negatif terhadap persepsi kesejahteraan masyarakatnya.")

    trend = df[df['Country'] == country_selected]
    fig, ax = plt.subplots(figsize=figsize_line)
    sns.lineplot(data=trend, x="Year", y="Happiness Score", marker="o", color="green", linewidth=2, ax=ax)
    ax.axvline(year_selected, color="red", linestyle="--")
    ax.set_title(f"Tren Skor Kebahagiaan - {country_selected}")
    st.pyplot(fig)


# Visualisasi 6: Proporsi Skor Tiap Negara
elif menu == "Proporsi Skor Tiap Negara":
    st.header(f"🧮 Proporsi Faktor Pembentuk Skor - {country_selected} ({year_selected})")
    st.caption("Melihat kontribusi tiap faktor terhadap skor kebahagiaan di negara tertentu pada tahun tertentu. Ini membantu memahami kekuatan dan kelemahan negara dalam aspek-aspek penentu kebahagiaan, seperti apakah kebahagiaan masyarakat lebih ditopang oleh ekonomi, dukungan sosial, atau faktor lain.")

    selected_row = df[(df['Country'] == country_selected) & (df['Year'] == year_selected)]
    
    if not selected_row.empty:
        row = selected_row.iloc[0]
        labels = [
            "GDP", "Social Support", "Healthy Life", "Freedom", "Generosity", "Corruption", "Dystopia Residual"
        ]
        values = [
            row.get("GDP per capita", 0) or 0,
            row.get("Social support", 0) or 0,
            row.get("Healthy life expectancy", 0) or 0,
            row.get("Freedom to make life choices", 0) or 0,
            row.get("Generosity", 0) or 0,
            row.get("Perceptions of corruption", 0) or 0,
            row.get("Dystopia Residual", 0) or 0
        ]
        values = [v if not pd.isna(v) else 0 for v in values]

        fig, ax = plt.subplots(figsize=(7, 5))  # Ukuran konsisten

        colors = sns.color_palette("Set2")
        wedges, texts, autotexts = ax.pie(
            values,
            labels=None,  # Jangan tampilkan label langsung
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            textprops={'color': "white", 'weight': 'bold'},
            wedgeprops={'linewidth': 1, 'edgecolor': 'white'}
        )

        ax.axis("equal")
        ax.set_title(f"Proporsi Faktor - {country_selected} ({year_selected})", fontsize=14)

        # Tambahkan legenda rapi di samping
        ax.legend(
            wedges, labels, title="Faktor", loc="center left",
            bbox_to_anchor=(1, 0.5), fontsize='small', title_fontsize='small'
        )

        fig.tight_layout()
        st.pyplot(fig)

    else:
        st.warning("Data tidak tersedia untuk kombinasi tahun dan negara ini.")

# Footer
st.markdown("""
    <hr style="border:1px solid #eee;">
    <p style='text-align: center; font-size: 12px; color: gray;'>
    Made with ❤️ by Delastrada Dian Puspita | Data: World Happiness Report
    </p>
""", unsafe_allow_html=True)
