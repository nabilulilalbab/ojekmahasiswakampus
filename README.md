---

# Ojek Mahasiswa Kampus

**Ojek Mahasiswa Kampus** adalah aplikasi berbasis web yang dirancang untuk memudahkan mahasiswa dalam melakukan pemesanan layanan antar jemput di sekitar kampus dengan harga terjangkau. Aplikasi ini memanfaatkan teknologi Django untuk pengelolaan order, validasi voucher diskon, serta pengecekan harga perjalanan secara real-time.

## Fitur Utama

- **Pemesanan Layanan Antar Jemput**
  - Mahasiswa dapat memesan layanan antar jemput dengan mudah melalui formulir pemesanan.
  - Integrasi dengan sistem voucher diskon untuk mendapatkan potongan harga.
- **Manajemen Event & Voucher**
  - Sistem event aktif yang memungkinkan penggunaan voucher diskon khusus selama periode tertentu.
  - Validasi dan penggunaan voucher yang terintegrasi langsung pada proses pemesanan.
- **User Experience yang Optimal**
  - Tampilan antarmuka yang responsif dan mudah digunakan.
  - Informasi lengkap mengenai kelebihan layanan seperti tarif terjangkau, privasi terjamin, kecepatan, dan ketersediaan voucher diskon.

## Teknologi yang Digunakan

- **Backend:** Django, Django REST Framework (jika diperlukan)
- **Frontend:** HTML, CSS, JavaScript (AJAX untuk pengecekan harga dan validasi voucher)
- **Database:** SQLite (default) atau PostgreSQL/MySQL sesuai kebutuhan deployment

## Instalasi

1. **Clone Repository**

   ```bash
   git clone https://github.com/nabilulilalbab/ojekmahasiswakampus.git
   cd ojekmahasiswakampus
   ```

2. **Buat Virtual Environment dan Install Dependencies**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Untuk Linux/Mac
   # atau
   venv\Scripts\activate  # Untuk Windows

   pip install -r requirements.txt
   ```

3. **Konfigurasi Environment Variables**

   Buat file `.env` atau atur variabel di `settings.py`:

   ```env
   SECRET_KEY='your_secret_key'
   ```

4. **Migrasi Database**

   ```bash
   python manage.py migrate
   ```

5. **Jalankan Server**

   ```bash
   python manage.py runserver
   ```

   Akses aplikasi melalui `http://127.0.0.1:8000/`

## Struktur Proyek

```
ojekmahasiswakampus/
├── omk/
│   ├── migrations/
│   ├── templates/
│   │   ├── omk/
│   │   │   ├── home.html
│   │   │   ├── order_form.html
│   │   │   └── order_success.html
│   ├── views.py
│   ├── models.py
│   ├── forms.py
│   └── urls.py
├── manage.py
└── requirements.txt
```

## Kontribusi

Kontribusi sangat diterima! Silakan fork repository ini, buat branch fitur/bugfix, dan ajukan pull request. Pastikan untuk mengikuti standar coding yang ada.

**Kontributor:**  
- [nabilulilalbab](https://github.com/nabilulilalbab)  
- [bimadevs](https://github.com/bimadevs)  

## Lisensi

Project ini dilisensikan di bawah [MIT License](LICENSE).

## Kontak

Untuk pertanyaan lebih lanjut, silakan hubungi [nabilulilalbab](https://github.com/nabilulilalbab).

---
