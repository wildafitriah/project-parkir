import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Sistem Parkir", page_icon="🚗", layout="wide")

# ================= LINKED LIST =================
class Node:
    def __init__(self, plat, jenis):
        self.plat = plat.upper()
        self.jenis = jenis
        self.masuk = datetime.now()
        self.next = None

class ParkirLinkedList:
    def __init__(self):
        self.head = None

    def tambah(self, plat, jenis):
        baru = Node(plat, jenis)

        if self.head is None:
            self.head = baru
            return

        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = baru

    def tampil(self):
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

                jam = max(
                    1,
                    int((keluar - cur.masuk).total_seconds() // 3600) + 1
                )

                tarif = 2000 if cur.jenis == "Motor" else 5000
                biaya = jam * tarif

                hasil = {
                    "Plat": cur.plat,
                    "Jenis": cur.jenis,
                    "Jam Masuk": cur.masuk.strftime("%d-%m-%Y %H:%M:%S"),
                    "Jam Keluar": keluar.strftime("%d-%m-%Y %H:%M:%S"),
                    "Lama Parkir (Jam)": jam,
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

# ================= SESSION =================
if "parkir" not in st.session_state:
    st.session_state.parkir = ParkirLinkedList()

if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

# ================= LOGIN =================
if "login" not in st.session_state:
    st.session_state.login = False

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

# ================= MENU =================
st.title("🚗 Sistem Parkir Linked List")

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Kendaraan Masuk",
        "Kendaraan Keluar",
        "Daftar Parkir",
        "Cari Kendaraan",
        "Sorting Plat",
        "Pendapatan"
    ]
)

if menu == "Kendaraan Masuk":

    plat = st.text_input("Plat Nomor")
    jenis = st.selectbox("Jenis Kendaraan", ["Motor", "Mobil"])

    if st.button("Tambah"):
        if plat:
            st.session_state.parkir.tambah(plat, jenis)
            st.success("Kendaraan berhasil masuk")

elif menu == "Kendaraan Keluar":

    plat = st.text_input("Plat Nomor Kendaraan")

    if st.button("Proses Pembayaran"):

        hasil = st.session_state.parkir.keluar(plat)

        if hasil:
            st.session_state.riwayat.append(hasil)

            st.success("Pembayaran Berhasil")

            st.write("### Detail Transaksi")
            st.write(hasil)

        else:
            st.error("Plat tidak ditemukan")

elif menu == "Daftar Parkir":

    data = st.session_state.parkir.tampil()

    if data:
        st.dataframe(pd.DataFrame(data), use_container_width=True)
    else:
        st.info("Parkiran kosong")

elif menu == "Cari Kendaraan":

    plat = st.text_input("Masukkan Plat")

    if st.button("Cari"):
        hasil = st.session_state.parkir.cari(plat)

        if hasil:
            st.success("Data ditemukan")
            st.write({
                "Plat": hasil.plat,
                "Jenis": hasil.jenis,
                "Jam Masuk": hasil.masuk.strftime("%d-%m-%Y %H:%M:%S")
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
