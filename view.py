import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# =====================================================================
# CUSTOM STYLE HELPER
# =====================================================================

def init_styles():
    """Initializes modern styles for the ttk widgets."""
    style = ttk.Style()
    style.theme_use("clam")

    # Color Palette
    bg_light = "#f8fafc"       # Slate 50 (App background)
    bg_content = "#ffffff"     # White (Card/Content panel background)
    bg_dark = "#0f172a"        # Slate 900 (Sidebar background)
    accent_blue = "#2563eb"    # Blue 600 (Primary buttons & links)
    accent_blue_hover = "#1d4ed8"
    text_dark = "#0f172a"      # Dark text
    text_muted = "#64748b"     # Slate 500 (Subtitles/Labels)
    border_color = "#cbd5e1"   # Slate 300 (Input borders)
    
    # Configure base frame and panels
    style.configure("TFrame", background=bg_light)
    style.configure("Content.TFrame", background=bg_light)
    
    # Cards
    style.configure("Card.TFrame", background=bg_content, borderwidth=1, relief="solid")
    
    # Sidebar
    style.configure("Sidebar.TFrame", background=bg_dark)
    style.configure("Sidebar.TButton", 
                    background=bg_dark, 
                    foreground="#f1f5f9", 
                    font=("Segoe UI", 10, "bold"), 
                    borderwidth=0, 
                    focuscolor=bg_dark, 
                    anchor="w", 
                    padding=(15, 10))
    style.map("Sidebar.TButton",
        background=[('active', '#1e293b'), ('pressed', '#1e293b')],
        foreground=[('active', '#ffffff'), ('pressed', '#ffffff')]
    )
    
    # Standard Buttons
    style.configure("TButton", 
                    font=("Segoe UI", 10, "bold"), 
                    padding=(12, 6), 
                    background=accent_blue, 
                    foreground="#ffffff", 
                    borderwidth=0)
    style.map("TButton",
        background=[('active', accent_blue_hover), ('disabled', '#cbd5e1')],
        foreground=[('active', '#ffffff'), ('disabled', '#94a3b8')]
    )
    
    # Success Button
    style.configure("Success.TButton", 
                    background="#16a34a", 
                    foreground="#ffffff", 
                    font=("Segoe UI", 10, "bold"), 
                    padding=(12, 6), 
                    borderwidth=0)
    style.map("Success.TButton",
        background=[('active', '#15803d'), ('disabled', '#cbd5e1')]
    )
    
    # Danger Button
    style.configure("Danger.TButton", 
                    background="#dc2626", 
                    foreground="#ffffff", 
                    font=("Segoe UI", 10, "bold"), 
                    padding=(12, 6), 
                    borderwidth=0)
    style.map("Danger.TButton",
        background=[('active', '#b91c1c'), ('disabled', '#cbd5e1')]
    )

    # Secondary Button (Muted grey)
    style.configure("Secondary.TButton", 
                    background="#64748b", 
                    foreground="#ffffff", 
                    font=("Segoe UI", 10, "bold"), 
                    padding=(12, 6), 
                    borderwidth=0)
    style.map("Secondary.TButton",
        background=[('active', '#475569')]
    )

    # Labels
    style.configure("TLabel", background=bg_light, foreground=text_dark, font=("Segoe UI", 10))
    style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"), foreground=bg_dark)
    style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"), foreground=text_dark)
    style.configure("Sub.TLabel", font=("Segoe UI", 10, "italic"), foreground=text_muted)
    style.configure("CardTitle.TLabel", font=("Segoe UI", 9, "bold"), foreground=text_muted, background=bg_content)
    style.configure("CardValue.TLabel", font=("Segoe UI", 16, "bold"), foreground=bg_dark, background=bg_content)
    
    # Entry inputs
    style.configure("TEntry", fieldbackground="#ffffff", bordercolor=border_color, font=("Segoe UI", 10))
    style.configure("TCombobox", fieldbackground="#ffffff", font=("Segoe UI", 10))
    
    # Treeview (Modern Styling)
    style.configure("Treeview", 
                    background="#ffffff", 
                    foreground=text_dark, 
                    rowheight=26, 
                    fieldbackground="#ffffff", 
                    font=("Segoe UI", 9),
                    borderwidth=0)
    style.map("Treeview",
        background=[('selected', '#dbeafe')],  # Slate/Blue selection
        foreground=[('selected', '#1e40af')]
    )
    
    style.configure("Treeview.Heading", 
                    background="#f1f5f9", 
                    foreground=text_dark, 
                    font=("Segoe UI", 9, "bold"), 
                    padding=6,
                    borderwidth=1,
                    relief="flat")
    style.map("Treeview.Heading",
              background=[('active', '#e2e8f0')])


# =====================================================================
# BASE PAGE (OOP: Inheritance)
# =====================================================================

class BasePage(ttk.Frame):
    """Base class for all visual screens/frames."""
    def __init__(self, parent, controller=None):
        super().__init__(parent, style="Content.TFrame")
        self.controller = controller

    def refresh_page(self):
        """Polymorphic method for loading data. Each child page implements this."""
        pass


# =====================================================================
# 1. LOGIN PAGE
# =====================================================================

