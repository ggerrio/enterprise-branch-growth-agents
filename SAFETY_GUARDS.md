# Aturan Keamanan & Kebijakan Human-in-the-Loop (HITL) Cabang

## 1. Identifikasi Aksi Risiko Tinggi (High-Stakes Actions)
Setiap kali rekomendasi strategi bisnis menghasilkan usulan berupa:
- Alokasi dana insentif promosi tambahan untuk showroom.
- Perubahan target kuota booking untuk CMO lapangan.
Aksi ini diklasifikasikan sebagai Aksi Risiko Tinggi.

## 2. Protokol Penahanan Otomatis (Halt & Triage)
- Agen DILARANG LANGSUNG mengirimkan output ini ke sistem CRM/database operasional CMO lapangan secara otomatis.
- Agen harus memotong alur kerja (*intercept*), membekukan status (*state*), dan memicu fungsi `trigger_human_intervention()`.

## 3. Komponen Antarmuka Persetujuan (A2UI HITL Request)
Agen wajib memunculkan draf keputusan kepada Branch Manager dengan format visual berikut:
------------------------------------------------------------
[⚠️ PERMINTAAN PERSETUJUAN STRATEGI BISNIS KELUAR]
Showroom Target: [Nama Showroom]
Rekomendasi Insentif: Rp [Jumlah Dana]
Alasan: Pengambilan alih pasar dari kompetitor (NPL Aman)

Apakah Anda menyetujui peluncuran program promo ini?
[ SETUJUI ANGGARAN ]   |   [ TOLAK / REVISI ]
------------------------------------------------------------

## 4. Validasi Akhir
- Jika Branch Manager mengklik [ SETUJUI ANGGARAN ], agen diizinkan memperbarui status log promosi database menjadi "APPROVED".
- Jika dibatalkan atau tidak ada respons, status tetap "PENDING" dan akses jaringan ke database operasional cabang tetap ditutup.