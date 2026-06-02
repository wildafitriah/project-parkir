import streamlit as st
import pandas as pd

try:
    import matplotlib.pyplot as plt
except Exception as e:
    st.error(f"Matplotlib Error: {e}")

from datetime import datetime

# =====================================================
# KONFIGURASI HALAMAN
# =====================================================

st.set_page_config(
    page_title="Smart Parking System",
    page_icon="🚗",
    layout="wide"
)

# =====================================================
# CSS CUSTOM
# =====================================================

st.markdown("""
<style>

.main{
    background-color:#f5f7fb;
}

.big-title{
    text-align:center;
    font-size:40px;
    font-weight:bold;
    color:white;
}

.header-box{
    background:linear-gradient(90deg,#00c6ff,#0072ff);
    padding:25px;
    border-radius:15px;
    margin-bottom:20px;
}

.card{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0px 0px 10px rgba(0,0,0,0.1);
}

.metric-card{
    background:linear-gradient(135deg,#667eea,#764ba2);
    color:white;
    padding:20px;
    border-radius:15px;
    text-align:center;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# NODE LINKED LIST
# =====================================================

class Node:

    def __init__(self, plat, jenis):

        self.plat = plat.upper()
        self.jenis = jenis

        self.jam_masuk = datetime.now()

        self.next = None

# =====================================================
# LINKED LIST PARKIR
# =====================================================

class LinkedListParkir:

    def __init__(self):

        self.head = None

    # =====================================
    # TAMBAH DATA
    # =====================================

    def tambah_kendaraan(self, plat, jenis):

        baru = Node(plat, jenis)

        if self.head is None:

            self.head = baru
            return

        temp = self.head

        while temp.next:

            temp = temp.next

        temp.next = baru

    # =====================================
    # CARI PLAT
    # =====================================

    def cari_kendaraan(self, plat):

        temp = self.head

        while temp:

            if temp.plat == plat.upper():
                return temp

            temp = temp.next

        return None

    # =====================================
    # HAPUS KENDARAAN
    # =====================================

    def hapus_kendaraan(self, plat):

        plat = plat.upper()

        if self.head is None:
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

    # =====================================
    # TAMPILKAN SEMUA
    # =====================================

    def tampilkan_semua(self):

        hasil = []

        temp = self.head

        while temp:

            hasil.append({

                "Plat": temp.plat,
                "Jenis": temp.jenis,
                "Masuk": temp.jam_masuk.strftime(
                    "%d-%m-%Y %H:%M:%S"
                )

            })

            temp = temp.next

        return hasil

    # =====================================
    # SORTING
    # =====================================

    def sorting_plat(self):

        data = self.tampilkan_semua()

        return sorted(
            data,
            key=lambda x: x["Plat"]
        )

# =====================================================
# SESSION STATE
# =====================================================

if "login" not in st.session_state:

    st.session_state.login = False

if "parkir" not in st.session_state:

    st.session_state.parkir = LinkedListParkir()

if "riwayat" not in st.session_state:

    st.session_state.riwayat = []

if "pendapatan" not in st.session_state:

    st.session_state.pendapatan = []

# =====================================================
# LOGIN ADMIN
# =====================================================

if not st.session_state.login:

    st.markdown("""
    <div class='header-box'>
        <div class='big-title'>
            🚗 SMART PARKING SYSTEM
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1,col2,col3 = st.columns([1,2,1])

    with col2:

        st.info(
            "Silakan Login Sebagai Admin"
        )

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button(
            "🔐 LOGIN",
            use_container_width=True
        ):

            if (
                username == "admin"
                and
                password == "123"
            ):

                st.session_state.login = True

                st.success(
                    "Login Berhasil"
                )

                st.rerun()

            else:

                st.error(
                    "Username atau Password Salah"
                )

    st.stop()

# =====================================================
# HEADER UTAMA
# =====================================================

st.markdown("""
<div class='header-box'>
<div class='big-title'>
🚗 SMART PARKING SYSTEM
</div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/744/744465.png",
    width=120
)

st.sidebar.success(
    "Admin Login"
)

menu = st.sidebar.radio(

    "📋 MENU",

    [

        "Dashboard",

        "Kendaraan Masuk",

        "Kendaraan Keluar",

        "Cari Kendaraan",

        "Kendaraan Aktif",

        "Sorting Plat",

        "Grafik Pendapatan",

        "Riwayat Transaksi"

    ]

)

# =====================================================
# TARIF PARKIR
# =====================================================

TARIF = {

    "Motor": 2000,
    "Mobil": 5000

}

# =====================================================
# DASHBOARD
# =====================================================

if menu == "Dashboard":

    total_aktif = len(
        st.session_state.parkir.tampilkan_semua()
    )

    total_transaksi = len(
        st.session_state.riwayat
    )

    total_pendapatan = sum(
        st.session_state.pendapatan
    )

    col1,col2,col3 = st.columns(3)

    with col1:

        st.markdown(f"""
        <div class='metric-card'>
        <h2>🚗</h2>
        <h3>{total_aktif}</h3>
        <p>Kendaraan Aktif</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown(f"""
        <div class='metric-card'>
        <h2>🧾</h2>
        <h3>{total_transaksi}</h3>
        <p>Total Transaksi</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown(f"""
        <div class='metric-card'>
        <h2>💰</h2>
        <h3>Rp {total_pendapatan:,.0f}</h3>
        <p>Pendapatan</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.subheader(
        "📊 Informasi Sistem"
    )

    st.write(
        """
        Sistem ini menggunakan:

        ✔ Linked List

        ✔ Searching

        ✔ Sorting

        ✔ PDF Report

        ✔ Grafik Pendapatan

        ✔ Streamlit Dashboard

        ✔ Metode Pembayaran Cash, QRIS dan Transfer
        """
    )
    # =====================================================
# KENDARAAN MASUK
# =====================================================

elif menu == "Kendaraan Masuk":

    st.subheader("🚘 Input Kendaraan Masuk")

    col1, col2 = st.columns(2)

    with col1:

        plat = st.text_input(
            "Plat Nomor",
            placeholder="Contoh : B1234ABC"
        )

    with col2:

        jenis = st.selectbox(
            "Jenis Kendaraan",
            [
                "Motor",
                "Mobil"
            ]
        )

    st.markdown("### 💳 Tarif Parkir")

    tarif_col1, tarif_col2 = st.columns(2)

    with tarif_col1:

        st.info(
            f"🏍️ Motor : Rp {TARIF['Motor']:,}/Jam"
        )

    with tarif_col2:

        st.info(
            f"🚗 Mobil : Rp {TARIF['Mobil']:,}/Jam"
        )

    if st.button(
        "✅ Tambahkan Kendaraan",
        use_container_width=True
    ):

        if plat == "":

            st.warning(
                "Plat nomor harus diisi."
            )

        else:

            cek = st.session_state.parkir.cari_kendaraan(
                plat
            )

            if cek:

                st.error(
                    "Plat nomor sudah terdaftar!"
                )

            else:

                st.session_state.parkir.tambah_kendaraan(
                    plat,
                    jenis
                )

                st.success(
                    f"Kendaraan {plat.upper()} berhasil masuk."
                )

# =====================================================
# CARI KENDARAAN
# =====================================================

elif menu == "Cari Kendaraan":

    st.subheader("🔍 Pencarian Kendaraan")

    plat_cari = st.text_input(
        "Masukkan Plat Nomor"
    )

    if st.button(
        "Cari Sekarang"
    ):

        hasil = st.session_state.parkir.cari_kendaraan(
            plat_cari
        )

        if hasil:

            st.success(
                "Kendaraan ditemukan."
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Plat Nomor",
                    hasil.plat
                )

            with col2:

                st.metric(
                    "Jenis",
                    hasil.jenis
                )

            st.info(
                f"Jam Masuk : {hasil.jam_masuk.strftime('%d-%m-%Y %H:%M:%S')}"
            )

        else:

            st.error(
                "Kendaraan tidak ditemukan."
            )
# =====================================================
# KENDARAAN AKTIF
# =====================================================

elif menu == "Kendaraan Aktif":

    st.subheader(
        "🚗 Kendaraan Sedang Parkir"
    )

    data = st.session_state.parkir.tampilkan_semua()

    if len(data) > 0:

        df = pd.DataFrame(data)

        st.dataframe(
            df,
            use_container_width=True
        )

        motor = len(
            df[df["Jenis"] == "Motor"]
        )

        mobil = len(
            df[df["Jenis"] == "Mobil"]
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Total Kendaraan",
                len(df)
            )

        with col2:

            st.metric(
                "Motor",
                motor
            )

        with col3:

            st.metric(
                "Mobil",
                mobil
            )

    else:

        st.warning(
            "Belum ada kendaraan aktif."
        )
# =====================================================
# SORTING PLAT NOMOR
# =====================================================

elif menu == "Sorting Plat":

    st.subheader(
        "🔤 Sorting Plat Nomor A-Z"
    )

    hasil = (
        st.session_state
        .parkir
        .sorting_plat()
    )

    if len(hasil) > 0:

        df = pd.DataFrame(
            hasil
        )

        st.success(
            "Data berhasil diurutkan."
        )

        st.dataframe(
            df,
            use_container_width=True
        )

    else:

        st.warning(
            "Data kendaraan kosong."
        )
# =====================================================
# KENDARAAN KELUAR
# =====================================================

elif menu == "Kendaraan Keluar":

    st.subheader("🚪 Proses Kendaraan Keluar")

    plat_keluar = st.text_input(
        "Masukkan Plat Nomor"
    )

    metode = st.selectbox(
        "Metode Pembayaran",
        [
            "Cash",
            "QRIS",
            "Transfer Bank"
        ]
    )

    st.markdown("---")

    if st.button(
        "💰 Hitung & Bayar",
        use_container_width=True
    ):

        data = (
            st.session_state
            .parkir
            .cari_kendaraan(
                plat_keluar
            )
        )

        if data is None:

            st.error(
                "Plat nomor tidak ditemukan."
            )

        else:

            jam_keluar = datetime.now()

            lama_parkir = (
                jam_keluar -
                data.jam_masuk
            ).total_seconds() / 3600

            if lama_parkir < 1:
                lama_parkir = 1

            lama_parkir = round(
                lama_parkir
            )

            tarif_per_jam = TARIF[
                data.jenis
            ]

            total_bayar = (
                lama_parkir *
                tarif_per_jam
            )

            st.success(
                "Perhitungan berhasil."
            )

            col1,col2 = st.columns(2)

            with col1:

                st.info(
                    f"🚗 Plat : {data.plat}"
                )

                st.info(
                    f"🚙 Jenis : {data.jenis}"
                )

                st.info(
                    f"⏱ Lama Parkir : {lama_parkir} Jam"
                )

            with col2:

                st.success(
                    f"💰 Tarif/Jam : Rp {tarif_per_jam:,}"
                )

                st.success(
                    f"💵 Total Bayar : Rp {total_bayar:,}"
                )

                st.success(
                    f"💳 Metode : {metode}"
                )
            # =====================================
            # QRIS
            # =====================================

            if metode == "QRIS":

                st.image(
                    "https://upload.wikimedia.org/wikipedia/commons/8/80/QR_code_for_mobile_English_Wikipedia.svg",
                    width=250
                )

                st.warning(
                    "Silakan scan QRIS untuk melakukan pembayaran."
                )

            # =====================================
            # TRANSFER BANK
            # =====================================

            elif metode == "Transfer Bank":

                st.info(
                    """
                    Bank BCA

                    No Rekening:
                    1234567890

                    Atas Nama:
                    SMART PARKING
                    """
                )

            # =====================================
            # CASH
            # =====================================

            else:

                st.success(
                    "Pembayaran dilakukan secara tunai."
                )
            st.markdown("---")

            if st.button(
                "✅ Konfirmasi Pembayaran"
            ):

                transaksi = {

                    "Plat":
                    data.plat,

                    "Jenis":
                    data.jenis,

                    "Masuk":
                    data.jam_masuk.strftime(
                        "%d-%m-%Y %H:%M:%S"
                    ),

                    "Keluar":
                    jam_keluar.strftime(
                        "%d-%m-%Y %H:%M:%S"
                    ),

                    "Durasi":
                    lama_parkir,

                    "Metode":
                    metode,

                    "Total":
                    total_bayar
                }

                st.session_state.riwayat.append(
                    transaksi
                )

                st.session_state.pendapatan.append(
                    total_bayar
                )

                st.session_state.parkir.hapus_kendaraan(
                    data.plat
                )

                st.success(
                    "Pembayaran berhasil."
                )

                st.balloons()
                # =====================================
                # PDF STRUK
                # =====================================

                nama_pdf = (
                    f"struk_{data.plat}.pdf"
                )

                doc = SimpleDocTemplate(
                    nama_pdf
                )

                styles = (
                    getSampleStyleSheet()
                )

                isi_pdf = [

                    Paragraph(
                        "SMART PARKING SYSTEM",
                        styles["Title"]
                    ),

                    Spacer(1,20),

                    Paragraph(
                        f"Plat : {data.plat}",
                        styles["BodyText"]
                    ),

                    Paragraph(
                        f"Jenis : {data.jenis}",
                        styles["BodyText"]
                    ),

                    Paragraph(
                        f"Jam Masuk : {data.jam_masuk}",
                        styles["BodyText"]
                    ),

                    Paragraph(
                        f"Jam Keluar : {jam_keluar}",
                        styles["BodyText"]
                    ),

                    Paragraph(
                        f"Lama Parkir : {lama_parkir} Jam",
                        styles["BodyText"]
                    ),

                    Paragraph(
                        f"Metode Pembayaran : {metode}",
                        styles["BodyText"]
                    ),

                    Paragraph(
                        f"Total Bayar : Rp {total_bayar:,}",
                        styles["BodyText"]
                    )

                ]

                doc.build(
                    isi_pdf
                )

                with open(
                    nama_pdf,
                    "rb"
                ) as file:

                    st.download_button(

                        label="📄 Download Struk PDF",

                        data=file,

                        file_name=nama_pdf,

                        mime="application/pdf"

                    )
                st.markdown("---")

                st.subheader(
                    "🧾 Detail Transaksi"
                )

                detail = pd.DataFrame([
                    {
                        "Plat":
                        data.plat,

                        "Jenis":
                        data.jenis,

                        "Masuk":
                        data.jam_masuk,

                        "Keluar":
                        jam_keluar,

                        "Durasi":
                        lama_parkir,

                        "Metode":
                        metode,

                        "Total":
                        total_bayar
                    }
                ])

                st.dataframe(
                    detail,
                    use_container_width=True
                )
# =====================================================
# GRAFIK PENDAPATAN
# =====================================================

elif menu == "Grafik Pendapatan":

    st.subheader(
        "📈 Grafik Pendapatan Parkir"
    )

    if len(
        st.session_state.pendapatan
    ) > 0:

        df_grafik = pd.DataFrame({

            "Transaksi":
            range(
                1,
                len(
                    st.session_state.pendapatan
                ) + 1
            ),

            "Pendapatan":
            st.session_state.pendapatan

        })

        st.dataframe(
            df_grafik,
            use_container_width=True
        )

        fig, ax = plt.subplots(
            figsize=(10,5)
        )

        ax.plot(

            df_grafik["Transaksi"],

            df_grafik["Pendapatan"],

            marker="o",

            linewidth=3

        )

        ax.set_title(
            "Grafik Pendapatan"
        )

        ax.set_xlabel(
            "Transaksi"
        )

        ax.set_ylabel(
            "Pendapatan (Rp)"
        )

        st.pyplot(fig)

    else:

        st.warning(
            "Belum ada data pendapatan."
        )
    st.markdown("---")

    st.subheader(
        "🚗 Statistik Jenis Kendaraan"
    )

    aktif = (
        st.session_state
        .parkir
        .tampilkan_semua()
    )

    if len(aktif) > 0:

        motor = 0
        mobil = 0

        for item in aktif:

            if item["Jenis"] == "Motor":

                motor += 1

            elif item["Jenis"] == "Mobil":

                mobil += 1

        fig2, ax2 = plt.subplots()

        ax2.pie(

            [motor, mobil],

            labels=[
                "Motor",
                "Mobil"
            ],

            autopct="%1.1f%%"

        )

        st.pyplot(fig2)

    else:

        st.info(
            "Belum ada kendaraan aktif."
        )
# =====================================================
# RIWAYAT TRANSAKSI
# =====================================================

elif menu == "Riwayat Transaksi":

    st.subheader(
        "🧾 Riwayat Transaksi"
    )

    if len(
        st.session_state.riwayat
    ) > 0:

        df = pd.DataFrame(
            st.session_state.riwayat
        )

        st.dataframe(
            df,
            use_container_width=True
        )
        csv = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(

            "📥 Download CSV",

            csv,

            "riwayat_parkir.csv",

            "text/csv"

        )
        total = df["Total"].sum()

        st.success(
            f"💰 Total Pendapatan : Rp {total:,.0f}"
        )
        st.markdown("---")

        st.subheader(
            "🔍 Filter Plat Nomor"
        )

        keyword = st.text_input(
            "Cari Plat"
        )

        if keyword:

            hasil = df[
                df["Plat"]
                .str.contains(
                    keyword.upper(),
                    na=False
                )
            ]

            st.dataframe(
                hasil,
                use_container_width=True
            )
        st.markdown("---")

        if st.button(
            "🗑 Hapus Semua Riwayat"
        ):

            st.session_state.riwayat = []

            st.session_state.pendapatan = []

            st.success(
                "Semua riwayat berhasil dihapus."
            )

            st.rerun()
    else:

        st.warning(
            "Belum ada transaksi."
        )
# =====================================================
# LOGOUT
# =====================================================

st.sidebar.markdown("---")

if st.sidebar.button(
    "🚪 Logout"
):

    st.session_state.login = False

    st.rerun()

