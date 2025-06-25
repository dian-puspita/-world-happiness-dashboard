# 🌍 World Happiness Dashboard (2015–2019)

Dashboard interaktif berbasis **Streamlit** untuk mengeksplorasi laporan kebahagiaan dunia tahun 2015–2019 dari World Happiness Report.  
Proyek ini menyajikan berbagai visualisasi data untuk membantu pengguna memahami tren kebahagiaan global, negara-negara paling bahagia, serta faktor-faktor yang membentuk skor kebahagiaan suatu negara.

> ✨ Dibuat oleh: **Delastrada Dian Puspita**

---

## 📊 Fitur Visualisasi

1. **🏆 Negara Paling Bahagia Tiap Tahun**  
   Top 5 negara paling bahagia berdasarkan skor tahunan.

2. **📈 Rata-Rata Skor Kebahagiaan Dunia**  
   Tren rata-rata skor kebahagiaan dunia dari tahun ke tahun.

3. **🌐 Distribusi Skor Dunia**  
   Histogram persebaran skor kebahagiaan semua negara di suatu tahun.

4. **🧩 Komposisi Faktor Penyumbang Skor**  
   Proporsi rata-rata kontribusi faktor penyusun skor kebahagiaan secara global.

5. **📊 Tren Skor Negara Tertentu**  
   Perjalanan skor kebahagiaan sebuah negara dari tahun ke tahun.

6. **🧮 Proporsi Skor Tiap Negara**  
   Pie chart kontribusi tiap faktor (ekonomi, kesehatan, kebebasan, dll) terhadap skor negara tertentu di tahun tertentu.

---

## 🗂️ Struktur File

```
world_happiness_project/
│
├── dashboard.py                # File utama Streamlit
├── world_happiness_clean.csv  # Dataset kebahagiaan dunia 2015–2019
└── README.md                   # Dokumentasi proyek ini
```

---

## ▶️ Cara Menjalankan

1. **Clone Repository:**
```bash
git clone https://github.com/username/world_happiness_project.git
cd world_happiness_project
```

2. **Install Dependensi:**
```bash
pip install streamlit pandas matplotlib seaborn numpy
```

3. **Jalankan Aplikasi:**
```bash
streamlit run dashboard.py
```

---

## 🧠 Dataset

Data diambil dari **World Happiness Report** tahun 2015–2019 dan telah dibersihkan untuk keperluan eksplorasi.  
Dataset ini mencakup variabel seperti:

- Skor kebahagiaan
- GDP per capita
- Dukungan sosial
- Harapan hidup sehat
- Kebebasan memilih
- Kedermawanan
- Persepsi terhadap korupsi

---

## 🌍 World Happiness Dashboard

Dashboard interaktif untuk mengeksplorasi World Happiness Report 2015–2019.

🚀 Coba aplikasinya: [Klik di sini](https://dian-puspita-happiness-viz.streamlit.app)

### 📊 Fitur Visualisasi:
- Negara paling bahagia tiap tahun
- Rata-rata skor global
- Distribusi skor
- Komposisi faktor skor
- Tren skor per negara
- Proporsi skor tiap negara

## 📄 Lisensi

Proyek ini bebas digunakan untuk keperluan edukasi dan non-komersial.  
Silakan beri atribusi jika ingin memodifikasi atau mendistribusikan ulang.

---

## 🙌 Terima Kasih

Terima kasih kepada World Happiness Report dan komunitas open source atas data dan inspirasi.

---

Made with ❤️ by Delastrada Dian Puspita