class LoginPage(BasePage):
    """Login UI Frame."""
    def __init__(self, parent, controller=None):
        super().__init__(parent, controller)
        self.setup_ui()

    def setup_ui(self):
        # Configure layout grids
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Center Card Container
        card = ttk.Frame(self, style="Card.TFrame", padding=30)
        card.grid(row=0, column=0, sticky="")
        
        # Inner components
        lbl_title = ttk.Label(card, text="SISTEM KASIR RISKY", font=("Segoe UI", 16, "bold"), foreground="#0f172a", background="#ffffff")
        lbl_title.pack(pady=(0, 5))
        
        lbl_subtitle = ttk.Label(card, text="Silakan masuk untuk melanjutkan", font=("Segoe UI", 10), foreground="#64748b", background="#ffffff")
        lbl_subtitle.pack(pady=(0, 20))

        # Username Input
        lbl_user = ttk.Label(card, text="Username:", font=("Segoe UI", 10, "bold"), background="#ffffff")
        lbl_user.pack(anchor="w", pady=(0, 5))
        self.ent_user = ttk.Entry(card, width=30)
        self.ent_user.pack(pady=(0, 15))

        # Password Input
        lbl_pass = ttk.Label(card, text="Password:", font=("Segoe UI", 10, "bold"), background="#ffffff")
        lbl_pass.pack(anchor="w", pady=(0, 5))
        self.ent_pass = ttk.Entry(card, show="*", width=30)
        self.ent_pass.pack(pady=(0, 25))

        # Submit Button
        self.btn_login = ttk.Button(card, text="MASUK", width=25)
        self.btn_login.pack(pady=(0, 10))

        # Enter key triggers login
        self.ent_pass.bind("<Return>", lambda e: self.btn_login.invoke())
        self.ent_user.bind("<Return>", lambda e: self.btn_login.invoke())

    def clear_inputs(self):
        self.ent_user.delete(0, tk.END)
        self.ent_pass.delete(0, tk.END)
        self.ent_user.focus_set()


# =====================================================================
# 2. DASHBOARD PAGE
# =====================================================================

class DashboardPage(BasePage):
    """Dashboard visual metrics and low-stock indicators."""
    def __init__(self, parent, controller=None):
        super().__init__(parent, controller)
        self.setup_ui()

    def setup_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Header Label
        lbl_header = ttk.Label(self, text="DASHBOARD UTAMA", style="Title.TLabel")
        lbl_header.grid(row=0, column=0, sticky="w", padx=20, pady=20)

        # Metrics panel (Row of cards)
        metrics_frame = ttk.Frame(self)
        metrics_frame.grid(row=1, column=0, sticky="nwe", padx=20)
        metrics_frame.columnconfigure((0, 1, 2, 3), weight=1)

        # Create Metric Cards
        self.card_barang = self.create_card(metrics_frame, "TOTAL BARANG", "0", "#2563eb", 0)
        self.card_transaksi = self.create_card(metrics_frame, "TOTAL TRANSAKSI", "0", "#16a34a", 1)
        self.card_pendapatan = self.create_card(metrics_frame, "PENDAPATAN HARI INI", "Rp 0", "#8b5cf6", 2)
        self.card_alert = self.create_card(metrics_frame, "STOK HAMPIR HABIS", "0 Item", "#dc2626", 3)

        # Bottom section: Low Stock Table Indicator
        table_frame = ttk.Frame(self)
        table_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=20)
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(1, weight=1)

        lbl_alert_title = ttk.Label(table_frame, text="Daftar Barang Stok Menipis (<= 5 Unit)", style="Header.TLabel")
        lbl_alert_title.grid(row=0, column=0, sticky="w", pady=(10, 5))

        # Treeview for warnings
        columns = ("id", "nama", "kategori", "harga", "stok")
        self.tree_warn = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree_warn.heading("id", text="ID Barang")
        self.tree_warn.heading("nama", text="Nama Barang")
        self.tree_warn.heading("kategori", text="Kategori")
        self.tree_warn.heading("harga", text="Harga Satuan")
        self.tree_warn.heading("stok", text="Stok Tersisa")
        
        self.tree_warn.column("id", width=100, anchor="center")
        self.tree_warn.column("nama", width=250, anchor="w")
        self.tree_warn.column("kategori", width=150, anchor="w")
        self.tree_warn.column("harga", width=120, anchor="e")
        self.tree_warn.column("stok", width=100, anchor="center")

        # Scrollbar
        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_warn.yview)
        self.tree_warn.configure(yscrollcommand=scroll.set)
        
        self.tree_warn.grid(row=1, column=0, sticky="nsew")
        scroll.grid(row=1, column=1, sticky="ns")

    def create_card(self, parent, title, val, color, col):
        """Creates a metric card with a colored highlight band on the left."""
        card_outer = ttk.Frame(parent, style="Card.TFrame", padding=1)
        card_outer.grid(row=0, column=col, padx=8, pady=10, sticky="nsew")
        
        # Color indicator stripe
        stripe = tk.Frame(card_outer, bg=color, width=5)
        stripe.pack(side="left", fill="y")
        
        card_inner = ttk.Frame(card_outer, padding=12)
        card_inner.pack(side="left", fill="both", expand=True)
        # Force background colors inside card elements
        card_inner.configure(style="TFrame")
        
        lbl_t = ttk.Label(card_inner, text=title, style="CardTitle.TLabel")
        lbl_t.pack(anchor="w")
        
        lbl_v = ttk.Label(card_inner, text=val, style="CardValue.TLabel")
        lbl_v.pack(anchor="w", pady=(5, 0))
        
        return lbl_v  # Return label reference so controller can update it later


# =====================================================================
# 3. BARANG PAGE (CRUD)
# =====================================================================

