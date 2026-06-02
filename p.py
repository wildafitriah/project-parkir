import streamlit as st
import pandas as pd
from datetime import datetime

# =========================
# OPTIONAL MATPLOTLIB
# =========================
MATPLOTLIB_READY = True
try:
    import matplotlib.pyplot as plt
except:
    MATPLOTLIB_READY = False


# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Smart Parking System",
    page_icon="🚗",
    layout="wide"
)

# =========================
# CSS
# =========================
st.markdown("""
<style>
.main { background-color:#f5f7fb; }
.header-box {
    background:linear-gradient(90deg,#00c6ff,#0072ff);
    padding:20px;
    border-radius:15px;
    color:white;
    text-align:center;
    font-size:30px;
    font-weight:bold;
    margin-bottom:20px;
}
.metric-card {
    background:linear-gradient(135deg,#667eea,#764ba2);
    color:white;
    padding:15px;
    border-radius:12px;
    text-align:center;
}
</style>
""", unsafe_allow_html=True)


# =========================
# NODE
# =========================
class Node:
    def __init__(self, plat, jenis):
        self.plat = plat.upper()
        self.jenis = jenis
        self.jam_masuk = datetime.now()
        self.next = None


# =========================
# LINKED LIST
# =========================
class LinkedListParkir:
    def __init__(self):
        self.head = None

    def tambah(self, plat, jenis):
        new_node = Node(plat, jenis)
        if not self.head:
            self.head = new_node
            return

        temp = self.head
        while temp.next:
            temp = temp.next
        temp.next = new_node

    def cari(self, plat):
        temp = self.head
        while temp:
            if temp.plat == plat.upper():
                return temp
            temp = temp.next
        return None

    def hapus(self, plat):
        plat = plat.upper()
        if not self.head:
            return None

        if self.head.plat == plat:
            data = self.head
            self.head = self.head.next
            return data

        prev = self.head
        curr = self.head.next

        while curr:
            if curr.plat == plat:
                prev.next = curr.next
                return curr
            prev = curr
            curr = curr.next

        return None

    def tampilkan(self):
        data = []
        temp = self.head

        while temp:
            data.append({
                "Plat": temp.plat,
                "Jenis": temp.jenis,
                "Masuk": temp.jam_masuk.strftime("%d-%m-%Y %H:%M:%S")
            })
            temp = temp.next

        return data

    def sorting(self):
        return sorted(self.tampilkan(), key=lambda x: x["Plat"])


# =========================
# SESSION STATE
# =========================
if "login" not in st.session_state:
    st.session_state.login = False

if "parkir" not in st.session_state:
    st.session_state.parkir = LinkedListParkir()

if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

if "pendapatan" not in st.session_state:
    st.session_state.pendapatan = []


# =========================
# LOGIN
# =========================
if not st.session_state.login:
    st.markdown("<div class='header-box'>SMART PARKING SYSTEM</div>", unsafe_allow_html=True)

    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "admin" and pw == "123":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Login gagal")

    st.stop()


# =========================
# HEADER
# =========================
st.markdown("<div class='header-box'>SMART PARKING SYSTEM</div>", unsafe_allow_html=True)


# =========================
# SIDEBAR MENU
# =========================
menu = st.sidebar.radio(
    "Menu",
    ["Dashboard", "Masuk", "Keluar", "Cari", "Aktif", "Sorting", "Grafik", "Riwayat"]
)

TARIF = {"Motor": 2000, "Mobil": 5000}


# =========================
# DASHBOARD
# =========================
if menu == "Dashboard":

    aktif = st.session_state.parkir.tampilkan()

    st.metric("Kendaraan Aktif", len(aktif))
    st.metric("Transaksi", len(st.session_state.riwayat))
    st.metric("Pendapatan", sum(st.session_state.pendapatan))

    st.write("Sistem Parking Linked List + Streamlit")


# =========================
# MASUK
# =========================
elif menu == "Masuk":

    plat = st.text_input("Plat")
    jenis = st.selectbox("Jenis", ["Motor", "Mobil"])

    if st.button("Masuk"):
        if plat:
            if st.session_state.parkir.cari(plat):
                st.error("Sudah terdaftar")
            else:
                st.session_state.parkir.tambah(plat, jenis)
                st.success("Masuk berhasil")


# =========================
# KELUAR
# =========================
elif menu == "Keluar":

    plat = st.text_input("Plat keluar")
    metode = st.selectbox("Metode", ["Cash", "QRIS", "Transfer"])

    if st.button("Proses"):

        data = st.session_state.parkir.cari(plat)

        if not data:
            st.error("Tidak ditemukan")
        else:

            keluar = datetime.now()
            durasi = max(1, round((keluar - data.jam_masuk).total_seconds() / 3600))
            total = durasi * TARIF[data.jenis]

            st.success(f"Total: Rp {total:,}")

            st.session_state.riwayat.append({
                "Plat": data.plat,
                "Jenis": data.jenis,
                "Total": total
            })

            st.session_state.pendapatan.append(total)
            st.session_state.parkir.hapus(plat)

            st.success("Selesai")


# =========================
# CARI
# =========================
elif menu == "Cari":

    plat = st.text_input("Cari")

    if st.button("Cari"):
        data = st.session_state.parkir.cari(plat)

        if data:
            st.write(data.plat, data.jenis)
        else:
            st.error("Tidak ditemukan")


# =========================
# AKTIF
# =========================
elif menu == "Aktif":

    df = pd.DataFrame(st.session_state.parkir.tampilkan())

    st.dataframe(df if not df.empty else "Kosong")


# =========================
# SORTING
# =========================
elif menu == "Sorting":

    df = pd.DataFrame(st.session_state.parkir.sorting())
    st.dataframe(df if not df.empty else "Kosong")


# =========================
# GRAFIK
# =========================
elif menu == "Grafik":

    if st.session_state.pendapatan:

        df = pd.DataFrame({
            "x": range(len(st.session_state.pendapatan)),
            "y": st.session_state.pendapatan
        })

        if MATPLOTLIB_READY:
            fig, ax = plt.subplots()
            ax.plot(df["x"], df["y"])
            st.pyplot(fig)

    else:
        st.warning("Belum ada data")


# =========================
# RIWAYAT
# =========================
elif menu == "Riwayat":

    df = pd.DataFrame(st.session_state.riwayat)

    st.dataframe(df if not df.empty else "Kosong")

    st.download_button(
        "Download CSV",
        df.to_csv(index=False),
        file_name="riwayat.csv"
    )


# =========================
# LOGOUT
# =========================
if st.sidebar.button("Logout"):
    st.session_state.login = False
    st.rerun()