
import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="Sistem Parkir Linked List", page_icon="🚗", layout="wide")

# ===================== LINKED LIST =====================
class KendaraanNode:
    def __init__(self, plat, jenis, masuk):
        self.plat = plat.upper()
        self.jenis = jenis
        self.masuk = masuk
        self.next = None

class ParkirLinkedList:
    def __init__(self):
        self.head = None

    def tambah(self, plat, jenis):
        node = KendaraanNode(plat, jenis, datetime.now())

        if self.head is None:
            self.head = node
            return

        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = node

    def tampilkan(self):
        data = []
        cur = self.head

        while cur:
            data.append({
                "Plat": cur.plat,
                "Jenis": cur.jenis,
                "Jam Masuk": cur.masuk.strftime("%d-%m-%Y %H:%M:%S")
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
                    int((keluar - cur.masuk).total_seconds() / 3600) + 1
                )

                tarif = 2000 if cur.jenis == "Motor" else 5000
                biaya = lama * tarif

                hasil = {
                    "Plat": cur.plat,
                    "Jenis": cur.jenis,
                    "Masuk": cur.masuk.strftime("%d-%m-%Y %H:%M:%S"),
                    "Keluar": keluar.strftime("%d-%m-%Y %H:%M:%S"),
                    "Lama (Jam)": lama,
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


# ===================== PDF =====================
def buat_pdf(data, nama_file):
    doc = SimpleDocTemplate(nama_file)
    styles = getSampleStyleSheet()

    isi = [
        Paragraph("STRUK PARKIR", styles["Title"]),
        Spacer(1, 12)
    ]

    for k, v in data.items():
        isi.append(Paragraph(f"{k}: {v}", styles["Normal"]))

    doc.build(isi)


# ===================== SESSION =====================
if "login" not in st.session_state:
    st.session_state.login = False

if "parkir" not in st.session_state:
    st.session_state.parkir = ParkirLinkedList()

if "riwayat" not in st.session_state:
    st.session_state.riwayat = []


# ===================== LOGIN =====================
if not st.session_state.login:

    st.title("🔐 Login Admin")

    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "admin" and pw == "123":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Login gagal")

    st.stop()


# ===================== MENU =====================
st.title("🚗 Sistem Parkir Berbasis Linked List")

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Kendaraan Masuk",
        "Kendaraan Keluar",
        "Daftar Parkir",
        "Cari Plat",
        "Sorting Plat",
        "Grafik Pendapatan"
    ]
)

# ===================== MASUK =====================
if menu == "Kendaraan Masuk":

    st.subheader("Tambah Kendaraan")

    plat = st.text_input("Plat Nomor")

    jenis = st.selectbox(
        "Jenis Kendaraan",
        ["Motor", "Mobil"]
    )

    if st.button("Simpan"):
        if plat:
            st.session_state.parkir.tambah(plat, jenis)
            st.success("Kendaraan berhasil masuk")

# ===================== KELUAR =====================
elif menu == "Kendaraan Keluar":

    plat = st.text_input("Plat Kendaraan")

    if st.button("Proses Pembayaran"):

        hasil = st.session_state.parkir.keluar(plat)

        if hasil:

            st.session_state.riwayat.append(hasil)

            st.success("Pembayaran Berhasil")

            st.write(hasil)

            pdf_file = f"struk_{hasil['Plat']}.pdf"
            buat_pdf(hasil, pdf_file)

            with open(pdf_file, "rb") as f:
                st.download_button(
                    "Download Struk PDF",
                    f,
                    file_name=pdf_file
                )

        else:
            st.error("Plat tidak ditemukan")

# ===================== DAFTAR =====================
elif menu == "Daftar Parkir":

    data = st.session_state.parkir.tampilkan()

    if data:
        st.dataframe(pd.DataFrame(data))
    else:
        st.info("Tidak ada kendaraan")

# ===================== SEARCH =====================
elif menu == "Cari Plat":

    plat = st.text_input("Cari Plat")

    if st.button("Cari"):
        hasil = st.session_state.parkir.cari(plat)

        if hasil:
            st.success("Ditemukan")
            st.write({
                "Plat": hasil.plat,
                "Jenis": hasil.jenis,
                "Masuk": hasil.masuk.strftime("%d-%m-%Y %H:%M:%S")
            })
        else:
            st.error("Tidak ditemukan")

# ===================== SORT =====================
elif menu == "Sorting Plat":

    data = st.session_state.parkir.tampilkan()

    if data:
        df = pd.DataFrame(data)
        df = df.sort_values("Plat")
        st.dataframe(df)
    else:
        st.info("Data kosong")

# ===================== GRAFIK =====================
elif menu == "Grafik Pendapatan":

    if st.session_state.riwayat:

        df = pd.DataFrame(st.session_state.riwayat)

        fig, ax = plt.subplots()
        ax.plot(df.index + 1, df["Biaya"], marker="o")
        ax.set_title("Pendapatan per Transaksi")
        ax.set_xlabel("Transaksi")
        ax.set_ylabel("Pendapatan")

        st.pyplot(fig)

        st.metric(
            "Total Pendapatan",
            f"Rp {df['Biaya'].sum():,}"
        )

    else:
        st.info("Belum ada transaksi")