class BarangPage(BasePage):
    """Inventory management UI frame (CRUD)."""
    def __init__(self, parent, controller=None):
        super().__init__(parent, controller)
        self.setup_ui()

    def setup_ui(self):
        # Configure layout grids
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # ------------------ LEFT SIDE: FORM INPUT ------------------
        form_frame = ttk.Frame(self, padding=15)
        form_frame.grid(row=0, column=0, sticky="ns", padx=(20, 10), pady=20)
        
        lbl_form_title = ttk.Label(form_frame, text="Form Barang", style="Header.TLabel")
        lbl_form_title.pack(anchor="w", pady=(0, 15))

        # Inputs
        ttk.Label(form_frame, text="ID Barang:", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.ent_id = ttk.Entry(form_frame, width=25)
        self.ent_id.pack(fill="x", pady=(0, 10))

        ttk.Label(form_frame, text="Nama Barang:", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.ent_nama = ttk.Entry(form_frame, width=25)
        self.ent_nama.pack(fill="x", pady=(0, 10))

        ttk.Label(form_frame, text="Kategori:", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.ent_kategori = ttk.Combobox(form_frame, width=23, values=["Sembako", "Makanan", "Minuman", "Perlengkapan Mandi", "Rokok", "Lain-lain"])
        self.ent_kategori.pack(fill="x", pady=(0, 10))

        ttk.Label(form_frame, text="Harga Jual:", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.ent_harga = ttk.Entry(form_frame, width=25)
        self.ent_harga.pack(fill="x", pady=(0, 10))

        ttk.Label(form_frame, text="Stok:", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.ent_stok = ttk.Entry(form_frame, width=25)
        self.ent_stok.pack(fill="x", pady=(0, 20))

        # Form Buttons
        self.btn_save = ttk.Button(form_frame, text="Simpan Data", style="Success.TButton")
        self.btn_save.pack(fill="x", pady=2)
        
        self.btn_clear = ttk.Button(form_frame, text="Bersihkan Form", style="Secondary.TButton")
        self.btn_clear.pack(fill="x", pady=2)
        
        self.btn_delete = ttk.Button(form_frame, text="Hapus Barang", style="Danger.TButton")
        self.btn_delete.pack(fill="x", pady=(15, 2))

        # ------------------ RIGHT SIDE: TABLE LIST ------------------
        list_frame = ttk.Frame(self)
        list_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(1, weight=1)

        # Search Bar
        search_frame = ttk.Frame(list_frame)
        search_frame.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        ttk.Label(search_frame, text="Cari Barang:", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, padx=(0, 5))
        self.ent_search = ttk.Entry(search_frame, width=30)
        self.ent_search.grid(row=0, column=1, padx=(0, 5))
        self.btn_search = ttk.Button(search_frame, text="Cari")
        self.btn_search.grid(row=0, column=2)

        # Table & Scroll
        columns = ("id", "nama", "kategori", "harga", "stok")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        self.tree.heading("id", text="ID Barang")
        self.tree.heading("nama", text="Nama Barang")
        self.tree.heading("kategori", text="Kategori")
        self.tree.heading("harga", text="Harga Satuan")
        self.tree.heading("stok", text="Stok")
        
        self.tree.column("id", width=80, anchor="center")
        self.tree.column("nama", width=200, anchor="w")
        self.tree.column("kategori", width=120, anchor="w")
        self.tree.column("harga", width=100, anchor="e")
        self.tree.column("stok", width=80, anchor="center")

        scroll = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        
        self.tree.grid(row=1, column=0, sticky="nsew")
        scroll.grid(row=1, column=1, sticky="ns")

    def get_inputs(self):
        """Retrieves user form text input."""
        return {
            "id_barang": self.ent_id.get(),
            "nama_barang": self.ent_nama.get(),
            "kategori": self.ent_kategori.get(),
            "harga": self.ent_harga.get(),
            "stok": self.ent_stok.get()
        }

    def fill_form(self, id_val, nama, kategori, harga, stok):
        """Populates the input form fields."""
        self.clear_form()
        self.ent_id.insert(0, id_val)
        self.ent_id.configure(state="disabled")  # Freeze Primary Key on update
        self.ent_nama.insert(0, nama)
        self.ent_kategori.set(kategori)
        self.ent_harga.insert(0, str(harga))
        self.ent_stok.insert(0, str(stok))

    def clear_form(self):
        """Clears all input widgets on the form."""
        self.ent_id.configure(state="normal")
        self.ent_id.delete(0, tk.END)
        self.ent_nama.delete(0, tk.END)
        self.ent_kategori.set("")
        self.ent_harga.delete(0, tk.END)
        self.ent_stok.delete(0, tk.END)


# =====================================================================
# 4. TRANSAKSI PAGE (CHECKOUT KASIR)
# =====================================================================

class TransaksiPage(BasePage):
    """Point of Sale checkout cash register."""
    def __init__(self, parent, controller=None):
        super().__init__(parent, controller)
        self.setup_ui()

    def setup_ui(self):
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure(1, weight=1)

        # ------------------ TOP: Header Info ------------------
        info_frame = ttk.Frame(self, padding=10)
        info_frame.grid(row=0, column=0, columnspan=2, sticky="we", padx=20, pady=(15, 0))
        
        ttk.Label(info_frame, text="TRANSAKSI BARU (KASIR)", style="Header.TLabel").grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))

        ttk.Label(info_frame, text="No. Invoice:", font=("Segoe UI", 9, "bold")).grid(row=1, column=0, sticky="w", padx=(0, 5))
        self.lbl_invoice = ttk.Label(info_frame, text="TR-XXXXXX-XXXX", font=("Segoe UI", 10, "bold"), foreground="#2563eb")
        self.lbl_invoice.grid(row=1, column=1, sticky="w", padx=(0, 20))

        # Hidden entry to prevent controller errors and record cashier name silently
        self.ent_pelanggan = ttk.Entry(info_frame)

        ttk.Label(info_frame, text="Petugas (Kasir):", font=("Segoe UI", 9, "bold")).grid(row=1, column=2, sticky="w", padx=(0, 5))
        self.lbl_kasir = ttk.Label(info_frame, text="-", font=("Segoe UI", 10, "italic"))
        self.lbl_kasir.grid(row=1, column=3, sticky="w")

        # ------------------ MIDDLE LEFT: PRODUCT LIST ------------------
        prod_frame = ttk.Frame(self)
        prod_frame.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=15)
        prod_frame.columnconfigure(0, weight=1)
        prod_frame.rowconfigure(2, weight=1)

        # Search Bar
        search_frame = ttk.Frame(prod_frame)
        search_frame.grid(row=0, column=0, sticky="we", pady=(0, 5))
        self.ent_search_prod = ttk.Entry(search_frame, width=25)
        self.ent_search_prod.pack(side="left", padx=(0, 5), fill="x", expand=True)
        self.btn_search_prod = ttk.Button(search_frame, text="Cari")
        self.btn_search_prod.pack(side="left")

        ttk.Label(prod_frame, text="Klik 2x pada barang untuk memasukkan ke keranjang:", style="Sub.TLabel").grid(row=1, column=0, sticky="w", pady=(0, 5))

        # Products Table
        prod_cols = ("id", "nama", "harga", "stok")
        self.tree_prod = ttk.Treeview(prod_frame, columns=prod_cols, show="headings")
        self.tree_prod.heading("id", text="Kode")
        self.tree_prod.heading("nama", text="Nama Barang")
        self.tree_prod.heading("harga", text="Harga")
        self.tree_prod.heading("stok", text="Stok")
        
        self.tree_prod.column("id", width=80, anchor="center")
        self.tree_prod.column("nama", width=180, anchor="w")
        self.tree_prod.column("harga", width=80, anchor="e")
        self.tree_prod.column("stok", width=60, anchor="center")

        scroll_prod = ttk.Scrollbar(prod_frame, orient="vertical", command=self.tree_prod.yview)
        self.tree_prod.configure(yscrollcommand=scroll_prod.set)
        
        self.tree_prod.grid(row=2, column=0, sticky="nsew")
        scroll_prod.grid(row=2, column=1, sticky="ns")

        # ------------------ MIDDLE RIGHT: CART ------------------
        cart_frame = ttk.Frame(self)
        cart_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 20), pady=15)
        cart_frame.columnconfigure(0, weight=1)
        cart_frame.rowconfigure(1, weight=1)

        # Cart controls
        cart_controls = ttk.Frame(cart_frame)
        cart_controls.grid(row=0, column=0, sticky="we", pady=(0, 5))
        
        ttk.Label(cart_controls, text="Daftar Keranjang", style="Header.TLabel").pack(side="left")
        self.btn_remove_cart = ttk.Button(cart_controls, text="Hapus Item", style="Danger.TButton")
        self.btn_remove_cart.pack(side="right", padx=(5, 0))
        
        self.btn_edit_qty = ttk.Button(cart_controls, text="Ubah Qty", style="Secondary.TButton")
        self.btn_edit_qty.pack(side="right")

        # Cart Table
        cart_cols = ("id", "nama", "harga", "qty", "subtotal")
        self.tree_cart = ttk.Treeview(cart_frame, columns=cart_cols, show="headings")
        self.tree_cart.heading("id", text="Kode")
        self.tree_cart.heading("nama", text="Nama Barang")
        self.tree_cart.heading("harga", text="Harga")
        self.tree_cart.heading("qty", text="Qty")
        self.tree_cart.heading("subtotal", text="Subtotal")

        self.tree_cart.column("id", width=80, anchor="center")
        self.tree_cart.column("nama", width=180, anchor="w")
        self.tree_cart.column("harga", width=80, anchor="e")
        self.tree_cart.column("qty", width=50, anchor="center")
        self.tree_cart.column("subtotal", width=90, anchor="e")

        scroll_cart = ttk.Scrollbar(cart_frame, orient="vertical", command=self.tree_cart.yview)
        self.tree_cart.configure(yscrollcommand=scroll_cart.set)
        
        self.tree_cart.grid(row=1, column=0, sticky="nsew")
        scroll_cart.grid(row=1, column=1, sticky="ns")

        # ------------------ BOTTOM: CHECKOUT PANEL ------------------
        checkout_panel = ttk.Frame(self, style="Card.TFrame", padding=15)
        checkout_panel.grid(row=2, column=0, columnspan=2, sticky="we", padx=20, pady=(0, 20))
        checkout_panel.columnconfigure(2, weight=1)

        # Total belanja
        ttk.Label(checkout_panel, text="TOTAL BELANJA:", font=("Segoe UI", 12, "bold"), background="#ffffff").grid(row=0, column=0, sticky="w")
        self.lbl_total = ttk.Label(checkout_panel, text="Rp 0", font=("Segoe UI", 24, "bold"), foreground="#2563eb", background="#ffffff")
        self.lbl_total.grid(row=1, column=0, sticky="w", columnspan=2, pady=(0, 10))

        # Payment form fields
        ttk.Label(checkout_panel, text="Uang Bayar:", font=("Segoe UI", 10, "bold"), background="#ffffff").grid(row=0, column=2, sticky="e", padx=10)
        self.ent_bayar = ttk.Entry(checkout_panel, font=("Segoe UI", 14, "bold"), width=15)
        self.ent_bayar.grid(row=0, column=3, sticky="w")

        ttk.Label(checkout_panel, text="Uang Kembali:", font=("Segoe UI", 10, "bold"), background="#ffffff").grid(row=1, column=2, sticky="e", padx=10)
        self.lbl_kembali = ttk.Label(checkout_panel, text="Rp 0", font=("Segoe UI", 14, "bold"), foreground="#16a34a", background="#ffffff")
        self.lbl_kembali.grid(row=1, column=3, sticky="w")

        # Action Buttons
        self.btn_pay = ttk.Button(checkout_panel, text="Bayar & Simpan", style="Success.TButton", padding=(20, 10))
        self.btn_pay.grid(row=0, column=4, rowspan=2, padx=(20, 0), sticky="ns")

        self.btn_reset_tx = ttk.Button(checkout_panel, text="Batal", style="Danger.TButton", padding=(15, 10))
        self.btn_reset_tx.grid(row=0, column=5, rowspan=2, padx=(10, 0), sticky="ns")


