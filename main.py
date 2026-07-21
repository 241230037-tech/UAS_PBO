import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime

# Import layers (MVC Architecture)
from model import (
    Database, 
    UserManager, 
    BarangManager, 
    TransaksiManager, 
    User, 
    Barang, 
    Transaksi, 
    DetailTransaksi, 
    DatabaseError
)
from view import (
    MainView, 
    LoginPage, 
    DashboardPage, 
    BarangPage, 
    TransaksiPage, 
    RiwayatPage, 
    LaporanPage, 
    UserPage
)

# Helper function for currency formatting (Rupiah)
def format_rupiah(amount):
    try:
        val = float(amount)
        formatted = f"{val:,.0f}".replace(",", ".")
        return f"Rp {formatted}"
    except (ValueError, TypeError):
        return "Rp 0"

class Controller:
    """The Controller acts as the bridge connecting Model and View (Strict MVC)."""
    def __init__(self):
        # 1. Initialize Model Database and Managers
        try:
            self.db = Database()
            self.user_mgr = UserManager(self.db)
            self.barang_mgr = BarangManager(self.db)
            self.tx_mgr = TransaksiManager(self.db)
        except DatabaseError as e:
            messagebox.showerror("Error Database", f"Fatal: Gagal inisialisasi database!\n{e}")
            exit(1)

        # 2. State management variables
        self.current_user = None
        self.cart_items = {}  # format: {id_barang: DetailTransaksi}

        # 3. Initialize View Window
        self.view = MainView()
        self.view.controller = self  # Give MainView a pointer back to this controller

        # 4. Bind visual event callbacks to controller actions
        self.bind_events()

        # 5. Start Application mainloop
        self.view.mainloop()

    def on_page_switch(self, page_class):
        """
        Invoked by the View polymorphically whenever a frame is raised.
        Acts as the central router.
        """
        if not self.current_user and page_class != LoginPage:
            # Enforce login state redirection
            self.view.switch_page(LoginPage)
            return

        try:
            if page_class == DashboardPage:
                self.refresh_dashboard()
            elif page_class == BarangPage:
                self.refresh_barang()
            elif page_class == TransaksiPage:
                self.refresh_transaksi()
            elif page_class == RiwayatPage:
                self.refresh_riwayat()
            elif page_class == LaporanPage:
                self.refresh_laporan()
            elif page_class == UserPage:
                self.refresh_users()
        except DatabaseError as e:
            messagebox.showerror("Error Database", f"Terjadi kesalahan saat memuat data: {e}")
        except Exception as e:
            messagebox.showerror("Error Aplikasi", f"Gagal memuat halaman: {e}")

    def bind_events(self):
        """Establishes listeners between UI widgets and actions."""
        # --- LOGIN PAGE ---
        login_pg = self.view.pages[LoginPage]
        login_pg.btn_login.configure(command=self.handle_login)

        # --- SIDEBAR & MENU BAR ---
        self.view.sidebar.btn_logout.configure(command=self.handle_logout)
        self.view.file_menu.entryconfig("Keluar Aplikasi", command=self.handle_app_exit)

        # --- BARANG PAGE ---
        brg_pg = self.view.pages[BarangPage]
        brg_pg.btn_save.configure(command=self.handle_save_barang)
        brg_pg.btn_clear.configure(command=self.handle_clear_barang)
        brg_pg.btn_delete.configure(command=self.handle_delete_barang)
        brg_pg.btn_search.configure(command=self.handle_search_barang)
        brg_pg.tree.bind("<<TreeviewSelect>>", self.handle_select_barang)

        # --- USER PAGE ---
        usr_pg = self.view.pages[UserPage]
        usr_pg.btn_save.configure(command=self.handle_save_user)
        usr_pg.btn_clear.configure(command=self.handle_clear_user)
        usr_pg.btn_delete.configure(command=self.handle_delete_user)
        usr_pg.tree.bind("<<TreeviewSelect>>", self.handle_select_user)

        # --- TRANSAKSI PAGE (KASIR) ---
        tx_pg = self.view.pages[TransaksiPage]
        tx_pg.btn_search_prod.configure(command=self.handle_search_product_cashier)
        tx_pg.ent_search_prod.bind("<Return>", lambda e: self.handle_search_product_cashier())
        tx_pg.tree_prod.bind("<Double-1>", self.handle_add_to_cart)
        tx_pg.btn_remove_cart.configure(command=self.handle_remove_from_cart)
        tx_pg.btn_edit_qty.configure(command=self.handle_edit_qty_cart)
        tx_pg.btn_pay.configure(command=self.handle_checkout_transaction)
        tx_pg.btn_reset_tx.configure(command=self.handle_cancel_transaction)
        tx_pg.ent_bayar.bind("<KeyRelease>", self.handle_recalculate_change)

        # --- RIWAYAT PAGE ---
        riw_pg = self.view.pages[RiwayatPage]
        riw_pg.tree_tx.bind("<<TreeviewSelect>>", self.handle_select_riwayat_tx)

        # --- LAPORAN PAGE ---
        lap_pg = self.view.pages[LaporanPage]
        lap_pg.btn_filter.configure(command=self.handle_filter_laporan)


    # =====================================================================
    # 1. LOGIN & LOGOUT ROUTINES
    # =====================================================================
    
    def handle_login(self):
        login_pg = self.view.pages[LoginPage]
        username = login_pg.ent_user.get().strip()
        password = login_pg.ent_pass.get().strip()

        if not username or not password:
            messagebox.showwarning("Peringatan", "Username dan Password wajib diisi!")
            return

        try:
            user = self.user_mgr.authenticate(username, password)
            if user:
                self.current_user = user
                messagebox.showinfo("Login Sukses", f"Selamat datang kembali, {user.nama} ({user.role})!")
                
                # Show appropriate screens and menus
                self.view.show_sidebar_by_role(user.role)
                self.view.enable_nav_menu()
                
                # Redirect based on role
                if user.role == "Owner":
                    self.view.switch_page(DashboardPage)
                else:
                    self.view.switch_page(TransaksiPage)
                login_pg.clear_inputs()
            else:
                messagebox.showerror("Gagal Masuk", "Username atau Password salah!")
                login_pg.ent_pass.delete(0, tk.END)
                login_pg.ent_pass.focus_set()
        except DatabaseError as e:
            messagebox.showerror("Error Database", f"Gagal memverifikasi login:\n{e}")

    def handle_logout(self):
        confirm = messagebox.askyesno("Konfirmasi Keluar", "Apakah Anda yakin ingin keluar dari akun?")
        if confirm:
            self.current_user = None
            self.cart_items.clear()
            self.view.hide_sidebar()
            self.view.disable_nav_menu()
            self.view.switch_page(LoginPage)

    def handle_app_exit(self):
        confirm = messagebox.askyesno("Keluar Aplikasi", "Keluar dari sistem kasir?")
        if confirm:
            self.view.destroy()


    # =====================================================================
    # 2. DASHBOARD DATA
    # =====================================================================

    def refresh_dashboard(self):
        dash_pg = self.view.pages[DashboardPage]

        # 1. Fetch metrics
        tot_barang = self.barang_mgr.get_total_count()
        tot_transaksi = self.tx_mgr.get_total_count()
        income_today = self.tx_mgr.get_income_today()
        low_stock_items = self.barang_mgr.get_low_stock(limit=5)
        
        # 2. Update metric labels
        dash_pg.card_barang.configure(text=str(tot_barang))
        dash_pg.card_transaksi.configure(text=str(tot_transaksi))
        dash_pg.card_pendapatan.configure(text=format_rupiah(income_today))
        dash_pg.card_alert.configure(text=f"{len(low_stock_items)} Item")

        # 3. Populate warning table
        dash_pg.tree_warn.delete(*dash_pg.tree_warn.get_children())
        for b in low_stock_items:
            dash_pg.tree_warn.insert(
                "", "end",
                values=(b.id_barang, b.nama_barang, b.kategori, format_rupiah(b.harga), f"{b.stok} Unit")
            )


    # =====================================================================
    # 3. BARANG DATA CRUD (OOP: Polymorphism & Encapsulation)
    # =====================================================================

    def refresh_barang(self):
        brg_pg = self.view.pages[BarangPage]
        
        # Load all barang list
        items = self.barang_mgr.get_all()
        self.populate_barang_tree(items)

        # Clear form inputs & lock generated ID
        brg_pg.clear_form()
        next_id = self.barang_mgr.generate_next_id()
        brg_pg.ent_id.insert(0, next_id)

    def populate_barang_tree(self, items):
        brg_pg = self.view.pages[BarangPage]
        brg_pg.tree.delete(*brg_pg.tree.get_children())
        for b in items:
            brg_pg.tree.insert(
                "", "end",
                values=(b.id_barang, b.nama_barang, b.kategori, format_rupiah(b.harga), b.stok)
            )

    def handle_search_barang(self):
        brg_pg = self.view.pages[BarangPage]
        q = brg_pg.ent_search.get().strip()
        if not q:
            # If empty search query, reload all
            items = self.barang_mgr.get_all()
        else:
            items = self.barang_mgr.search(q)
        self.populate_barang_tree(items)

    def handle_select_barang(self, event):
        brg_pg = self.view.pages[BarangPage]
        sel = brg_pg.tree.selection()
        if not sel:
            return
        
        row_vals = brg_pg.tree.item(sel[0], "values")
        # Format values
        id_val = row_vals[0]
        nama = row_vals[1]
        kategori = row_vals[2]
        
        # Clean currency format back to float numbers
        harga_clean = row_vals[3].replace("Rp ", "").replace(".", "").replace(",", ".")
        stok = row_vals[4]
        
        brg_pg.fill_form(id_val, nama, kategori, harga_clean, stok)

    def handle_save_barang(self):
        brg_pg = self.view.pages[BarangPage]
        inputs = brg_pg.get_inputs()

        # Validate entries
        try:
            # OOP Encapsulation/Validation: let Barang class validate properties on assignment
            b = Barang(
                id_barang=inputs["id_barang"],
                nama_barang=inputs["nama_barang"],
                kategori=inputs["kategori"],
                harga=inputs["harga"],
                stok=inputs["stok"]
            )
        except ValueError as e:
            messagebox.showwarning("Input Tidak Valid", str(e))
            return

        try:
            # Check if this is a CREATE or an UPDATE (ID entry state)
            # Use a robust check since Ttk state representation varies by platform
            is_new = ("disabled" not in str(brg_pg.ent_id.cget("state")))
            
            if is_new:
                # Check duplication
                existing = self.barang_mgr.get_by_id(b.id_barang)
                if existing:
                    messagebox.showerror("Error Duplikasi", f"ID Barang '{b.id_barang}' sudah terdaftar di database!")
                    return
                self.barang_mgr.create(b)
                messagebox.showinfo("Sukses", f"Barang '{b.nama_barang}' berhasil ditambahkan!")
            else:
                self.barang_mgr.update(b)
                messagebox.showinfo("Sukses", f"Detail barang '{b.nama_barang}' berhasil diperbarui!")

            self.refresh_barang()
        except DatabaseError as e:
            messagebox.showerror("Database Error", f"Gagal menyimpan data barang:\n{e}")

    def handle_clear_barang(self):
        self.refresh_barang()

    def handle_delete_barang(self):
        brg_pg = self.view.pages[BarangPage]
        sel = brg_pg.tree.selection()
        if not sel:
            messagebox.showwarning("Peringatan", "Silakan pilih barang yang ingin dihapus dari tabel!")
            return
        
        row_vals = brg_pg.tree.item(sel[0], "values")
        id_barang = row_vals[0]
        nama_barang = row_vals[1]

        confirm = messagebox.askyesno("Konfirmasi Hapus", f"Apakah Anda yakin ingin menghapus '{nama_barang}' ({id_barang})?")
        if confirm:
            try:
                self.barang_mgr.delete(id_barang)
                messagebox.showinfo("Sukses", "Barang berhasil dihapus dari sistem.")
                self.refresh_barang()
            except DatabaseError as e:
                messagebox.showerror("Database Error", f"Gagal menghapus barang:\n{e}")


    # =====================================================================
    # 4. USER MANAGER CRUD
    # =====================================================================

    def refresh_users(self):
        usr_pg = self.view.pages[UserPage]
        usr_pg.clear_form()
        
        # Load user list
        users = self.user_mgr.get_all()
        usr_pg.tree.delete(*usr_pg.tree.get_children())
        for u in users:
            usr_pg.tree.insert(
                "", "end",
                values=(u.id_user, u.username, u.nama, u.role)
            )

    def handle_select_user(self, event):
        usr_pg = self.view.pages[UserPage]
        sel = usr_pg.tree.selection()
        if not sel:
            return
        
        vals = usr_pg.tree.item(sel[0], "values")
        id_val = vals[0]
        username = vals[1]
        nama = vals[2]
        role = vals[3]
        
        usr_pg.fill_form(id_val, username, nama, role)

    def handle_save_user(self):
        usr_pg = self.view.pages[UserPage]
        inputs = usr_pg.get_inputs()
        
        # Encapsulation validation
        try:
            # Temporary password validation on create
            is_update = bool(inputs["id_user"])
            if not is_update and not inputs["password"].strip():
                raise ValueError("Password wajib diisi untuk pengguna baru!")
                
            u = User(
                username=inputs["username"],
                password=inputs["password"] if not is_update else "",  # Checked separately on update
                nama=inputs["nama"],
                role=inputs["role"],
                id_user=inputs["id_user"] if is_update else None
            )
        except ValueError as e:
            messagebox.showwarning("Input Tidak Valid", str(e))
            return

        try:
            if not is_update:
                # Save new user
                u.password = inputs["password"]  # Put raw for manager hashing
                self.user_mgr.create(u)
                messagebox.showinfo("Sukses", f"Akun '{u.username}' berhasil dibuat!")
            else:
                # Update user
                u_pw = inputs["password"] if inputs["password"].strip() else None
                self.user_mgr.update(u, new_password=u_pw)
                messagebox.showinfo("Sukses", f"Akun '{u.username}' berhasil diperbarui!")
            
            self.refresh_users()
        except DatabaseError as e:
            messagebox.showerror("Database Error", f"Gagal menyimpan akun:\n{e}")

    def handle_clear_user(self):
        self.refresh_users()

    def handle_delete_user(self):
        usr_pg = self.view.pages[UserPage]
        sel = usr_pg.tree.selection()
        if not sel:
            messagebox.showwarning("Peringatan", "Pilih akun yang ingin dihapus!")
            return
        
        vals = usr_pg.tree.item(sel[0], "values")
        id_user = vals[0]
        username = vals[1]

        # Prevent suicide delete
        if int(id_user) == self.current_user.id_user:
            messagebox.showerror("Error Akses", "Anda tidak dapat menghapus akun Anda sendiri!")
            return

        confirm = messagebox.askyesno("Konfirmasi Hapus", f"Hapus akun '{username}'?")
        if confirm:
            try:
                self.user_mgr.delete(id_user)
                messagebox.showinfo("Sukses", f"Akun '{username}' berhasil dihapus.")
                self.refresh_users()
            except DatabaseError as e:
                messagebox.showerror("Database Error", f"Gagal menghapus akun:\n{e}")


    # =====================================================================
    # 5. TRANSAKSI (POS KASIR) HANDLERS
    # =====================================================================

    def refresh_transaksi(self):
        tx_pg = self.view.pages[TransaksiPage]
        
        # Reset Invoice Code
        next_invoice = self.tx_mgr.generate_next_id()
        tx_pg.lbl_invoice.configure(text=next_invoice)

        # Set cashier label
        tx_pg.lbl_kasir.configure(text=self.current_user.nama)

        # Reset states
        self.cart_items.clear()
        tx_pg.ent_pelanggan.configure(state="normal")
        tx_pg.ent_pelanggan.delete(0, tk.END)
        tx_pg.ent_pelanggan.insert(0, self.current_user.nama)
        tx_pg.ent_pelanggan.configure(state="disabled")
        tx_pg.ent_bayar.delete(0, tk.END)
        tx_pg.lbl_kembali.configure(text="Rp 0", foreground="#16a34a")
        tx_pg.ent_search_prod.delete(0, tk.END)

        # Load all products for searching
        self.refresh_cashier_product_list()
        self.update_cart_view()

    def refresh_cashier_product_list(self, query=None):
        tx_pg = self.view.pages[TransaksiPage]
        tx_pg.tree_prod.delete(*tx_pg.tree_prod.get_children())
        
        if query:
            items = self.barang_mgr.search(query)
        else:
            items = self.barang_mgr.get_all()

        for b in items:
            tx_pg.tree_prod.insert(
                "", "end",
                values=(b.id_barang, b.nama_barang, format_rupiah(b.harga), b.stok)
            )

    def handle_search_product_cashier(self):
        tx_pg = self.view.pages[TransaksiPage]
        q = tx_pg.ent_search_prod.get().strip()
        self.refresh_cashier_product_list(query=q)

    def handle_add_to_cart(self, event):
        tx_pg = self.view.pages[TransaksiPage]
        sel = tx_pg.tree_prod.selection()
        if not sel:
            return
        
        row = tx_pg.tree_prod.item(sel[0], "values")
        id_barang = row[0]
        nama_barang = row[1]
        harga_clean = float(row[2].replace("Rp ", "").replace(".", "").replace(",", "."))
        stok_avail = int(row[3])

        if stok_avail <= 0:
            messagebox.showwarning("Stok Habis", f"Stok untuk '{nama_barang}' habis! Silakan lakukan pengadaan barang.")
            return

        # Check cart thresholds
        if id_barang in self.cart_items:
            det = self.cart_items[id_barang]
            if det.jumlah + 1 > stok_avail:
                messagebox.showwarning("Stok Kurang", f"Batas stok tercapai. Maksimum pembelian: {stok_avail} unit.")
                return
            det.jumlah += 1
            det.subtotal = det.jumlah * harga_clean
        else:
            det = DetailTransaksi(
                id_barang=id_barang,
                jumlah=1,
                subtotal=harga_clean,
                nama_barang=nama_barang
            )
            self.cart_items[id_barang] = det

        self.update_cart_view()

    def update_cart_view(self):
        tx_pg = self.view.pages[TransaksiPage]
        tx_pg.tree_cart.delete(*tx_pg.tree_cart.get_children())
        
        total_price = 0.0
        for item in self.cart_items.values():
            # Get original item single price
            unit_price = item.subtotal / item.jumlah
            tx_pg.tree_cart.insert(
                "", "end",
                values=(item.id_barang, item.nama_barang, format_rupiah(unit_price), item.jumlah, format_rupiah(item.subtotal))
            )
            total_price += item.subtotal

        # Set Large Total Belanja Text
        tx_pg.lbl_total.configure(text=format_rupiah(total_price))
        self.handle_recalculate_change(None)

    def handle_remove_from_cart(self):
        tx_pg = self.view.pages[TransaksiPage]
        sel = tx_pg.tree_cart.selection()
        if not sel:
            messagebox.showwarning("Peringatan", "Pilih item keranjang yang ingin dihapus!")
            return
        
        row = tx_pg.tree_cart.item(sel[0], "values")
        id_barang = row[0]
        
        if id_barang in self.cart_items:
            del self.cart_items[id_barang]
            self.update_cart_view()

    def handle_edit_qty_cart(self):
        tx_pg = self.view.pages[TransaksiPage]
        sel = tx_pg.tree_cart.selection()
        if not sel:
            messagebox.showwarning("Peringatan", "Pilih item keranjang yang ingin diubah kuantitasnya!")
            return
        
        row = tx_pg.tree_cart.item(sel[0], "values")
        id_barang = row[0]
        nama_barang = row[1]
        curr_qty = int(row[3])

        # Get maximum stock limit
        b_info = self.barang_mgr.get_by_id(id_barang)
        if not b_info:
            return
        max_stock = b_info.stok

        new_qty = simpledialog.askinteger(
            "Ubah Jumlah Qty",
            f"Masukkan jumlah kuantitas untuk '{nama_barang}' (Stok tersedia: {max_stock}):",
            initialvalue=curr_qty,
            minvalue=1,
            maxvalue=max_stock
        )
        
        if new_qty is not None:
            det = self.cart_items[id_barang]
            det.jumlah = new_qty
            det.subtotal = new_qty * b_info.harga
            self.update_cart_view()

    def handle_recalculate_change(self, event):
        tx_pg = self.view.pages[TransaksiPage]
        
        # Calculate totals
        total = 0.0
        for item in self.cart_items.values():
            total += item.subtotal

        # Parse Bayar
        bayar_str = tx_pg.ent_bayar.get().strip()
        if not bayar_str:
            tx_pg.lbl_kembali.configure(text="Rp 0", foreground="#64748b")
            return
        
        try:
            bayar = float(bayar_str)
            kembalian = bayar - total
            tx_pg.lbl_kembali.configure(text=format_rupiah(kembalian))
            if kembalian < 0:
                tx_pg.lbl_kembali.configure(foreground="#dc2626")  # Danger Red
            else:
                tx_pg.lbl_kembali.configure(foreground="#16a34a")  # Success Green
        except ValueError:
            tx_pg.lbl_kembali.configure(text="Input salah", foreground="#dc2626")

    def handle_cancel_transaction(self):
        confirm = messagebox.askyesno("Konfirmasi", "Batalkan transaksi yang sedang berjalan?")
        if confirm:
            self.refresh_transaksi()

    def handle_checkout_transaction(self):
        tx_pg = self.view.pages[TransaksiPage]
        
        invoice = tx_pg.lbl_invoice.cget("text")
        pelanggan = tx_pg.ent_pelanggan.get().strip()
        kasir = self.current_user.nama
        
        if not self.cart_items:
            messagebox.showwarning("Keranjang Kosong", "Tambahkan barang terlebih dahulu sebelum bayar!")
            return
        
        if not pelanggan:
            messagebox.showwarning("Input Kurang", "Nama pelanggan harus diisi!")
            return

        # Recalculate totals
        total = sum(item.subtotal for item in self.cart_items.values())
        
        # Validate Bayar Input
        bayar_str = tx_pg.ent_bayar.get().strip()
        if not bayar_str:
            messagebox.showwarning("Pembayaran Kurang", "Nominal bayar wajib diinput!")
            return
        
        try:
            bayar = float(bayar_str)
            if bayar < total:
                messagebox.showwarning("Pembayaran Kurang", f"Uang bayar kurang! Total belanja: {format_rupiah(total)}")
                return
            kembalian = bayar - total
        except ValueError:
            messagebox.showerror("Input Salah", "Nominal bayar harus berupa angka!")
            return

        # Prepare transaction payload (OOP encapsulation)
        try:
            tx = Transaksi(
                id_transaksi=invoice,
                pelanggan=pelanggan,
                kasir=kasir,
                total=total,
                bayar=bayar,
                kembalian=kembalian,
                details=list(self.cart_items.values())
            )
            
            # Commit to SQLite
            self.tx_mgr.create(tx)
            
            # Show receipt and notification
            receipt_msg = (
                f"=== INVOICE TRANSAKSI ===\n"
                f"Invoice : {invoice}\n"
                f"Pelanggan: {pelanggan}\n"
                f"Kasir : {kasir}\n"
                f"-----------------------------------------\n"
                f"Total : {format_rupiah(total)}\n"
                f"Bayar : {format_rupiah(bayar)}\n"
                f"Kembali : {format_rupiah(kembalian)}\n"
                f"-----------------------------------------\n"
                f"Pembayaran Sukses!"
            )
            messagebox.showinfo("Transaksi Sukses", receipt_msg)
            
            # Reset page
            self.refresh_transaksi()
        except ValueError as e:
            messagebox.showwarning("Gagal Checkout", str(e))
        except DatabaseError as e:
            messagebox.showerror("Database Error", f"Checkout transaksi gagal diproses database:\n{e}")


    # =====================================================================
    # 6. RIWAYAT TRANSAKSI PAGE
    # =====================================================================

    def refresh_riwayat(self):
        riw_pg = self.view.pages[RiwayatPage]
        riw_pg.tree_tx.delete(*riw_pg.tree_tx.get_children())
        riw_pg.tree_det.delete(*riw_pg.tree_det.get_children())

        # Load all history
        txs = self.tx_mgr.get_all()
        for t in txs:
            riw_pg.tree_tx.insert(
                "", "end",
                values=(t.id_transaksi, t.tanggal, t.kasir, format_rupiah(t.total), format_rupiah(t.bayar), format_rupiah(t.kembalian))
            )

    def handle_select_riwayat_tx(self, event):
        riw_pg = self.view.pages[RiwayatPage]
        sel = riw_pg.tree_tx.selection()
        if not sel:
            return
        
        row = riw_pg.tree_tx.item(sel[0], "values")
        invoice_id = row[0]

        # Load details
        try:
            details = self.tx_mgr.get_details(invoice_id)
            riw_pg.tree_det.delete(*riw_pg.tree_det.get_children())
            for d in details:
                # Calc single price unit
                u_price = d.subtotal / d.jumlah
                riw_pg.tree_det.insert(
                    "", "end",
                    values=(d.id_barang, d.nama_barang, format_rupiah(u_price), d.jumlah, format_rupiah(d.subtotal))
                )
        except DatabaseError as e:
            messagebox.showerror("Database Error", f"Gagal memuat rincian invoice:\n{e}")


    # =====================================================================
    # 7. LAPORAN PAGE HANDLERS
    # =====================================================================

    def refresh_laporan(self):
        # Default load: call filter reporting on default entries dates
        self.handle_filter_laporan()

    def handle_filter_laporan(self):
        lap_pg = self.view.pages[LaporanPage]
        start = lap_pg.ent_start.get().strip()
        end = lap_pg.ent_end.get().strip()

        # Validate date formats YYYY-MM-DD
        for d_str, label in ((start, "Mulai Tanggal"), (end, "Sampai Tanggal")):
            try:
                datetime.strptime(d_str, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Format Tanggal Salah", f"Format {label} '{d_str}' tidak valid! Gunakan format YYYY-MM-DD (contoh: 2026-07-01).")
                return

        try:
            # Query totals
            income, qty = self.tx_mgr.get_revenue_summary(start, end)
            
            # Update metric visual cards
            lap_pg.card_omset.configure(text=format_rupiah(income))
            lap_pg.card_qty.configure(text=f"{qty} Unit")

            # Load report transactions table
            rows = self.tx_mgr.get_report_data(start, end)
            lap_pg.tree_rep.delete(*lap_pg.tree_rep.get_children())
            for r in rows:
                lap_pg.tree_rep.insert(
                    "", "end",
                    values=(r.id_transaksi, r.tanggal, r.kasir, format_rupiah(r.total))
                )
        except DatabaseError as e:
            messagebox.showerror("Database Error", f"Gagal menghasilkan laporan:\n{e}")


# =====================================================================
# MAIN THREAD INITIALIZATION
# =====================================================================

if __name__ == "__main__":
    # Start MVC Application Controller
    Controller()
