# UAS_PBO
# Risky Kasir - Sistem Point of Sale (POS) Toko Kelontong

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green) ![SQLite](https://img.shields.io/badge/Database-SQLite3-lightgrey) ![Architecture](https://img.shields.io/badge/Architecture-Strict%20MVC-orange)

## Deskripsi Umum
**Risky Kasir** adalah aplikasi desktop fungsional tingkat menengah (*enterprise-grade prototype*) yang dirancang khusus untuk mempermudah manajemen operasional Toko Kelontong. Dibangun sepenuhnya menggunakan bahasa pemrograman Python, aplikasi ini menerapkan arsitektur **Strict Model-View-Controller (MVC)** secara disiplin. Pemisahan struktur kode antara logika bisnis, antarmuka pengguna, dan manajemen database memastikan kode sumber tetap bersih (*Clean Code*), modular, dan mudah dipelihara.

Aplikasi ini mendukung navigasi multi-halaman (*Single Page Application desktop*) menggunakan teknik *Frame Switching* yang mulus, serta terintegrasi langsung dengan database relasional SQLite lokal untuk persistensi data yang aman tanpa memerlukan instalasi *server* eksternal.

## Fitur Utama
Aplikasi memiliki sistem otentikasi pengguna berbasis peran (*Role-Based Access Control*) yang membagi akses untuk dua aktor utama: **Owner** (Pemilik) dan **Kasir** (Staf).

*   **Sistem Login & Kelola Akun (Owner):** Keamanan akses masuk dan pengelolaan CRUD (Create, Read, Update, Delete) data pengguna sistem.
*   **Manajemen Data Barang (Owner):** Pencatatan inventaris barang, penentuan harga, pengaturan kategori, dan peringatan visual otomatis untuk stok barang yang menipis (<= 5 unit).
*   **Transaksi Kasir (Kasir):** Antarmuka Point of Sale (POS) yang responsif dengan keranjang belanja interaktif, pencarian barang instan, dan kalkulasi total serta uang kembalian secara otomatis.
*   **Riwayat Penjualan (Owner & Kasir):** Tabel rekaman jejak seluruh *invoice* transaksi beserta rincian item yang dibeli pelanggan pada waktu tertentu.
*   **Laporan Toko (Owner):** Ringkasan metrik total pendapatan/omset dan kuantitas barang terjual yang dapat difilter secara dinamis berdasarkan rentang tanggal.

## Tangkapan Layar Antarmuka

### 1. Dashboard Utama (Tampilan Owner)
Menampilkan ringkasan data penting harian dan tabel peringatan untuk stok barang yang hampir habis.
![Dashboard Utama](Screenshot%202026-07-21%20225844.png)

### 2. Form Transaksi Kasir Baru
Sistem keranjang belanja untuk melayani transaksi pelanggan secara efisien.
![Transaksi Kasir](Screenshot%202026-07-21%20225904.png)

### 3. Riwayat Transaksi Penjualan
Rekapan bukti *invoice* transaksi yang telah berhasil diproses ke dalam database.
![Riwayat Penjualan](Screenshot%202026-07-21%20225952.png)

## Cara Menjalankan Aplikasi

### Persyaratan Sistem
*   Python versi 3.8 atau yang lebih baru.
*   Aplikasi ini murni menggunakan pustaka bawaan Python (*Standard Library*) seperti `tkinter`, `sqlite3`, `datetime`, dan `hashlib`. **Tidak diperlukan** instalasi pustaka pihak ketiga melalui `pip`.

### Langkah-langkah Eksekusi
1. Kloning repositori ini ke komputer lokal Anda:
   ```bash
   git clone https://github.com/username/risky-kasir.git
   ```
2. Buka terminal atau *command prompt*, lalu arahkan ke folder direktori proyek:
   ```bash
   cd risky-kasir
   ```
3. Jalankan *file* pengontrol utama untuk memulai aplikasi:
   ```bash
   python main.py
   ```
4. **Catatan Login Pertama:** Saat aplikasi pertama kali dijalankan, sistem akan otomatis menginisialisasi *file* database `kasir_risky.db` dan membuat dua akun *default* untuk keperluan pengujian:
   *   Akun Owner : Username: `admin` | Password: `admin`
   *   Akun Kasir : Username: `kasir` | Password: `kasir`

## Struktur Direktori & Arsitektur (Strict MVC)
*   **`model.py`** (Lapisan Data): Mengelola koneksi *database* SQLite, skema pembentukan tabel, validasi properti kelas dengan prinsip OOP (*Encapsulation*), dan logika kueri SQL.
*   **`view.py`** (Lapisan Antarmuka): Menyimpan seluruh susunan elemen UI/UX Tkinter (Ttk), gaya visual (*Themed*), tabel *Treeview*, dan navigasi pergeseran *Frame*. Tidak mengandung operasi *database* apa pun.
*   **`main.py`** (Lapisan Pengontrol): Menyatukan *Model* dan *View*. Bertindak sebagai pengatur (*router*) yang menangani *event handling* (klik tombol, *input* teks) dari *View* untuk memicu manipulasi data di *Model*.