# =====================================================================
# 5. RIWAYAT TRANSAKSI PAGE
# =====================================================================

class RiwayatPage(BasePage):
    """List and examine completed transaction logs."""
    def __init__(self, parent, controller=None):
        super().__init__(parent, controller)
        self.setup_ui()

    def setup_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure((1, 3), weight=1)

        # Header Title
        ttk.Label(self, text="RIWAYAT TRANSAKSI PENJUALAN", style="Title.TLabel").grid(row=0, column=0, sticky="w", padx=20, pady=15)

        # ------------------ TOP HALF: TRANSACTIONS TABLE ------------------
        tx_frame = ttk.Frame(self)
        tx_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=5)
        tx_frame.columnconfigure(0, weight=1)
        tx_frame.rowconfigure(0, weight=1)

        columns_tx = ("id", "tanggal", "kasir", "total", "bayar", "kembalian")
        self.tree_tx = ttk.Treeview(tx_frame, columns=columns_tx, show="headings")
        self.tree_tx.heading("id", text="No. Invoice")
        self.tree_tx.heading("tanggal", text="Tanggal / Waktu")
        self.tree_tx.heading("kasir", text="Kasir")
        self.tree_tx.heading("total", text="Total")
        self.tree_tx.heading("bayar", text="Bayar")
        self.tree_tx.heading("kembalian", text="Kembalian")

        self.tree_tx.column("id", width=120, anchor="center")
        self.tree_tx.column("tanggal", width=180, anchor="center")
        self.tree_tx.column("kasir", width=150, anchor="w")
        self.tree_tx.column("total", width=100, anchor="e")
        self.tree_tx.column("bayar", width=100, anchor="e")
        self.tree_tx.column("kembalian", width=100, anchor="e")

        scroll_tx = ttk.Scrollbar(tx_frame, orient="vertical", command=self.tree_tx.yview)
        self.tree_tx.configure(yscrollcommand=scroll_tx.set)
        
        self.tree_tx.grid(row=0, column=0, sticky="nsew")
        scroll_tx.grid(row=0, column=1, sticky="ns")

        # ------------------ MIDDLE LABEL ------------------
        ttk.Label(self, text="Rincian Item Belanja Invoice Terpilih:", style="Header.TLabel").grid(row=2, column=0, sticky="w", padx=20, pady=(15, 5))

        # ------------------ BOTTOM HALF: DETAILS TABLE ------------------
        detail_frame = ttk.Frame(self)
        detail_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=(5, 20))
        detail_frame.columnconfigure(0, weight=1)
        detail_frame.rowconfigure(0, weight=1)

        columns_det = ("id_barang", "nama", "harga", "jumlah", "subtotal")
        self.tree_det = ttk.Treeview(detail_frame, columns=columns_det, show="headings")
        self.tree_det.heading("id_barang", text="ID Barang")
        self.tree_det.heading("nama", text="Nama Barang")
        self.tree_det.heading("harga", text="Harga")
        self.tree_det.heading("jumlah", text="Jumlah")
        self.tree_det.heading("subtotal", text="Subtotal")

        self.tree_det.column("id_barang", width=100, anchor="center")
        self.tree_det.column("nama", width=250, anchor="w")
        self.tree_det.column("harga", width=120, anchor="e")
        self.tree_det.column("jumlah", width=80, anchor="center")
        self.tree_det.column("subtotal", width=150, anchor="e")

        scroll_det = ttk.Scrollbar(detail_frame, orient="vertical", command=self.tree_det.yview)
        self.tree_det.configure(yscrollcommand=scroll_det.set)
        
        self.tree_det.grid(row=0, column=0, sticky="nsew")
        scroll_det.grid(row=0, column=1, sticky="ns")


