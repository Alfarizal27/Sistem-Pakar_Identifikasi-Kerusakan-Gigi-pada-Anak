import streamlit as st
import json

# Konfigurasi halaman
st.set_page_config(page_title="Sistem Pakar Kerusakan Gigi", layout="wide")

# ==============================
# 1️⃣ Fungsi: Memuat rules.json
# ==============================
def load_rules():
    with open("rules.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["rules"]  # langsung ambil list rules


# ==============================
# 2️⃣ Fungsi: Hitung CF (Certainty Factor)
# ==============================
def hitung_cf(gejala_dipilih, rules):
    hasil = []

    for rule in rules:
        penyakit = rule["then"]
        cf_total = 0.0

        for gejala, cf in rule["premise_cf_expert"].items():
            if gejala in gejala_dipilih:
                cf_total += cf  # tambahkan jika gejala dipilih

        cf_total = min(cf_total, 1.0)  # batasi maksimal 1.0
        hasil.append((penyakit, round(cf_total * 100, 2)))

    hasil.sort(key=lambda x: x[1], reverse=True)  # urutkan dari yang tertinggi
    return hasil


# ==============================
# 3️⃣ Tampilan Utama
# ==============================
st.title("🦷 Cek Kesehatan Gigi Yuk!")
st.write("""
Selamat datang di **Sistem Pakar Diagnosa Kerusakan Gigi** berbasis web.
Silakan jawab beberapa pertanyaan untuk mengetahui kemungkinan jenis kerusakan gigi yang kamu alami.
""")


# ==============================
# 4️⃣ Tombol Mulai
# ==============================
if "mulai" not in st.session_state:
    if st.button("Mulai Pemeriksaan"):
        st.session_state.mulai = True

# ==============================
# 5️⃣ Jika tombol mulai ditekan
# ==============================
if "mulai" in st.session_state:
    rules = load_rules()

    # Ambil semua gejala unik dari rules
    gejala_semua = sorted(set(g for r in rules for g in r["if"]))

    st.header("Pilih gejala yang kamu rasakan:")
    gejala_dipilih = []

    for gejala in gejala_semua:
        if st.checkbox(gejala):
            gejala_dipilih.append(gejala)

    if st.button("Lihat Hasil Diagnosa"):
        if not gejala_dipilih:
            st.warning("Pilih minimal satu gejala dulu ya!")
        else:
            hasil = hitung_cf(gejala_dipilih, rules)

            st.subheader("📋 Hasil Diagnosa:")
            for penyakit, cf in hasil:
                st.write(f"**{penyakit}** — Tingkat Keyakinan: {cf}%")
