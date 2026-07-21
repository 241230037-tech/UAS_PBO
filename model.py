import sqlite3
import hashlib
import os
from datetime import datetime

class DatabaseError(Exception):
    """Custom exception for database-related errors."""
    pass

class Database:
    """Manages the connection and standard query execution for SQLite."""
    def __init__(self, db_name="kasir_risky.db"):
        self.db_name = db_name
        self.init_db()

    def get_connection(self):
        """Returns a sqlite3 connection object."""
        try:
            conn = sqlite3.connect(self.db_name)
            conn.row_factory = sqlite3.Row  # Access columns by name
            conn.execute("PRAGMA foreign_keys = ON;")
            return conn
        except sqlite3.Error as e:
            raise DatabaseError(f"Gagal menghubungkan ke database: {e}")

    def init_db(self):
        """Creates the tables if they don't exist and seeds default users."""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # 1. User Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS User (
                    id_user INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    nama TEXT NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('Owner', 'Kasir'))
                );
            """)

            # 2. Barang Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Barang (
                    id_barang TEXT PRIMARY KEY,
                    nama_barang TEXT NOT NULL,
                    kategori TEXT NOT NULL,
                    harga REAL NOT NULL CHECK(harga >= 0),
                    stok INTEGER NOT NULL CHECK(stok >= 0)
                );
            """)

            # 3. Transaksi Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Transaksi (
                    id_transaksi TEXT PRIMARY KEY,
                    tanggal TEXT NOT NULL,
                    pelanggan TEXT NOT NULL,
                    kasir TEXT NOT NULL,
                    total REAL NOT NULL CHECK(total >= 0),
                    bayar REAL NOT NULL CHECK(bayar >= 0),
                    kembalian REAL NOT NULL CHECK(kembalian >= 0)
                );
            """)

            # 4. Detail_Transaksi Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Detail_Transaksi (
                    id_detail INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_transaksi TEXT NOT NULL,
                    id_barang TEXT NOT NULL,
                    jumlah INTEGER NOT NULL CHECK(jumlah > 0),
                    subtotal REAL NOT NULL CHECK(subtotal >= 0),
                    FOREIGN KEY (id_transaksi) REFERENCES Transaksi(id_transaksi) ON DELETE CASCADE,
                    FOREIGN KEY (id_barang) REFERENCES Barang(id_barang)
                );
            """)

            conn.commit()

            # Seed default users if table is empty
            cursor.execute("SELECT COUNT(*) FROM User")
            if cursor.fetchone()[0] == 0:
                # Password default: admin (Owner) and kasir (Kasir)
                admin_pw = self.hash_password("admin")
                kasir_pw = self.hash_password("kasir")
                cursor.execute(
                    "INSERT INTO User (username, password, nama, role) VALUES (?, ?, ?, ?)",
                    ("admin", admin_pw, "Administrator Owner", "Owner")
                )
                cursor.execute(
                    "INSERT INTO User (username, password, nama, role) VALUES (?, ?, ?, ?)",
                    ("kasir", kasir_pw, "Kasir Toko", "Kasir")
                )
                conn.commit()

        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            raise DatabaseError(f"Gagal menginisialisasi database: {e}")
        finally:
            if conn:
                conn.close()

    @staticmethod
    def hash_password(password):
        """Utility function to hash passwords using SHA-256."""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def execute_query(self, sql, params=(), fetch=None):
        """
        Executes a single SQL query securely and returns results.
        Fulfills DRY principle by grouping connection opening, execution, commit, and closing.
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params)
            
            result = None
            if fetch == "one":
                result = cursor.fetchone()
            elif fetch == "all":
                result = cursor.fetchall()
            
            conn.commit()
            return result
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            raise DatabaseError(f"Terjadi kesalahan database saat eksekusi: {e}")
        finally:
            if conn:
                conn.close()


# =====================================================================
# ENTITY MODELS (OOP: Encapsulation)
# =====================================================================

class User:
    """Encapsulates User data and properties."""
    def __init__(self, username, password, nama, role, id_user=None):
        self._id_user = id_user
        self.username = username
        self.password = password  # Stored hashed or raw depending on source, validation handles it
        self.nama = nama
        self.role = role

    @property
    def id_user(self):
        return self._id_user

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, val):
        if not val or not val.strip():
            raise ValueError("Username tidak boleh kosong!")
        self._username = val.strip()

    @property
    def nama(self):
        return self._nama

    @nama.setter
    def nama(self, val):
        if not val or not val.strip():
            raise ValueError("Nama lengkap tidak boleh kosong!")
        self._nama = val.strip()

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, val):
        if val not in ("Owner", "Kasir"):
            raise ValueError("Role harus berupa 'Owner' atau 'Kasir'!")
        self._role = val

class Barang:
    """Encapsulates Barang data, properties and validation logic."""
    def __init__(self, id_barang, nama_barang, kategori, harga, stok):
        self.id_barang = id_barang
        self.nama_barang = nama_barang
        self.kategori = kategori
        self.harga = harga
        self.stok = stok

    @property
    def id_barang(self):
        return self._id_barang

    @id_barang.setter
    def id_barang(self, val):
        if not val or not val.strip():
            raise ValueError("ID Barang tidak boleh kosong!")
        self._id_barang = val.strip()

    @property
    def nama_barang(self):
        return self._nama_barang

    @nama_barang.setter
    def nama_barang(self, val):
        if not val or not val.strip():
            raise ValueError("Nama barang tidak boleh kosong!")
        self._nama_barang = val.strip()

    @property
    def kategori(self):
        return self._kategori

    @kategori.setter
    def kategori(self, val):
        if not val or not val.strip():
            raise ValueError("Kategori tidak boleh kosong!")
        self._kategori = val.strip()

    @property
    def harga(self):
        return self._harga

    @harga.setter
    def harga(self, val):
        try:
            val_f = float(val)
        except (ValueError, TypeError):
            raise ValueError("Harga barang harus berupa angka desimal/bulat!")
        if val_f < 0:
            raise ValueError("Harga barang tidak boleh kurang dari 0!")
        self._harga = val_f

    @property
    def stok(self):
        return self._stok

    @stok.setter
    def stok(self, val):
        try:
            val_i = int(val)
        except (ValueError, TypeError):
            raise ValueError("Stok barang harus berupa angka bulat!")
        if val_i < 0:
            raise ValueError("Stok barang tidak boleh kurang dari 0!")
        self._stok = val_i

class DetailTransaksi:
    """Encapsulates Transaction Item Detail."""
    def __init__(self, id_barang, jumlah, subtotal, nama_barang=None, id_detail=None, id_transaksi=None):
        self.id_detail = id_detail
        self.id_transaksi = id_transaksi
        self.id_barang = id_barang
        self.jumlah = jumlah
        self.subtotal = subtotal
        self.nama_barang = nama_barang  # Helper for display

    @property
    def jumlah(self):
        return self._jumlah

    @jumlah.setter
    def jumlah(self, val):
        try:
            val_i = int(val)
        except (ValueError, TypeError):
            raise ValueError("Jumlah beli harus berupa angka bulat!")
        if val_i <= 0:
            raise ValueError("Jumlah beli harus lebih besar dari 0!")
        self._jumlah = val_i

    @property
    def subtotal(self):
        return self._subtotal

    @subtotal.setter
    def subtotal(self, val):
        try:
            val_f = float(val)
        except (ValueError, TypeError):
            raise ValueError("Subtotal harus berupa angka!")
        if val_f < 0:
            raise ValueError("Subtotal tidak boleh kurang dari 0!")
        self._subtotal = val_f

class Transaksi:
    """Encapsulates Header Transaction records."""
    def __init__(self, id_transaksi, pelanggan, kasir, total, bayar, kembalian, tanggal=None, details=None):
        self.id_transaksi = id_transaksi
        self.tanggal = tanggal or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.pelanggan = pelanggan
        self.kasir = kasir
        self.total = total
        self.bayar = bayar
        self.kembalian = kembalian
        self.details = details or []

    @property
    def id_transaksi(self):
        return self._id_transaksi

    @id_transaksi.setter
    def id_transaksi(self, val):
        if not val or not val.strip():
            raise ValueError("ID Transaksi tidak boleh kosong!")
        self._id_transaksi = val.strip()

    @property
    def pelanggan(self):
        return self._pelanggan

    @pelanggan.setter
    def pelanggan(self, val):
        if not val or not val.strip():
            raise ValueError("Nama pelanggan tidak boleh kosong!")
        self._pelanggan = val.strip()

    @property
    def total(self):
        return self._total

    @total.setter
    def total(self, val):
        try:
            val_f = float(val)
        except (ValueError, TypeError):
            raise ValueError("Total belanja harus berupa angka!")
        if val_f < 0:
            raise ValueError("Total belanja tidak boleh kurang dari 0!")
        self._total = val_f

    @property
    def bayar(self):
        return self._bayar

    @bayar.setter
    def bayar(self, val):
        try:
            val_f = float(val)
        except (ValueError, TypeError):
            raise ValueError("Nominal bayar harus berupa angka!")
        if val_f < 0:
            raise ValueError("Nominal bayar tidak boleh kurang dari 0!")
        self._bayar = val_f

    @property
    def kembalian(self):
        return self._kembalian

    @kembalian.setter
    def kembalian(self, val):
        try:
            val_f = float(val)
        except (ValueError, TypeError):
            raise ValueError("Kembalian harus berupa angka!")
        if val_f < 0:
            raise ValueError("Nominal kembalian kurang dari 0! Uang bayar tidak mencukupi.")
        self._kembalian = val_f


# =====================================================================
# REPOSITORY/MANAGER LAYER
# =====================================================================

class ModelManager:
    """Base Manager referencing the Database instance."""
    def __init__(self, db: Database):
        self.db = db

class UserManager(ModelManager):
    """Manages User credentials, registration, and user profiles CRUD."""
    
    def authenticate(self, username, password):
        """Authenticates user. Returns a User object if valid, else None."""
        hashed = self.db.hash_password(password)
        res = self.db.execute_query(
            "SELECT * FROM User WHERE username = ? AND password = ?",
            (username, hashed),
            fetch="one"
        )
        if res:
            return User(
                id_user=res["id_user"],
                username=res["username"],
                password=res["password"],
                nama=res["nama"],
                role=res["role"]
            )
        return None

    def create(self, user_obj: User):
        """Creates a new user in database. Password is automatically hashed."""
        hashed = self.db.hash_password(user_obj.password)
        self.db.execute_query(
            "INSERT INTO User (username, password, nama, role) VALUES (?, ?, ?, ?)",
            (user_obj.username, hashed, user_obj.nama, user_obj.role)
        )

    def get_all(self):
        """Fetches all users."""
        rows = self.db.execute_query("SELECT * FROM User ORDER BY id_user DESC", fetch="all")
        users = []
        for r in rows:
            users.append(User(
                id_user=r["id_user"],
                username=r["username"],
                password=r["password"],
                nama=r["nama"],
                role=r["role"]
            ))
        return users

    def update(self, user_obj: User, new_password=None):
        """Updates user profile. If new_password is provided, updates hashed password."""
        if new_password and new_password.strip():
            hashed = self.db.hash_password(new_password)
            self.db.execute_query(
                "UPDATE User SET username = ?, password = ?, nama = ?, role = ? WHERE id_user = ?",
                (user_obj.username, hashed, user_obj.nama, user_obj.role, user_obj.id_user)
            )
        else:
            self.db.execute_query(
                "UPDATE User SET username = ?, nama = ?, role = ? WHERE id_user = ?",
                (user_obj.username, user_obj.nama, user_obj.role, user_obj.id_user)
            )

    def delete(self, id_user):
        """Deletes user from table."""
        self.db.execute_query("DELETE FROM User WHERE id_user = ?", (id_user,))


class BarangManager(ModelManager):
    """Manages inventory items CRUD."""

    def generate_next_id(self):
        """Generates a sequential product ID (e.g. BRG-0001, BRG-0002)."""
        row = self.db.execute_query("SELECT id_barang FROM Barang ORDER BY id_barang DESC LIMIT 1", fetch="one")
        if not row:
            return "BRG-0001"
        last_id = row["id_barang"]
        try:
            num = int(last_id.split("-")[1])
            return f"BRG-{(num + 1):04d}"
        except (IndexError, ValueError):
            return "BRG-0001"

    def create(self, barang_obj: Barang):
        """Registers a new item."""
        self.db.execute_query(
            "INSERT INTO Barang (id_barang, nama_barang, kategori, harga, stok) VALUES (?, ?, ?, ?, ?)",
            (barang_obj.id_barang, barang_obj.nama_barang, barang_obj.kategori, barang_obj.harga, barang_obj.stok)
        )

    def get_all(self):
        """Fetches all inventory items."""
        rows = self.db.execute_query("SELECT * FROM Barang ORDER BY id_barang ASC", fetch="all")
        items = []
        for r in rows:
            items.append(Barang(
                id_barang=r["id_barang"],
                nama_barang=r["nama_barang"],
                kategori=r["kategori"],
                harga=r["harga"],
                stok=r["stok"]
            ))
        return items

    def get_by_id(self, id_barang):
        """Fetches specific item details."""
        row = self.db.execute_query("SELECT * FROM Barang WHERE id_barang = ?", (id_barang,), fetch="one")
        if row:
            return Barang(
                id_barang=row["id_barang"],
                nama_barang=row["nama_barang"],
                kategori=row["kategori"],
                harga=row["harga"],
                stok=row["stok"]
            )
        return None

    def update(self, barang_obj: Barang):
        """Updates product information."""
        self.db.execute_query(
            "UPDATE Barang SET nama_barang = ?, kategori = ?, harga = ?, stok = ? WHERE id_barang = ?",
            (barang_obj.nama_barang, barang_obj.kategori, barang_obj.harga, barang_obj.stok, barang_obj.id_barang)
        )

    def delete(self, id_barang):
        """Removes a product from inventory."""
        self.db.execute_query("DELETE FROM Barang WHERE id_barang = ?", (id_barang,))

    def search(self, query):
        """Searches products by ID, name, or category."""
        like_q = f"%{query}%"
        rows = self.db.execute_query(
            "SELECT * FROM Barang WHERE id_barang LIKE ? OR nama_barang LIKE ? OR kategori LIKE ? ORDER BY id_barang ASC",
            (like_q, like_q, like_q),
            fetch="all"
        )
        items = []
        for r in rows:
            items.append(Barang(
                id_barang=r["id_barang"],
                nama_barang=r["nama_barang"],
                kategori=r["kategori"],
                harga=r["harga"],
                stok=r["stok"]
            ))
        return items

    def get_low_stock(self, limit=5):
        """Retrieves items whose stock is less than or equal to `limit`."""
        rows = self.db.execute_query(
            "SELECT * FROM Barang WHERE stok <= ? ORDER BY stok ASC",
            (limit,),
            fetch="all"
        )
        items = []
        for r in rows:
            items.append(Barang(
                id_barang=r["id_barang"],
                nama_barang=r["nama_barang"],
                kategori=r["kategori"],
                harga=r["harga"],
                stok=r["stok"]
            ))
        return items

    def get_total_count(self):
        """Returns total distinct items in inventory."""
        row = self.db.execute_query("SELECT COUNT(*) FROM Barang", fetch="one")
        return row[0] if row else 0


class TransaksiManager(ModelManager):
    """Manages transaction checkout processes, invoices, and logs."""

    def generate_next_id(self):
        """Generates invoice ID using format TR-YYYYMMDD-XXXX."""
        date_str = datetime.now().strftime("%Y%m%d")
        prefix = f"TR-{date_str}-"
        row = self.db.execute_query(
            "SELECT id_transaksi FROM Transaksi WHERE id_transaksi LIKE ? ORDER BY id_transaksi DESC LIMIT 1",
            (prefix + "%",),
            fetch="one"
        )
        if not row:
            return f"{prefix}0001"
        last_id = row["id_transaksi"]
        try:
            num = int(last_id.split("-")[2])
            return f"{prefix}{(num + 1):04d}"
        except (IndexError, ValueError):
            return f"{prefix}0001"

    def create(self, tx_obj: Transaksi):
        """
        Saves transaction and its details, and updates product stocks atomically.
        Fulfills strict MVC data integrity checks.
        """
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            # Verify and update stock for each item before inserting transaction header
            for item in tx_obj.details:
                cursor.execute("SELECT stok, nama_barang FROM Barang WHERE id_barang = ?", (item.id_barang,))
                res = cursor.fetchone()
                if not res:
                    raise ValueError(f"Barang {item.id_barang} tidak ditemukan di database!")
                
                curr_stock = res["stok"]
                nama_b = res["nama_barang"]
                if curr_stock < item.jumlah:
                    raise ValueError(f"Stok untuk '{nama_b}' tidak mencukupi! (Stok: {curr_stock}, Beli: {item.jumlah})")

            # 1. Insert Transaksi header
            cursor.execute(
                "INSERT INTO Transaksi (id_transaksi, tanggal, pelanggan, kasir, total, bayar, kembalian) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (tx_obj.id_transaksi, tx_obj.tanggal, tx_obj.pelanggan, tx_obj.kasir, tx_obj.total, tx_obj.bayar, tx_obj.kembalian)
            )

            # 2. Insert Detail_Transaksi & Decrement Barang Stok
            for item in tx_obj.details:
                cursor.execute(
                    "INSERT INTO Detail_Transaksi (id_transaksi, id_barang, jumlah, subtotal) VALUES (?, ?, ?, ?)",
                    (tx_obj.id_transaksi, item.id_barang, item.jumlah, item.subtotal)
                )
                cursor.execute(
                    "UPDATE Barang SET stok = stok - ? WHERE id_barang = ?",
                    (item.jumlah, item.id_barang)
                )

            conn.commit()
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            raise DatabaseError(f"Gagal memproses transaksi di database: {e}")
        except ValueError as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()

    def get_all(self):
        """Fetches all transaction headers."""
        rows = self.db.execute_query("SELECT * FROM Transaksi ORDER BY tanggal DESC", fetch="all")
        txs = []
        for r in rows:
            txs.append(Transaksi(
                id_transaksi=r["id_transaksi"],
                tanggal=r["tanggal"],
                pelanggan=r["pelanggan"],
                kasir=r["kasir"],
                total=r["total"],
                bayar=r["bayar"],
                kembalian=r["kembalian"]
            ))
        return txs

    def get_details(self, id_transaksi):
        """Fetches items for a specific transaction invoice."""
        rows = self.db.execute_query(
            """
            SELECT dt.*, b.nama_barang 
            FROM Detail_Transaksi dt
            JOIN Barang b ON dt.id_barang = b.id_barang
            WHERE dt.id_transaksi = ?
            ORDER BY dt.id_detail ASC
            """,
            (id_transaksi,),
            fetch="all"
        )
        details = []
        for r in rows:
            details.append(DetailTransaksi(
                id_detail=r["id_detail"],
                id_transaksi=r["id_transaksi"],
                id_barang=r["id_barang"],
                jumlah=r["jumlah"],
                subtotal=r["subtotal"],
                nama_barang=r["nama_barang"]
            ))
        return details

    def get_total_count(self):
        """Returns total transactions count."""
        row = self.db.execute_query("SELECT COUNT(*) FROM Transaksi", fetch="one")
        return row[0] if row else 0

    def get_income_today(self):
        """Returns total revenue collected today."""
        today = datetime.now().strftime("%Y-%m-%d")
        row = self.db.execute_query(
            "SELECT SUM(total) FROM Transaksi WHERE tanggal LIKE ?",
            (today + "%",),
            fetch="one"
        )
        return row[0] if row and row[0] is not None else 0.0

    def get_report_data(self, start_date, end_date):
        """
        Gets transaction report summaries filtered by start and end dates.
        Fits date values (YYYY-MM-DD) by comparing strings.
        """
        # Ensure times are appended to search the whole days
        s_date = f"{start_date} 00:00:00"
        e_date = f"{end_date} 23:59:59"
        
        rows = self.db.execute_query(
            "SELECT * FROM Transaksi WHERE tanggal >= ? AND tanggal <= ? ORDER BY tanggal DESC",
            (s_date, e_date),
            fetch="all"
        )
        
        txs = []
        for r in rows:
            txs.append(Transaksi(
                id_transaksi=r["id_transaksi"],
                tanggal=r["tanggal"],
                pelanggan=r["pelanggan"],
                kasir=r["kasir"],
                total=r["total"],
                bayar=r["bayar"],
                kembalian=r["kembalian"]
            ))
        return txs

    def get_revenue_summary(self, start_date, end_date):
        """Calculates total revenue and items sold in a date range."""
        s_date = f"{start_date} 00:00:00"
        e_date = f"{end_date} 23:59:59"
        
        row_income = self.db.execute_query(
            "SELECT SUM(total) FROM Transaksi WHERE tanggal >= ? AND tanggal <= ?",
            (s_date, e_date),
            fetch="one"
        )
        row_qty = self.db.execute_query(
            """
            SELECT SUM(dt.jumlah) 
            FROM Detail_Transaksi dt
            JOIN Transaksi t ON dt.id_transaksi = t.id_transaksi
            WHERE t.tanggal >= ? AND t.tanggal <= ?
            """,
            (s_date, e_date),
            fetch="one"
        )
        
        income = row_income[0] if row_income and row_income[0] is not None else 0.0
        qty = row_qty[0] if row_qty and row_qty[0] is not None else 0
        return income, qty