# =====================================================================
# 6. LAPORAN PAGE (REPORTS FILTERED BY DATE)
# =====================================================================

class LaporanPage(BasePage):
    """Filters data ranges for revenue summaries and tables."""
    def __init__(self, parent, controller=None):
        super().__init__(parent, controller)
        self.setup_ui()

    def setup_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        # Header Title
        ttk.Label(self, text="LAPORAN PENJUALAN TOKO", style="Title.TLabel").grid(row=0, column=0, sticky="w", padx=20, pady=15)

        # ------------------ DATE FILTER PANEL ------------------
        filter_frame = ttk.Frame(self, padding=10)
        filter_frame.grid(row=1, column=0, sticky="we", padx=20, pady=(0, 10))

        ttk.Label(filter_frame, text="Mulai Tanggal:", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, padx=(0, 5))
        self.ent_start = ttk.Entry(filter_frame, width=15)
        self.ent_start.insert(0, datetime.now().strftime("%Y-%m-01"))  # default: 1st day of month
        self.ent_start.grid(row=0, column=1, padx=(0, 20))

        ttk.Label(filter_frame, text="Sampai Tanggal:", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, padx=(0, 5))
        self.ent_end = ttk.Entry(filter_frame, width=15)
        self.ent_end.insert(0, datetime.now().strftime("%Y-%m-%d"))  # default: today
        self.ent_end.grid(row=0, column=3, padx=(0, 20))

        self.btn_filter = ttk.Button(filter_frame, text="Saring Laporan")
        self.btn_filter.grid(row=0, column=4)

        # ------------------ METRICS SUMMARY PANEL ------------------
        summary_frame = ttk.Frame(self)
        summary_frame.grid(row=2, column=0, sticky="we", padx=20)
        summary_frame.columnconfigure((0, 1), weight=1)

        self.card_omset = self.create_summary_box(summary_frame, "TOTAL OMSET / PENDAPATAN", "Rp 0", "#16a34a", 0)
        self.card_qty = self.create_summary_box(summary_frame, "TOTAL BARANG TERJUAL", "0 Item", "#2563eb", 1)

        # ------------------ REFRESH TABLE LIST ------------------
        table_frame = ttk.Frame(self)
        table_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=20)
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        cols = ("id", "tanggal", "kasir", "total")
        self.tree_rep = ttk.Treeview(table_frame, columns=cols, show="headings")
        self.tree_rep.heading("id", text="No. Invoice")
        self.tree_rep.heading("tanggal", text="Tanggal / Waktu")
        self.tree_rep.heading("kasir", text="Kasir")
        self.tree_rep.heading("total", text="Total Belanja")

        self.tree_rep.column("id", width=120, anchor="center")
        self.tree_rep.column("tanggal", width=200, anchor="center")
        self.tree_rep.column("kasir", width=180, anchor="w")
        self.tree_rep.column("total", width=150, anchor="e")

        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_rep.yview)
        self.tree_rep.configure(yscrollcommand=scroll.set)
        
        self.tree_rep.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")

    def create_summary_box(self, parent, title, val, color, col):
        """Creates sub-metrics panel boxes for report summaries."""
        box = ttk.Frame(parent, style="Card.TFrame", padding=1)
        box.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")
        
        stripe = tk.Frame(box, bg=color, width=4)
        stripe.pack(side="left", fill="y")
        
        box_inner = ttk.Frame(box, padding=10)
        box_inner.pack(side="left", fill="both", expand=True)
        box_inner.configure(style="TFrame")

        lbl_t = ttk.Label(box_inner, text=title, style="CardTitle.TLabel")
        lbl_t.pack(anchor="w")
        
        lbl_v = ttk.Label(box_inner, text=val, style="CardValue.TLabel")
        lbl_v.pack(anchor="w", pady=(5, 0))

        return lbl_v


