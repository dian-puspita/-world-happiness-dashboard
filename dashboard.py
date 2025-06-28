import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import altair as alt

st.set_page_config(page_title="World Happiness Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("world_happiness_clean.csv")

df = load_data()

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

# Filter tahun dan negara, tapi sesuaikan agar dropdown tahun tidak muncul untuk "Rata-Rata Skor per Tahun"
years = sorted(df['Year'].unique())
countries = sorted(df['Country'].unique())

# Tahun hanya untuk menu yang butuh filter tahun, kecuali "Rata-Rata Skor per Tahun"
if menu in [
    "Negara Paling Bahagia Tiap Tahun",
    "Distribusi Skor Kebahagiaan Dunia",
    "Komposisi Faktor Penyumbang Skor",
    "Proporsi Skor Tiap Negara"
]:
    year_selected = st.sidebar.selectbox("Pilih Tahun", years)
else:
    year_selected = None  # Tidak perlu filter tahun

# Negara hanya untuk menu yang pakai filter negara
if menu in [
    "Tren Skor Negara Tertentu",
    "Proporsi Skor Tiap Negara"
]:
    country_selected = st.sidebar.selectbox("Pilih Negara", countries)
else:
    country_selected = None

# Judul halaman
st.title("🌍 World Happiness Dashboard (2015 - 2019)")
st.markdown("""
Dashboard interaktif untuk mengeksplorasi World Happiness Report 2015–2019.  
Visualisasi oleh: **Delastrada Dian Puspita**
""")

figsize_line = (7, 4)
figsize_pie = (6, 6)
figsize_bar = (8, 5)

# Visualisasi 1
if menu == "Negara Paling Bahagia Tiap Tahun":
    st.header(f"🏆 Top 5 Negara Paling Bahagia - Tahun {year_selected}")
    top5 = df[df["Year"] == year_selected].sort_values("Happiness Score", ascending=False).head(5)

    fig, ax = plt.subplots(figsize=figsize_bar)
    ax.hlines(y=top5["Country"], xmin=0, xmax=top5["Happiness Score"], color='skyblue', linewidth=3)
    ax.plot(top5["Happiness Score"], top5["Country"], "o", markersize=8, color='blue', alpha=0.8)
    ax.set_xlabel("Skor Kebahagiaan")
    ax.set_title("Top 5 Negara Paling Bahagia (Lollipop Chart)")
    ax.grid(True, axis='x', linestyle='--', alpha=0.5)
    st.pyplot(fig)

# Visualisasi 2 (tidak pakai filter tahun)
elif menu == "Rata-Rata Skor per Tahun":
    st.header("📊 Rata-Rata Skor Kebahagiaan Dunia per Tahun")
    st.caption("Visualisasi interaktif menggunakan Altair. Gerakkan mouse untuk melihat detail skor.")

    avg_score = df.groupby("Year")["Happiness Score"].mean().reset_index()
    avg_score["Year"] = avg_score["Year"].astype(str)  # Altair butuh tipe string untuk ordinal axis

    chart = alt.Chart(avg_score).mark_circle(size=200).encode(
        x=alt.X("Year:O", title="Tahun"),
        y=alt.Y("Happiness Score:Q", title="Rata-Rata Skor"),
        size=alt.Size("Happiness Score:Q", scale=alt.Scale(range=[100, 1000]), legend=None),
        color=alt.Color("Happiness Score:Q", scale=alt.Scale(scheme="blues")),
        tooltip=[
            alt.Tooltip("Year:O", title="Tahun"),
            alt.Tooltip("Happiness Score:Q", title="Skor", format=".2f")
        ]
    ).properties(
        width=700,
        height=400,
        title="🔵 Rata-Rata Skor Kebahagiaan Dunia per Tahun"
    ).interactive()

    st.altair_chart(chart, use_container_width=True)

# Visualisasi 3
elif menu == "Distribusi Skor Kebahagiaan Dunia":
    st.header("🌐 Distribusi Skor Kebahagiaan Dunia per Tahun")
    st.caption("Distribusi skor kebahagiaan negara-negara di dunia untuk tahun tertentu. Violin plot menunjukkan sebaran, kepadatan, dan median skor kebahagiaan.")

    yearly_data = df[df["Year"] == year_selected]

    fig, ax = plt.subplots(figsize=(6, 5))
    sns.violinplot(data=yearly_data, y="Happiness Score", inner="quart", palette="pastel", ax=ax)
    ax.set_title(f"Distribusi Skor Kebahagiaan Dunia - Tahun {year_selected}", fontsize=12)
    ax.set_xlabel("")
    ax.set_ylabel("Skor Kebahagiaan")
    st.pyplot(fig)

# Visualisasi 4
# Visualisasi 4
elif menu == "Komposisi Faktor Penyumbang Skor":
    st.header("🧩 Komposisi Faktor Penyumbang Skor")
    st.caption("Menunjukkan proporsi rata-rata dari faktor-faktor pembentuk skor kebahagiaan di dunia untuk tahun tertentu.")

    factor_cols = [
        'GDP per capita', 'Social support', 'Healthy life expectancy',
        'Freedom to make life choices', 'Generosity', 'Perceptions of corruption', 'Dystopia Residual'
    ]
    avg_factors = df[df['Year'] == year_selected][factor_cols].mean().dropna()

    fig, ax = plt.subplots(figsize=(6, 5))  # Ukuran diperkecil agar tidak terlalu besar
    colors = sns.color_palette('pastel')

    def small_autopct(pct):
        return f'{pct:.1f}%' if pct > 3 else ''

    wedges, texts, autotexts = ax.pie(
        avg_factors,
        labels=None,
        autopct=small_autopct,
        startangle=140,
        colors=colors,
        wedgeprops={'width': 0.5, 'edgecolor': 'white'},
        textprops={'fontsize': 9, 'color': "white"}
    )

    ax.set_title(f"Komposisi Faktor Skor Kebahagiaan Tahun {year_selected}", fontsize=14, pad=5)
    ax.axis("equal")
    ax.legend(
        wedges,
        avg_factors.index,
        title="Faktor",
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        fontsize='small',
        title_fontsize='small'
    )

    fig.subplots_adjust(top=0.85)  # Jarak atas (judul) lebih dekat ke chart
    st.pyplot(fig)

# Visualisasi 5
elif menu == "Tren Skor Negara Tertentu":
    st.header(f"📊 Tren Skor Kebahagiaan - {country_selected}")
    trend = df[df['Country'] == country_selected]
    chart = alt.Chart(trend).mark_line(point=alt.OverlayMarkDef(color="green")).encode(
        x=alt.X("Year:O", title="Tahun"),
        y=alt.Y("Happiness Score:Q", title="Skor Kebahagiaan"),
        tooltip=["Year", "Happiness Score"]
    ).properties(width=600, height=400).interactive()
    st.altair_chart(chart)

# Visualisasi 6
elif menu == "Proporsi Skor Tiap Negara":
    st.header(f"🧮 Proporsi Faktor Pembentuk Skor - {country_selected} ({year_selected})")
    selected_row = df[(df['Country'] == country_selected) & (df['Year'] == year_selected)]

    if not selected_row.empty:
        row = selected_row.iloc[0]
        labels = [
            "GDP", "Social Support", "Healthy Life", "Freedom", "Generosity", "Corruption", "Dystopia Residual"
        ]
        values = [
            row.get("GDP per capita", 0),
            row.get("Social support", 0),
            row.get("Healthy life expectancy", 0),
            row.get("Freedom to make life choices", 0),
            row.get("Generosity", 0),
            row.get("Perceptions of corruption", 0),
            row.get("Dystopia Residual", 0)
        ]
        values = [v if pd.notna(v) else 0 for v in values]

        fig, ax = plt.subplots(figsize=(7, 5))
        wedges, texts, autotexts = ax.pie(
            values,
            labels=None,
            autopct='%1.1f%%',
            startangle=90,
            colors=sns.color_palette("Set2"),
            textprops={'color': "white", 'weight': 'bold'},
            wedgeprops={'linewidth': 1, 'edgecolor': 'white'}
        )
        ax.axis("equal")
        ax.set_title(f"Proporsi Faktor - {country_selected} ({year_selected})", fontsize=14)
        ax.legend(
            wedges, labels, title="Faktor", loc="center left",
            bbox_to_anchor=(1, 0.5), fontsize='small', title_fontsize='small'
        )
        fig.tight_layout()
        st.pyplot(fig)
    else:
        st.warning("Data tidak tersedia untuk kombinasi negara dan tahun ini.")

# Footer
st.markdown("""
<hr style="border:1px solid #eee;">
<p style='text-align: center; font-size: 12px; color: gray;'>
Made with ❤️ by Delastrada Dian Puspita | Data: World Happiness Report
</p>
""", unsafe_allow_html=True)
