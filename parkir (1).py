import streamlit as st
import pandas as pd
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="Sistem Parkir", page_icon="🚗", layout="wide")

# ================= LINKED LIST =================
class Node:
    def __init__(self, plat, jenis):
        self.plat = plat.upper()
        self.jenis = jenis
        self.masuk = datetime.now()
        self.next = None

class LinkedListParkir:
    def __init__(self):
        self.head = None

    def tambah(self, plat, jenis):
        node = Node(plat, jenis)

        if self.head is None:
            self.head = node
            return

        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = node

    def tampil(self):
        data = []
        cur = self.head

        while cur:
            data.append({
                "Plat": cur.plat,
                "Jenis": cur.jenis,
                "Jam Masuk": cur.masuk.strftime("%d-%m-%Y %H:%M")
            })
            cur = cur.next

        return data

    def cari(self, plat):
        cur = self.head
        while cur:
            if cur.plat == plat.upper():
                return cur
            cur = cur.next
        return None

    def keluar(self, plat):
        cur = self.head
        prev = None

        while cur:
            if cur.plat == plat.upper():

                keluar = datetime.now()

                lama = max(
                    1,
                    int((keluar - cur.masuk).total_seconds() // 3600) + 1
                )

                tarif = 2000 if cur.jenis == "Motor" else 5000
                biaya = lama * tarif

                hasil = {
                    "Plat": cur.plat,
                    "Jenis": cur.jenis,
                    "Masuk": cur.masuk.strftime("%d-%m-%Y %H:%M"),
                    "Keluar": keluar.strftime("%d-%m-%Y %H:%M"),
                    "Lama Parkir": lama,
                    "Biaya": biaya
                }

                if prev:
                    prev.next = cur.next
                else:
                    self.head = cur.next

                return hasil

            prev = cur
            cur = cur.next

        return None

# ================= PDF =================
def buat_pdf(data, nama_file):
    doc = SimpleDocTemplate(nama_file)
    styles = getSampleStyleSheet()

    isi = [Paragraph("STRUK PARKIR", styles["Title"]), Spacer(1,12)]

    for k, v in data.items():
        isi.append(Paragraph(f"{k}: {v}", styles["Normal"]))

    doc.build(isi)

# ================= SESSION =================
if "login" not in st.session_state:
    st.session_state.login = False

if "parkir" not in st.session_state:
    st.session_state.parkir = LinkedListParkir()

if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

# ================= LOGIN =================
if not st.session_state.login:
    st.title("🔐 Login Admin")

    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "admin" and pw == "123":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Username atau Password salah")

    st.stop()

# ================= MENU =================
st.title("🚗 Sistem Parkir Linked List")

menu = st.sidebar.selectbox(
    "Menu",
    ["Kendaraan Masuk",
     "Kendaraan Keluar",
     "Daftar Parkir",
     "Cari Plat",
     "Sorting Plat",
     "Pendapatan"]
)

if menu == "Kendaraan Masuk":
    st.subheader("Input Kendaraan")

    plat = st.text_input("Plat Nomor")
    jenis = st.selectbox("Jenis", ["Motor", "Mobil"])

    if st.button("Simpan"):
        if plat:
            st.session_state.parkir.tambah(plat, jenis)
            st.success("Kendaraan berhasil masuk")

elif menu == "Kendaraan Keluar":
    plat = st.text_input("Plat Nomor Kendaraan")

    if st.button("Proses Keluar"):
        hasil = st.session_state.parkir.keluar(plat)

        if hasil:
            st.session_state.riwayat.append(hasil)

            st.success("Pembayaran Berhasil")
            st.write(hasil)

            nama_pdf = f"struk_{hasil['Plat']}.pdf"
            buat_pdf(hasil, nama_pdf)

            with open(nama_pdf, "rb") as f:
                st.download_button(
                    "Download Struk PDF",
                    f,
                    file_name=nama_pdf
                )
        else:
            st.error("Plat tidak ditemukan")

elif menu == "Daftar Parkir":
    data = st.session_state.parkir.tampil()

    if data:
        st.dataframe(pd.DataFrame(data), use_container_width=True)
    else:
        st.info("Parkiran kosong")

elif menu == "Cari Plat":
    plat = st.text_input("Masukkan Plat")

    if st.button("Cari"):
        hasil = st.session_state.parkir.cari(plat)

        if hasil:
            st.success("Data ditemukan")
            st.write({
                "Plat": hasil.plat,
                "Jenis": hasil.jenis,
                "Jam Masuk": hasil.masuk.strftime("%d-%m-%Y %H:%M")
            })
        else:
            st.error("Data tidak ditemukan")

elif menu == "Sorting Plat":
    data = st.session_state.parkir.tampil()

    if data:
        df = pd.DataFrame(data)
        df = df.sort_values("Plat")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Belum ada data")

elif menu == "Pendapatan":
    total = sum(x["Biaya"] for x in st.session_state.riwayat)

    st.metric("Total Pendapatan", f"Rp {total:,}")
    st.metric("Jumlah Transaksi", len(st.session_state.riwayat))

    if st.session_state.riwayat:
        df = pd.DataFrame(st.session_state.riwayat)
        st.line_chart(df["Biaya"])
