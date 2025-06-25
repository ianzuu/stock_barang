import streamlit as st
import sqlite3
import pandas as pd

# --- Login Admin ---
def login():
    st.title("🔐 Login Admin")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state['login'] = True
            st.rerun()
        else:
            st.error("Username atau password salah!")

if 'login' not in st.session_state:
    st.session_state['login'] = False

if not st.session_state['login']:
    login()
    st.stop()  # Hentikan kode kalau belum login
st.set_page_config(
    page_title="Aplikasi Stok Barang ",
    page_icon="📦",
    layout="centered"
)

# Koneksi ke database
conn = sqlite3.connect('stok_barang.db', check_same_thread=False)
cursor = conn.cursor()

# Buat tabel kalau belum ada
cursor.execute('''
CREATE TABLE IF NOT EXISTS stok (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kode_barang TEXT,
    nama_barang TEXT,
    qty_awal INTEGER,
    qty_masuk INTEGER,
    qty_keluar INTEGER,
    qty_seharusnya INTEGER,
    qty_real INTEGER,
    qty_selisih INTEGER
)
''')
conn.commit()

st.title(" Aplikasi Stok Barang - by ian")

# Form input
st.subheader("?? Input Data Stok Barang")
with st.form("form_input"):
    kode = st.text_input("Kode Barang")
    nama = st.text_input("Nama Barang")
    qty_awal = st.number_input("Qty Awal", 0)
    qty_masuk = st.number_input("Qty Masuk", 0)
    qty_keluar = st.number_input("Qty Keluar", 0)
    qty_real = st.number_input("Qty Real", 0)

    submitted = st.form_submit_button("Simpan Data")
    if submitted:
        qty_seharusnya = qty_awal + qty_masuk - qty_keluar
        qty_selisih = qty_real - qty_seharusnya

        cursor.execute('''
            INSERT INTO stok (
                kode_barang, nama_barang, qty_awal, qty_masuk,
                qty_keluar, qty_seharusnya, qty_real, qty_selisih
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (kode, nama, qty_awal, qty_masuk, qty_keluar, qty_seharusnya, qty_real, qty_selisih))
        conn.commit()
        st.success(" Data berhasil disimpan!")

# Menampilkan data
st.subheader(" Data Stok Barang")
df = pd.read_sql_query("SELECT * FROM stok", conn)
st.dataframe(df)

st.subheader("✏️ Edit / 🗑️ Hapus Data")

# Pilih baris yang ingin diedit atau dihapus
if not df.empty:
    selected_id = st.selectbox("Pilih ID Data", df["id"])

    selected_row = df[df["id"] == selected_id].iloc[0]

    st.markdown("### Edit Data")
    with st.form("form_edit"):
        kode = st.text_input("Kode Barang", selected_row["kode_barang"])
        nama = st.text_input("Nama Barang", selected_row["nama_barang"])
        qty_awal = st.number_input("Qty Awal", value=int(selected_row["qty_awal"]))
        qty_masuk = st.number_input("Qty Masuk", value=int(selected_row["qty_masuk"]))
        qty_keluar = st.number_input("Qty Keluar", value=int(selected_row["qty_keluar"]))
        qty_real = st.number_input("Qty Real", value=int(selected_row["qty_real"]))

        update = st.form_submit_button("💾 Simpan Perubahan")
        if update:
            qty_seharusnya = qty_awal + qty_masuk - qty_keluar
            qty_selisih = qty_real - qty_seharusnya

            cursor.execute('''
                UPDATE stok SET
                    kode_barang=?, nama_barang=?, qty_awal=?, qty_masuk=?,
                    qty_keluar=?, qty_seharusnya=?, qty_real=?, qty_selisih=?
                WHERE id=?
            ''', (
                kode, nama, qty_awal, qty_masuk, qty_keluar,
                qty_seharusnya, qty_real, qty_selisih, selected_id
            ))
            conn.commit()
            st.success("✅ Data berhasil diperbarui!")
            st.rerun()

    if st.button("hapus data ini")


# Export Excel
def export_excel():
    df.to_excel("hasil_stok.xlsx", index=False)
    with open("hasil_stok.xlsx", "rb") as f:
        st.download_button("?? Download Excel", f, file_name="hasil_stok.xlsx")

export_excel()
