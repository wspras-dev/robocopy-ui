# Robocopy UI - Fitur Tambahan Part 2

## Ringkasan Perubahan

Dokumentasi ini mencatat penambahan fitur Junction dan Symbolic Link management ke aplikasi Robocopy Advanced GUI.

---

## Fitur Ditambahkan

### 1. Tab Baru: Junction & Symbolic Links

Sebuah tab baru bernama **"Junction & Links"** telah ditambahkan ke aplikasi dengan dua section utama:

#### Section 1: Copy Options
- **`/SJ` - Salin Junction/Symbolic Link**: Menyalin Junction/Symbolic Link itu sendiri ke tujuan, bukan menyalin file di dalam direktori target
- **`/SL` - Salin Symbolic Link**: Menyalin tautan simbolik sebagai tautan, bukan menyalin file target

#### Section 2: Exclude Options
- **`/XJ` - Kecualikan Semua Junction Points**: Mengecualikan titik persimpangan (yang biasanya disertakan secara default), mencegah potensi perulangan tak terbatas
- **`/XJD` - Kecualikan Junction untuk Direktori**: Secara khusus mengecualikan titik junction untuk direktori saja
- **`/XJF` - Kecualikan Junction untuk File**: Secara khusus mengecualikan titik junction untuk file saja

---

## Perubahan Kode

### 1. File: `rbcopy-plus.py`

#### Penambahan di `init_ui()` method (Line ~146)
```python
# Tab 5: Junction & Symbolic Links
tabs.addTab(self.create_junction_links_tab(), "Junction & Links")

# Tab 6: About
tabs.addTab(self.create_about_tab(), "About")
```

#### Method Baru: `create_junction_links_tab()` (Line ~406-467)
```python
def create_junction_links_tab(self):
    """Tab untuk Junction dan Symbolic Link options"""
    # Informasi section
    # Copy options section
    # Exclude options section
```

Struktur UI:
- **Information Group**: Menampilkan penjelasan lengkap tentang setiap parameter
- **Copy Options Group**: Checkbox untuk `/SJ` dan `/SL`
- **Exclude Options Group**: Checkbox untuk `/XJ`, `/XJD`, dan `/XJF`

#### Penambahan di `build_robocopy_command()` method (Line ~645-656)
```python
# Junction and Symbolic Link options
if self.copy_junction.isChecked():
    cmd += " /SJ"
if self.copy_symlink.isChecked():
    cmd += " /SL"
if self.exclude_junction.isChecked():
    cmd += " /XJ"
if self.exclude_junction_dir.isChecked():
    cmd += " /XJD"
if self.exclude_junction_file.isChecked():
    cmd += " /XJF"
```

#### Penambahan di `save_config()` method (Line ~765-769)
```python
"copy_junction": self.copy_junction.isChecked(),
"copy_symlink": self.copy_symlink.isChecked(),
"exclude_junction": self.exclude_junction.isChecked(),
"exclude_junction_dir": self.exclude_junction_dir.isChecked(),
"exclude_junction_file": self.exclude_junction_file.isChecked(),
```

#### Penambahan di `load_config()` method (Line ~811-815)
```python
self.copy_junction.setChecked(config_data.get("copy_junction", False))
self.copy_symlink.setChecked(config_data.get("copy_symlink", False))
self.exclude_junction.setChecked(config_data.get("exclude_junction", False))
self.exclude_junction_dir.setChecked(config_data.get("exclude_junction_dir", False))
self.exclude_junction_file.setChecked(config_data.get("exclude_junction_file", False))
```

#### Update Tab About (Line ~510)
Menambahkan "Junction dan Symbolic Link management" ke daftar fitur.

---

### 2. File: `README.md`

#### Penambahan Section: "Junction & Symbolic Link Management"
- Deskripsi singkat 5 parameter utama
- Penjelasan lengkap masing-masing parameter
- Tabel parameter untuk Copy Options
- Tabel parameter untuk Exclude Options
- Contoh use cases dengan langkah-langkah

#### Update Configuration File Section
Menambahkan 5 field baru ke contoh `config.conf`:
```json
"copy_junction": false,
"copy_symlink": false,
"exclude_junction": false,
"exclude_junction_dir": false,
"exclude_junction_file": false
```

---

## Contoh Penggunaan

### Skenario 1: Backup Folder dengan Junctions (Preserve Links)
1. Buka tab "Junction & Links"
2. Centang "Copy Junction (/SJ)"
3. Jalankan copy
4. Junction akan di-copy as-is, tanpa mengikuti target

### Skenario 2: Avoid Infinite Loops
1. Buka tab "Junction & Links"
2. Centang "Exclude Junction (/XJ)"
3. Jalankan copy
4. Semua junction akan diabaikan

### Skenario 3: Selective Junction Handling
1. Centang "Exclude File Junction (/XJF)" saja
2. File junctions akan di-skip, tapi directory junctions tetap di-copy

---

## Robocopy Parameter Reference

| Parameter | Singkatan | Deskripsi |
|-----------|-----------|-----------|
| /SJ | Copy Junction | Copy junction/symbolic link itu sendiri |
| /SL | Symbolic Link | Copy symbolic link sebagai link |
| /XJ | Exclude Junction | Exclude semua junction points |
| /XJD | Exclude Dir Junction | Exclude directory junctions saja |
| /XJF | Exclude File Junction | Exclude file junctions saja |

---

## Generated Command Examples

### Contoh 1: Copy dengan Preserve Junctions
```
robocopy "C:\Source" "D:\Backup" /S /SJ /R:1 /W:30
```

### Contoh 2: Copy Exclude Junctions
```
robocopy "C:\Source" "D:\Backup" /S /XJ /R:1 /W:30
```

### Contoh 3: Copy Hanya File (Skip File Junctions)
```
robocopy "C:\Source" "D:\Backup" /S /XJF /R:1 /W:30
```

---

## Testing Checklist

- [x] Syntax check passed
- [x] All 5 checkboxes properly initialized
- [x] Parameters added to command building
- [x] Config save/load functionality works
- [x] Tab displays correctly with information
- [x] README documentation updated

---

## Catatan Penting

1. **Default Behavior**: Semua junction dan symlink options default ke `False` (disabled)
2. **Mutual Exclusivity**: Parameter `/SJ` dan `/SL` bersifat independent, keduanya bisa digunakan bersamaan
3. **Safety**: Gunakan `/XJ` dengan hati-hati pada folder dengan circular junctions
4. **Config Persistence**: Semua setting otomatis disimpan ke `config.conf`

---

## Backward Compatibility

Fitur ini fully backward compatible. Aplikasi lama yang tidak memiliki setting junction akan otomatis mendapatkan default value `False` untuk semua parameter baru.

---

**Last Updated**: February 2026
**Version**: 1.0.0 - Part 2 Enhancement
