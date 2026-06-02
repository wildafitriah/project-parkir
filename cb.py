import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from fpdf import FPDF
import base64
import io

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Sistem Parkir Pro", layout="wide", page_icon="🚗")

# --- STRUKTUR DATA LINKED LIST ---
class Node:
    def __init__(self, plat, jenis, jam_masuk):
        self.plat = plat
        self.jenis = jenis
        self.jam_masuk = jam_masuk
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def tambah(self, plat, jenis, jam_masuk):
        new_node = Node(plat, jenis, jam_masuk)
        new_node.next = self.head
        self.head = new_node

    def hapus(self, plat):
        curr = self.head
        prev = None
        while curr:
            if curr.plat == plat:
                if prev: prev.next = curr.next
                else: self.head = curr.next
                return curr
            prev = curr
            curr = curr.next
        return None

    def get_all(self):
        data = []
        curr = self.head
        while curr:
            data.append({"Plat": curr.plat, "Jenis": curr.jenis, "Masuk": curr.jam_masuk})
            curr = curr.next
        return data

# Inisialisasi State
if 'parkir' not in st.session_state: st.session_state.parkir = LinkedList()
if 'riwayat' not in st.session_state: st.session_state.riwayat = pd.DataFrame(columns=["Plat", "Jenis", "Masuk", "Keluar", "Durasi", "Total", "Metode"])
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- FUNGSI UTAMA ---
def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="STRUK PEMBAYARAN PARKIR", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    for k, v in data.items():
        pdf.cell(200, 10, txt=f"{k}: {v}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# --- UI APP ---
st.sidebar.title("🔐 Login Admin")
if not st.session_state.logged_in:
    user = st.sidebar.text_input("Username")
    pwd = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if user == "admin" and pwd == "123":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.sidebar.error("Login Gagal!")
else:
    st.sidebar.success("Logged in as Admin")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

st.title("🚗 Sistem Manajemen Parkir Pintar")

if st.session_state.logged_in:
    tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Masuk/Keluar", "Riwayat & Statistik", "Cari & Urut"])

    with tab1:
        st.subheader("Statistik Parkir")
        col1, col2, col3 = st.columns(3)
        col1.metric("Kendaraan Aktif", len(st.session_state.parkir.get_all()))
        col2.metric("Total Transaksi", len(st.session_state.riwayat))
        col3.metric("Pendapatan", f"Rp {st.session_state.riwayat['Total'].sum():,}")

    with tab2:
        with st.expander("➕ Tambah Kendaraan Masuk"):
            plat = st.text_input("Plat Nomor").upper()
            jenis = st.selectbox("Jenis", ["Motor", "Mobil"])
            if st.button("Simpan Masuk"):
                st.session_state.parkir.tambah(plat, jenis, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                st.success(f"Kendaraan {plat} berhasil masuk")

        with st.expander("➖ Kendaraan Keluar"):
            plat_out = st.text_input("Plat Nomor Keluar").upper()
            metode = st.selectbox("Metode Pembayaran", ["Cash", "QRIS", "Transfer Bank"])
            if st.button("Proses Keluar"):
                kendaraan = st.session_state.parkir.hapus(plat_out)
                if kendaraan:
                    jam_keluar = datetime.now()
                    jam_masuk = datetime.strptime(kendaraan.jam_masuk, "%Y-%m-%d %H:%M:%S")
                    durasi = max(1, int((jam_keluar - jam_masuk).total_seconds() / 3600))
                    tarif = 2000 if kendaraan.jenis == "Motor" else 5000
                    total = durasi * tarif
                    
                    # Simpan ke riwayat
                    new_row = {"Plat": plat_out, "Jenis": kendaraan.jenis, "Masuk": kendaraan.jam_masuk, 
                               "Keluar": jam_keluar.strftime("%Y-%m-%d %H:%M:%S"), "Durasi": durasi, "Total": total, "Metode": metode}
                    st.session_state.riwayat = pd.concat([st.session_state.riwayat, pd.DataFrame([new_row])], ignore_index=True)
                    
                    st.success(f"Biaya: Rp {total}. Pembayaran via {metode}")
                    pdf_data = generate_pdf(new_row)
                    st.download_button("📥 Unduh Struk", pdf_data, "struk.pdf")
                else:
                    st.error("Plat tidak ditemukan!")

    with tab3:
        st.subheader("Grafik Pendapatan")
        if not st.session_state.riwayat.empty:
            fig, ax = plt.subplots()
            st.session_state.riwayat['Total'].plot(kind='bar', ax=ax, color='skyblue')
            st.pyplot(fig)
            st.dataframe(st.session_state.riwayat)
            st.download_button("Export CSV", st.session_state.riwayat.to_csv().encode('utf-8'), "data.csv")

    with tab4:
        st.subheader("Cari & Sortir")
        search = st.text_input("Cari Plat").upper()
        df = pd.DataFrame(st.session_state.parkir.get_all())
        if search:
            st.table(df[df['Plat'].str.contains(search)])
        else:
            st.table(df.sort_values(by='Plat'))

else:
    st.warning("Silakan Login di Sidebar untuk Mengakses Sistem.")