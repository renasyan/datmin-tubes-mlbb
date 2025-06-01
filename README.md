# Hero Counter Recommendation for Mobile Legends: Bang Bang

## Deskripsi Proyek
Sistem ini merekomendasikan tiga hero terbaik sebagai counter berdasarkan tiga hero musuh.  
- **Data**: History match MLBB (komposisi hero, hasil, durasi, kills, dsb).  
- **Metode**:  
  1. **Praproses & Encoding**:  
     - Parse `left_heroes`/`right_heroes` dari string ke list.  
     - Buat duplikat setiap match (flip kiri↔kanan, balik hasil).  
     - One-hot encode setiap hero dengan prefix `L_`/`R_`.  
  2. **Model Supervised (Logistic Regression)**  
     - Fit untuk memprediksi `match_result` (1 = tim kiri menang).  
     - Evaluasi:  
       - Akurasi data uji: 65,67 %  
       - ROC AUC: 71,57 %  
       - Cross-val 5-fold: 61,49 %  
       - Confusion matrix menunjukkan keseimbangan prediksi menang/kalah.  
  3. **Apriori Hybrid (Rule Mining + Label)**  
     - Transformasi transaksi: `L_<hero>`, `R_<hero>`, `WIN_L`/`WIN_R`.  
     - Generate aturan “{R_X, L_Y} ⇒ WIN_L” untuk menemukan hero counter statis.  
  4. **Sistem Rekomendasi**  
     - Input: daftar 3 hero musuh.  
     - Generate semua kombinasi 3 hero tim sendiri, prediksi probabilitas menang, dan pilih top 3.  
  5. **Dashboard UI (React + Tailwind)**  
     - Tampilkan metrik model (akurasi, ROC AUC, cross-val).  
     - Form input 3 hero musuh → hasil rekomendasi 3 hero counter.

---

## Anggota Tim
– Aimee Clarissa Adyanugraha Salim
- Miftha Huljannah Sarvita Yusuf  
– Renasya Cahya Handayani

---

## Cara Menjalankan di Lokal

1. **Clone Repo**  
   ```bash
   git clone https://github.com/username/repo-hero-counter.git](https://github.com/renasyan/datmin-tubes-mlbb)
   cd datmin-tubes-mlbb
   
npm install
npm start

Buka http://localhost:3000

Masukkan 3 hero musuh → klik “Rekomendasikan Hero” → lihat hasil.