# =====================================================================
# 7. USER PAGE (CRUD OWNER)
# =====================================================================

class UserPage(BasePage):
    """User account registrations and role authorization CRUD (Owner only)."""
    def __init__(self, parent, controller=None):
        super().__init__(parent, controller)
        self.setup_ui()

    def setup_ui(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # ------------------ LEFT SIDE: FORM INPUT ------------------
        form_frame = ttk.Frame(self, padding=15)
        form_frame.grid(row=0, column=0, sticky="ns", padx=(20, 10), pady=20)
        
        ttk.Label(form_frame, text="Form Kelola Akun", style="Header.TLabel").pack(anchor="w", pady=(0, 15))

        # ID field (Hidden/Read-only representation)
        self.id_user_var = tk.StringVar()
        
        ttk.Label(form_frame, text="Username:", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.ent_username = ttk.Entry(form_frame, width=25)
        self.ent_username.pack(fill="x", pady=(0, 10))

        ttk.Label(form_frame, text="Nama Lengkap:", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.ent_nama = ttk.Entry(form_frame, width=25)
        self.ent_nama.pack(fill="x", pady=(0, 10))

        ttk.Label(form_frame, text="Password:", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.ent_password = ttk.Entry(form_frame, show="*", width=25)
        self.ent_password.pack(fill="x", pady=(0, 5))
        
        self.lbl_pwd_hint = ttk.Label(form_frame, text="*Kosongkan password jika tidak ingin diubah", style="Sub.TLabel")
        self.lbl_pwd_hint.pack(anchor="w", pady=(0, 10))
        self.lbl_pwd_hint.pack_forget()  # Only show on update selections

        # Role widget created but not packed to remain hidden, default values are set in code
        self.ent_role = ttk.Combobox(form_frame, width=23, values=["Owner", "Kasir"])

        # Form Buttons
        self.btn_save = ttk.Button(form_frame, text="Simpan Akun", style="Success.TButton")
        self.btn_save.pack(fill="x", pady=2)
        
        self.btn_clear = ttk.Button(form_frame, text="Bersihkan Form", style="Secondary.TButton")
        self.btn_clear.pack(fill="x", pady=2)
        
        self.btn_delete = ttk.Button(form_frame, text="Hapus Akun", style="Danger.TButton")
        self.btn_delete.pack(fill="x", pady=(15, 2))

        # ------------------ RIGHT SIDE: TABLE LIST ------------------
        list_frame = ttk.Frame(self)
        list_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        columns = ("id", "username", "nama")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        self.tree.heading("id", text="ID User")
        self.tree.heading("username", text="Username")
        self.tree.heading("nama", text="Nama Lengkap")
        
        self.tree.column("id", width=80, anchor="center")
        self.tree.column("username", width=150, anchor="w")
        self.tree.column("nama", width=250, anchor="w")

        scroll = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")

    def get_inputs(self):
        return {
            "id_user": self.id_user_var.get(),
            "username": self.ent_username.get(),
            "nama": self.ent_nama.get(),
            "password": self.ent_password.get(),
            "role": self.ent_role.get()
        }

    def fill_form(self, id_val, username, nama, role):
        self.clear_form()
        self.id_user_var.set(str(id_val))
        self.ent_username.insert(0, username)
        self.ent_nama.insert(0, nama)
        self.ent_role.set(role)
        self.lbl_pwd_hint.pack(anchor="w", pady=(0, 10))

    def clear_form(self):
        self.id_user_var.set("")
        self.ent_username.delete(0, tk.END)
        self.ent_nama.delete(0, tk.END)
        self.ent_password.delete(0, tk.END)
        self.ent_role.set("Kasir")
        self.lbl_pwd_hint.pack_forget()


# =====================================================================
# SIDEBAR NAVIGATION COMPONENT
# =====================================================================

class Sidebar(ttk.Frame):
    """Left navigation panel containing action routes and links."""
    def __init__(self, parent, controller=None):
        super().__init__(parent, style="Sidebar.TFrame")
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        # App Label Header
        lbl_app = ttk.Label(self, text="RISKY KASIR", font=("Segoe UI", 14, "bold"), foreground="#ffffff", background="#0f172a")
        lbl_app.pack(padx=20, pady=(20, 5), anchor="w")
        
        lbl_sub = ttk.Label(self, text="Toko Kelontong", font=("Segoe UI", 8, "italic"), foreground="#94a3b8", background="#0f172a")
        lbl_sub.pack(padx=20, pady=(0, 20), anchor="w")

        # Divider
        divider = tk.Frame(self, bg="#334155", height=1)
        divider.pack(fill="x", padx=15, pady=(0, 15))

        # Nav Buttons list
        self.btn_dash = self.create_nav_btn("Dashboard", DashboardPage)
        self.btn_barang = self.create_nav_btn("Data Barang", BarangPage)
        self.btn_transaksi = self.create_nav_btn("Transaksi Kasir", TransaksiPage)
        self.btn_riwayat = self.create_nav_btn("Riwayat Penjualan", RiwayatPage)
        self.btn_laporan = self.create_nav_btn("Laporan Toko", LaporanPage)
        self.btn_users = self.create_nav_btn("Kelola Akun", UserPage)

        # Footer divider
        divider2 = tk.Frame(self, bg="#334155", height=1)
        divider2.pack(side="bottom", fill="x", padx=15, pady=(0, 10))

        # Logout button at bottom
        self.btn_logout = ttk.Button(self, text="Keluar Akun", style="Sidebar.TButton")
        self.btn_logout.pack(side="bottom", fill="x", padx=5, pady=(0, 10))

    def create_nav_btn(self, text, page_class):
        """Helper to create left-aligned flat sidebar buttons."""
        btn = ttk.Button(self, text=text, style="Sidebar.TButton", 
                         command=lambda: self.controller.switch_page(page_class))
        btn.pack(fill="x", padx=5, pady=2)
        return btn


# =====================================================================
# MAIN WINDOW FRAME SWITCHER CONTAINER
# =====================================================================

class MainView(tk.Tk):
    """Main Application Window."""
    def __init__(self):
        super().__init__()
        self.title("Perancangan Sistem Kasir - Toko Kelontong Risky")
        self.geometry("1024x640")
        self.minsize(980, 580)
        
        # Set icon or styling
        init_styles()
        
        # Configure layout grid
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # ------------------ SIDEBAR (LEFT) ------------------
        self.sidebar = Sidebar(self, self)
        # Hidden by default until login
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_remove()

        # ------------------ PAGES CONTAINER (RIGHT) ------------------
        self.container = ttk.Frame(self, style="Content.TFrame")
        self.container.grid(row=0, column=1, sticky="nsew")
        self.container.columnconfigure(0, weight=1)
        self.container.rowconfigure(0, weight=1)

        # Initialize all pages in container
        self.pages = {}
        for PageClass in (LoginPage, DashboardPage, BarangPage, TransaksiPage, RiwayatPage, LaporanPage, UserPage):
            page = PageClass(self.container, self)
            self.pages[PageClass] = page
            # Grid stack placement
            page.grid(row=0, column=0, sticky="nsew")

        # Setup custom Menu Bar
        self.setup_menu_bar()

        # Start with Login screen
        self.switch_page(LoginPage)

    def setup_menu_bar(self):
        """Generates standard window dropdown menu bar."""
        self.menubar = tk.Menu(self)

        # 1. File Menu
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Keluar Aplikasi", command=self.destroy)
        self.menubar.add_cascade(label="File", menu=self.file_menu)

        # 2. Navigasi Menu
        self.nav_menu = tk.Menu(self.menubar, tearoff=0)
        self.nav_menu.add_command(label="Dashboard", command=lambda: self.switch_page(DashboardPage))
        self.nav_menu.add_command(label="Data Barang", command=lambda: self.switch_page(BarangPage))
        self.nav_menu.add_command(label="Transaksi Baru", command=lambda: self.switch_page(TransaksiPage))
        self.nav_menu.add_command(label="Riwayat Penjualan", command=lambda: self.switch_page(RiwayatPage))
        self.nav_menu.add_command(label="Laporan Penjualan", command=lambda: self.switch_page(LaporanPage))
        self.nav_menu.add_command(label="Kelola Akun", command=lambda: self.switch_page(UserPage))
        self.menubar.add_cascade(label="Navigasi", menu=self.nav_menu)

        # 3. Bantuan Menu
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.help_menu.add_command(label="Info Aplikasi", command=self.show_app_info)
        self.menubar.add_cascade(label="Bantuan", menu=self.help_menu)

        self.config(menu=self.menubar)
        self.disable_nav_menu()  # Disable nav options until login

    def switch_page(self, page_class):
        """Displays the specified page class at the front of the stack (Polymorphism)."""
        # Strict MVC security role enforcement
        if page_class in (DashboardPage, BarangPage, LaporanPage, UserPage) and hasattr(self, "controller") and self.controller and getattr(self.controller, "current_user", None):
            if self.controller.current_user.role != "Owner":
                messagebox.showerror("Akses Ditolak", "Halaman ini hanya dapat diakses oleh Owner!")
                return

        page = self.pages[page_class]
        page.tkraise()
        
        # Trigger page switch callback in the main controller to refresh data
        if hasattr(self, "controller") and self.controller and hasattr(self.controller, "on_page_switch"):
            self.controller.on_page_switch(page_class)
        else:
            page.refresh_page()
        
        # Track active page highlighting in sidebar if sidebar is open
        if self.sidebar.winfo_manager() == "grid":
            self.highlight_sidebar_button(page_class)

    def highlight_sidebar_button(self, page_class):
        """Resets and highlights active button style on sidebar panel."""
        bg_dark = "#0f172a"
        bg_active = "#1e293b"
        
        # Reset all buttons
        self.sidebar.btn_dash.configure(style="Sidebar.TButton")
        self.sidebar.btn_barang.configure(style="Sidebar.TButton")
        self.sidebar.btn_transaksi.configure(style="Sidebar.TButton")
        self.sidebar.btn_riwayat.configure(style="Sidebar.TButton")
        self.sidebar.btn_laporan.configure(style="Sidebar.TButton")
        self.sidebar.btn_users.configure(style="Sidebar.TButton")

        # Highlight target
        if page_class == DashboardPage:
            self.sidebar.btn_dash.configure(background=bg_active)
        elif page_class == BarangPage:
            self.sidebar.btn_barang.configure(background=bg_active)
        elif page_class == TransaksiPage:
            self.sidebar.btn_transaksi.configure(background=bg_active)
        elif page_class == RiwayatPage:
            self.sidebar.btn_riwayat.configure(background=bg_active)
        elif page_class == LaporanPage:
            self.sidebar.btn_laporan.configure(background=bg_active)
        elif page_class == UserPage:
            self.sidebar.btn_users.configure(background=bg_active)

    def show_sidebar_by_role(self, role):
        """Shows or hides user panels depending on account credentials."""
        self.sidebar.grid()  # Show sidebar
        self.columnconfigure(0, minsize=200)
        
        if role == "Kasir":
            self.sidebar.btn_dash.pack_forget()
            self.sidebar.btn_barang.pack_forget()
            self.sidebar.btn_laporan.pack_forget()
            self.sidebar.btn_users.pack_forget()
            
            # Repack visible ones for Kasir
            self.sidebar.btn_transaksi.pack(fill="x", padx=5, pady=2)
            self.sidebar.btn_riwayat.pack(fill="x", padx=5, pady=2)
            
            self.nav_menu.entryconfig("Dashboard", state="disabled")
            self.nav_menu.entryconfig("Data Barang", state="disabled")
            self.nav_menu.entryconfig("Laporan Penjualan", state="disabled")
            self.nav_menu.entryconfig("Kelola Akun", state="disabled")
        else:
            # Repack buttons in correct order
            self.sidebar.btn_dash.pack(fill="x", padx=5, pady=2)
            self.sidebar.btn_barang.pack(fill="x", padx=5, pady=2)
            self.sidebar.btn_transaksi.pack(fill="x", padx=5, pady=2)
            self.sidebar.btn_riwayat.pack(fill="x", padx=5, pady=2)
            self.sidebar.btn_laporan.pack(fill="x", padx=5, pady=2)
            self.sidebar.btn_users.pack(fill="x", padx=5, pady=2)
            
            self.nav_menu.entryconfig("Dashboard", state="normal")
            self.nav_menu.entryconfig("Data Barang", state="normal")
            self.nav_menu.entryconfig("Laporan Penjualan", state="normal")
            self.nav_menu.entryconfig("Kelola Akun", state="normal")

    def hide_sidebar(self):
        """Hides left panel (used during logout)."""
        self.sidebar.grid_remove()
        self.columnconfigure(0, minsize=0)

    def enable_nav_menu(self):
        """Enables menu options after credentials validation."""
        self.menubar.entryconfig("Navigasi", state="normal")

    def disable_nav_menu(self):
        """Locks menu options on logout or start."""
        self.menubar.entryconfig("Navigasi", state="disabled")

    def show_app_info(self):
        """About Dialog helper."""
        messagebox.showinfo(
            "Info Aplikasi",
            "Aplikasi Sistem Kasir Toko Kelontong Risky\n"
            "Didesain dengan Tkinter & SQLite (Arsitektur MVC)\n\n"
            "Hak Cipta © 2026 - Semua Hak Dilindungi."
        )
