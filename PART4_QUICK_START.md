# PART 4 - QUICK START GUIDE

## Fitur Baru di Part 4

### 1. 📂 Browse ke Folder Terakhir (Otomatis)
Saat menekan tombol **Browse** pada field Source atau Destination, file dialog akan membuka langsung ke folder terakhir yang Anda pilih.

**Cara Menggunakan:**
1. Di tab "Source & Destination"
2. Klik tombol **Browse...** di samping field Source
3. File dialog akan membuka ke folder Source terakhir (jika ada)
4. Pilih folder baru, atau batalkan untuk kembali
5. Sama untuk Destination

**Keuntungan:**
- ✅ Lebih cepat saat memilih folder yang sering digunakan
- ✅ Tidak perlu navigate dari root folder setiap kali
- ✅ Workflow lebih smooth

---

### 2. 🎨 Animasi Gradient Background (Optional)

Saat copy berlangsung, background form aplikasi dapat menampilkan animasi gradient warna yang berubah-ubah.

**Cara Mengaktifkan:**
1. Buka tab **"Copy Options"**
2. Scroll ke bawah, cari grup **"Animation & Effects (Part 4)"**
3. Centang checkbox: **"🎨 Enable Animated Gradient Background During Copy"**
4. Klik Save Config jika ingin menyimpan setting
5. Jalankan Robocopy - background akan beranimasi!

**Warna Animasi:**
```
🔴 Red → 🟠 Orange → 🔵 Blue → 🟢 Green → 🟣 Purple → 🔴 (Cycle)
```

**Saat Berhenti:**
- Animasi otomatis berhenti saat copy selesai
- Animasi otomatis berhenti saat Anda klik STOP
- Animasi otomatis berhenti saat ada error

**Performance:**
- ✅ Update smooth (20 FPS)
- ✅ CPU usage minimal
- ✅ Tidak mempengaruhi proses copy
- ✅ Optional - bisa dimatikan kapan saja

---

## Workflow Contoh

### Skenario: Regular Backup

1. **Pertama Kali:**
   ```
   - Tab "Source & Destination"
   - Klik Browse di Source → pilih "D:\Documents"
   - Klik Browse di Destination → pilih "E:\Backup"
   - Tab "Copy Options"
   - Centang "🎨 Enable Animated Gradient Background"
   - Klik "💾 Save Config"
   ```

2. **Kedua Kalinya:**
   ```
   - Klik Browse di Source → langsung ke "D:\Documents" ✨
   - Klik Browse di Destination → langsung ke "E:\Backup" ✨
   - (Setting animasi sudah tersimpan)
   - Klik "▶ Run Robocopy"
   - Lihat background beranimasi sambil proses berjalan 🎨
   ```

---

## Settings Tersimpan

Semua pengaturan Part 4 otomatis tersimpan di **config.conf**:

```json
{
  "enable_animation": true,
  "source": "D:\\Documents",
  "destination": "E:\\Backup"
}
```

**Saat Load:**
- Folder Source otomatis terisi dari config
- Folder Destination otomatis terisi dari config
- Setting animasi otomatis dikembalikan

---

## Tips & Tricks

### Browse Lebih Cepat
- Setelah browse folder pertama, path tersimpan
- Klik Browse lagi, langsung ke folder terakhir
- Tidak perlu navigate dari awal

### Menghemat CPU
- Jika komputer lambat saat copy, nonaktifkan animasi
- Uncheck "🎨 Enable Animated Gradient Background"
- CPU akan fokus 100% ke proses copy

### Menggunakan Multiple Config
- Edit `config.conf` manual untuk multiple profile
- Atau gunakan "💾 Save Config" untuk setiap workflow

---

## Troubleshooting

| Masalah | Solusi |
|---------|--------|
| Browse tidak membuka ke folder terakhir | Pastikan path di field masih valid |
| Animasi tidak berjalan | Periksa apakah checkbox animasi sudah di-check |
| Background tidak berubah warna | Pastikan enable_animation = true di config.conf |
| CPU usage tinggi saat animasi | Nonaktifkan animasi, atau reduce update frequency |

---

## Integrasi dengan Part 3

Part 4 melanjutkan fitur-fitur Part 3:

| Fitur | Part | Status |
|-------|------|--------|
| Confirmation Dialog | Part 3 | ✅ Aktif |
| Button Disable saat Running | Part 3 | ✅ Aktif |
| Progress Monitoring | Part 3 | ✅ Aktif |
| **Browse Last Folder** | **Part 4** | **✅ NEW** |
| **Animated Background** | **Part 4** | **✅ NEW** |
| Config Save/Load | Part 3 | ✅ Enhanced |

---

## Spesifikasi Teknis

### AnimationThread
- **Update Rate**: 50ms (20 FPS)
- **Cycle Duration**: 5 detik per palet warna
- **Color Palettes**: 5 gradien berbeda
- **Signaling**: PyQt5 Signal untuk thread-safe updates

### Gradient System
- **Type**: QLinearGradient
- **Rendering**: Hardware accelerated (via Qt)
- **Interpolation**: Smooth RGB color interpolation

---

**Dokumentasi Lengkap**: Lihat `PART4_FEATURES.md`

**Last Updated**: February 2026
**Version**: 1.0.0
