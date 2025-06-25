import streamlit as st
import sqlite3
import pandas as pd

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
        st.success("? Data berhasil disimpan!")

# Menampilkan data
st.subheader("?? Data Stok Barang")
df = pd.read_sql_query("SELECT * FROM stok", conn)
st.dataframe(df)

# Export Excel
def export_excel():
    df.to_excel("hasil_stok.xlsx", index=False)
    with open("hasil_stok.xlsx", "rb") as f:
        st.download_button("?? Download Excel", f, file_name="hasil_stok.xlsx")

export_excel()
