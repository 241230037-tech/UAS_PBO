# Risky Kasir - Sistem Point of Sale (POS) Toko Kelontong

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green) ![SQLite](https://img.shields.io/badge/Database-SQLite3-lightgrey) ![Architecture](https://img.shields.io/badge/Architecture-Strict%20MVC-orange)

## Deskripsi Utama
Risky Kasir adalah aplikasi Point of Sale (POS) berbasis desktop yang dirancang khusus untuk manajemen operasional Toko Kelontong. Aplikasi ini dibangun secara murni menggunakan bahasa pemrograman Python, dengan antarmuka grafis memanfaatkan pustaka bawaan Tkinter dan sistem penyimpanan persisten berbasis SQLite. 

Aplikasi ini mendemonstrasikan implementasi pola desain perangkat lunak Model-View-Controller (MVC) secara ketat (*Strict MVC*). Pemisahan ini membagi aplikasi menjadi Lapisan Data, Lapisan Antarmuka, dan Pengontrol, sehingga kode sumber terstruktur dengan rapi, modular, dan mematuhi prinsip kebersihan kode (*Clean Code*).

## Fitur-Fitur Sistem

*   **Otentikasi & Keamanan Berbasis Peran:** Sistem membagi akses menjadi dua tingkat otoritas pengguna, yaitu "Owner" dan "Kasir". Setiap kata sandi akun tidak disimpan dalam bentuk teks biasa, melainkan dienkripsi menggunakan metode *hashing* algoritma SHA-256.
*   **Dashboard Pantauan Cepat:** Laman awal menyajikan ringkasan metrik waktu nyata seperti total inventaris barang, jumlah transaksi, total pendapatan hari ini, serta peringatan tabel khusus bagi barang yang stoknya menipis (5 unit atau kurang).
*   **Manajemen Data Barang (Inventory):** Fasilitas kelola data penuh (CRUD) untuk mendaftarkan barang baru, menetapkan kategori, memperbarui harga jual, serta mengelola stok. Sistem juga akan membuat nomor ID Barang secara berurutan dan otomatis.
*   **Modul Kasir & Keranjang Belanja:** Antarmuka transaksional yang responsif di mana kasir dapat mencari produk, menambahkannya ke dalam keranjang, mengubah kuantitas beli, memvalidasi ketersediaan stok sebelum penyimpanan, dan menghitung nominal kembalian uang pelanggan.
*   **Riwayat Transaksi Penjualan:** Sistem mencatat setiap transaksi dalam bentuk arsip *invoice* utama yang merangkum total belanja, serta tabel detail rincian (*breakdown*) setiap barang yang dibeli di dalam *invoice* tersebut.
*   **Laporan Omset Berdasarkan Waktu:** Fitur penyaringan pelaporan yang memungkinkan pemilik toko untuk mengalkulasi total pendapatan uang dan unit kuantitas barang terjual dengan memasukkan rentang tanggal awal dan tanggal akhir.
*   **Manajemen Pengguna Terpusat:** Layar pengaturan khusus bagi peran "Owner" untuk mendaftarkan akun pegawai baru, mengatur hak akses sistem, serta mereset kata sandi pegawai lama.

## Tangkapan Layar Antarmuka

### 1. Dashboard Utama
Menampilkan ringkasan data penting harian dan tabel peringatan untuk stok barang yang hampir habis.
![Dashboard Utama](Screenshot%202026-07-21%20225844_2.png)

### 2. Form Transaksi Kasir Baru
Sistem keranjang belanja interaktif untuk melayani transaksi pelanggan secara efisien, dilengkapi dengan fitur pencarian barang dan kalkulasi subtotal.
![Transaksi Kasir](Screenshot%202026-07-21%20233827.png)

### 3. Riwayat Transaksi Penjualan
Rekapan bukti *invoice* transaksi yang telah berhasil diproses ke dalam basis data, menyajikan informasi detail kasir yang bertugas dan rincian item.
![Riwayat Penjualan](Screenshot%202026-07-21%20225952_2.png)

### 4. Laporan Penjualan Toko
Menyajikan ringkasan metrik total pendapatan/omset dan kuantitas barang terjual yang dapat disaring secara dinamis berdasarkan input rentang tanggal.
![Laporan Penjualan](Screenshot%202026-07-21%20233845.png)

### 5. Form Kelola Akun
Antarmuka khusus bagi pemilik toko (Owner) untuk menambahkan, memperbarui, atau menghapus data pengguna dan membatasi hak akses sistem.
![Kelola Akun](Screenshot%202026-07-21%20233925.png)

## Struktur Arsitektur (Strict MVC)

*   **`model.py` (Model):** Mengelola koneksi basis data lokal `kasir_risky.db` secara independen. Berisi definisi struktur tabel SQLite dan membungkus entitas sistem (seperti `User`, `Barang`, `Transaksi`) menjadi rancangan kelas berorientasi objek yang kuat dengan validasi enkapsulasi.
*   **`view.py` (View):** Bertindak murni sebagai wadah tata letak visual tanpa adanya operasi intervensi basis data apa pun. Laman ini menggunakan komponen `ttk` dari Tkinter beserta gaya tema "clam" untuk merancang desain aplikasi modern yang dilengkapi *Sidebar*, *Cards*, serta peralihan laman bertumpuk (*Frame Switching*).
*   **`main.py` (Controller):** Lapisan penjembatan utama yang menghubungkan tangkapan aksi (*event listener*) pada antarmuka Tkinter dengan perintah manipulasi manajer sistem di basis data.

## Panduan Penggunaan dan Pemasangan

1.  Pastikan lingkungan lokal Anda telah terinstal bahasa pemrograman Python versi 3.8 atau yang lebih baru. Tidak diperlukan instalasi *package* tambahan dari luar karena aplikasi dibangun menggunakan Pustaka Standar Python (*Standard Library*).
2.  Letakkan fail `main.py`, `model.py`, dan `view.py` ke dalam satu folder yang sama.
3.  Jalankan program melalui terminal atau *command prompt* dengan mengeksekusi pengontrol utama:
    ```bash
    python main.py
    ```
4.  Pada saat inisialisasi awal, sistem akan secara otomatis membentuk berkas basis data SQLite `kasir_risky.db` dan membuat dua akun percontohan bawaan. Silakan gunakan detail berikut untuk masuk ke dalam sistem:
    *   Akses Pemilik (Owner) : Username: `admin` | Password: `admin`
    *   Akses Pegawai (Kasir) : Username: `kasir` | Password: `kasir`
