# Robocopy Advanced GUI

Aplikasi GUI untuk menjalankan Windows Robocopy dengan antarmuka yang user-friendly dan parameter yang mudah dikonfigurasi.

## Daftar Isi
- [Fitur Utama](#fitur-utama)
- [Sistem Requirements](#sistem-requirements)
- [Instalasi](#instalasi)
- [Cara Penggunaan](#cara-penggunaan)
- [Dokumentasi Fitur](#dokumentasi-fitur)
- [Configuration File](#configuration-file)
- [Troubleshooting](#troubleshooting)

---

## Fitur Utama

### 📁 **Source & Destination Management**
- Pilih folder source dan destination melalui file browser
- Path validation otomatis
- Support untuk path dengan spasi dan karakter khusus

### 📋 **Copy Options**
- **Mirror (/MIR)**: Synchronize folder source dan destination
- **Subdirectories (/S)**: Copy subdirectories (except empty ones)
- **Empty Subdirectories (/E)**: Copy empty subdirectories
- **Move Files (/MOVE)**: Move files (delete after copy)
- **Purge (/PURGE)**: Delete destination files/dirs tidak ada di source
- **Copy Attributes**: Copy Data, Attributes, Timestamps, Security info
- **Multi-threading**: Support 1-128 threads untuk copy lebih cepat

### 🔍 **File Selection**
- **Include File Patterns**: Specify file types untuk include
  - Contoh: `*.txt;*.docx;*.pdf`
- **Exclude File Patterns**: Exclude file types tertentu
  - Contoh: `*.tmp;Thumbs.db;.git`
- **Exclude Directories**: Exclude folder tertentu
  - Contoh: `.git;node_modules;__pycache__`
- **File Age Filter**: Filter berdasarkan umur file

### ⚙️ **Retry & Logging**
- **Retry Configuration**: Set jumlah retry dan wait time
- **Verbose Logging**: Show semua file yang di-skip
- **List Only Mode**: Test mode tanpa benar-benar copy file
- **Log to File**: Save output ke file `.log`

### 🔗 **Junction & Symbolic Link Management**
- **Copy Junction (/SJ)**: Salin Junction/Symbolic Link itu sendiri, bukan file di dalam direktori target
- **Copy Symbolic Link (/SL)**: Salin tautan simbolik sebagai tautan, bukan file target
- **Exclude Junction (/XJ)**: Kecualikan semua junction points untuk mencegah perulangan tak terbatas
- **Exclude Directory Junction (/XJD)**: Kecualikan titik junction untuk direktori saja
- **Exclude File Junction (/XJF)**: Kecualikan titik junction untuk file saja

### 🎯 **Additional Features**
- **Real-time Output Logging**: Monitor proses copy secara real-time
- **Copy Command**: Copy generated command ke clipboard
- **Configuration Persistence**: Auto-save settings ke `config.conf`
- **Application Logo**: Support icon dari `favicon.ico` atau `logo.png`
- **About Tab**: Informasi aplikasi dan developer
- **Process Control**: Stop/pause proses copy dengan tombol Stop

### ✨ **Part 4 - New Features (Feb 2026)**
- **Browse to Last Folder** (NEW): File dialog membuka ke folder terakhir yang digunakan
  - Smart path memory untuk Source dan Destination
  - Menghemat waktu navigasi folder
  - Works dengan config persistence
  
- **Animated Gradient Background** (NEW): Visual feedback animasi saat copy berlangsung
  - 5 color gradients yang berputar: Red→Orange→Blue→Green→Purple→Pink
  - Smooth animation (50ms update, 20 FPS)
  - Thread-safe implementation
  - Optional - dapat diaktifkan/dinonaktifkan
  - Minimal CPU impact (<5%)
  - Otomatis berhenti saat copy selesai

### 🎨 **Part 5 - Dual-Pane File Explorer (Feb 2026)**
- **Dual-Pane Layout** (NEW): Source dan Destination dalam layout side-by-side
  - Independent navigation per pane
  - Professional UX seperti Total Commander
  - Responsive dan mudah digunakan

- **File/Folder Listing with Icons** (NEW): Visual representation file dan folder
  - 📁 Folder icon untuk direktori
  - 📄 Document icons (.txt, .docx, .pdf, dll)
  - 📊 Spreadsheet icons (.xls, .xlsx, .csv)
  - 🖼️ Image icons (.jpg, .png, .gif, dll)
  - 🎬 Video icons (.mp4, .avi, .mkv, dll)
  - 🎵 Audio icons (.mp3, .wav, .flac, dll)
  - 💻 Code icons (.py, .js, .java, dll)
  - 📦 Archive icons (.zip, .rar, .7z, dll)
  - ⚙️ Executable icons (.exe, .msi, dll)
  - File size displayed untuk setiap file
  - Folders listed first, kemudian files (alphabetically sorted)

- **Double-Click Navigation** (NEW): Interactive folder exploration
  - Double-click folder untuk enter dan list contents
  - Automatic history tracking untuk back functionality
  - Parent folder (..) support untuk quick navigation up
  - Auto-refresh list saat navigasi
  - Path field automatically updated

- **Back Navigation & History** (NEW): Full history stack untuk navigasi
  - Back button untuk kembali ke previous folder
  - Full history stack implementation
  - Back button auto-disabled saat no history
  - Parent folder (..) di list untuk quick up navigation

- **File/Folder Statistics** (NEW): Quick insights tentang folder contents
  - Folder count per pane
  - File count per pane
  - Total size dengan auto-conversion (B→KB→MB→GB→TB)
  - Statistics displayed below setiap file list
  - Helps understand folder contents at a glance

### 📦 **Part 6 - Context Menu, Rename/Delete & Drag-Drop (Feb 2026)**

- **Context Menu Integration** (NEW): Right-click pada file/folder untuk quick actions
  - Right-click menu dengan opsi manajemen file
  - Opsi: Rename, Delete, Open in Explorer
  - Instant access tanpa toolbar buttons
  - Professional workflow integration

- **File Rename & Delete** (NEW): File management integrated dalam aplikasi
  - Rename file/folder dengan input dialog
  - Delete dengan confirmation (prevents accidents)
  - Recursive delete untuk folders (warns about contents)
  - Duplicate name checking (prevents overwrite)
  - Permission error handling (graceful failures)
  - Auto-refresh explorer (shows changes immediately)

- **Drag & Drop Copy** (NEW): Fast copy dengan automatic settings application
  - Drag file/folder dari Source pane ke Destination pane
  - Bidirectional: Source→Dest atau Dest→Source
  - Automatic robocopy triggering dengan drag-drop
  - Respects ALL configured settings:
    - Multi-threading (/MT:N)
    - Include/Exclude patterns
    - Copy flags (/S, /E, /MIR, /MOVE, /PURGE)
    - Attributes (/COPY:DAT, /SEC)
    - Retry & Logging options
    - Junction & Link settings
  - Visual feedback saat drag
  - Real-time progress display
  - No need to press "Run Robocopy" button

---

## Sistem Requirements

### Minimum Requirements
- **OS**: Windows 7 atau lebih baru
- **Python**: 3.7 atau lebih baru
- **RAM**: 512 MB minimum
- **Storage**: 50 MB untuk aplikasi

### Recommended Requirements
- **OS**: Windows 10/11
- **Python**: 3.9+
- **RAM**: 2 GB atau lebih
- **CPU**: Multi-core untuk multi-threading

---

## Instalasi

### 1. Install Python 3
Download dari [python.org](https://www.python.org) dan install dengan checklist "Add Python to PATH"

### 2. Clone atau Download Repository
```bash
# Menggunakan git
git clone <repository-url> robocopy-ui
cd robocopy-ui

# Atau download langsung dari browser
```

### 3. Install PyQt5
```powershell
pip install PyQt5
```

### 4. (Optional) Tambah Icon
Tempat file `favicon.ico` atau `logo.png` di folder aplikasi.

Ukuran rekomendasi:
- Icon: 256x256 piksel atau lebih
- Format: .ico atau .png

### 5. Jalankan Aplikasi
```powershell
python rbcopy-plus.py
```

---

## Cara Penggunaan

### Langkah-Langkah Dasar

#### 1. Set Source dan Destination Folder
- Buka tab **"Source & Destination"**
- Klik **"Browse..."** untuk pilih folder source
- Klik **"Browse..."** untuk pilih folder destination
- Atau ketik path langsung di text field

#### 2. Configure Copy Options
- Buka tab **"Copy Options"**
- Pilih options yang dibutuhkan:
  - Centang **"/S"** untuk copy subdirectories
  - Centang **"/MIR"** untuk mirror (synchronize)
  - Centang **"/MOVE"** untuk move files
  - Set jumlah threads untuk multi-threaded copy

#### 3. Set File Selection (Opsional)
- Buka tab **"File Selection"**
- Set **Include Files** untuk file yang ingin di-copy
  - Contoh: `*.txt;*.docx` (copy hanya text dan document)
- Set **Exclude Files** untuk file yang ingin di-skip
  - Contoh: `*.tmp;Thumbs.db` (skip temporary dan thumbnail files)
- Set **Exclude Directories** untuk folder yang ingin di-skip
  - Contoh: `.git;node_modules` (skip version control dan dependencies)

#### 4. Configure Retry & Logging (Opsional)
- Buka tab **"Retry & Logging"**
- Set **Max Retries**: Berapa kali retry jika ada error (default: 1)
- Set **Wait time**: Detik menunggu sebelum retry (default: 30)
- Centang **Verbose** untuk detail output
- Centang **Save log to file** untuk menyimpan hasil copy

#### 5. Run Robocopy
- Klik tombol **"▶ Run Robocopy"**
- Monitor progress di **"Output Log"** panel
- Klik **"⏹ Stop"** untuk menghentikan proses

#### 6. Save Configuration
- Klik **"💾 Save Config"** untuk menyimpan settings
- Settings akan otomatis disimpan setelah proses selesai
- Next time aplikasi dibuka, settings akan dimuat otomatis

---

## Dokumentasi Fitur

### Tab: Source & Destination

#### Source Folder
- **Input Field**: Text input untuk path folder source
- **Browse Button**: File dialog untuk browse folder
  - **Part 4 Feature**: Dialog membuka ke folder terakhir (smart path memory)
- **Required**: Ya

#### Destination Folder
- **Input Field**: Text input untuk path folder destination
- **Browse Button**: File dialog untuk browse folder
  - **Part 4 Feature**: Dialog membuka ke folder terakhir (smart path memory)
- **Required**: Ya

**Tips:**
- Support UNC path: `\\server\share\folder`
- Support drive letters: `C:\Users\Documents`
- Support relative path: `.\relative\path`
- **Part 4 Improvement**: Browse langsung ke folder terakhir (no need navigate from root!)

---

### Tab: Copy Options

#### Copy Flags

| Flag | Parameter | Deskripsi |
|------|-----------|-----------|
| /S | Copy Subdirectories | Copy subfolder (exclude empty) |
| /E | Empty Subdirectories | Copy subfolder (include empty) |
| /MIR | Mirror | Synchronize source dan destination |
| /MOVE | Move Files | Move files (delete after copy) |
| /PURGE | Purge | Delete files di destination yang tidak ada di source |

#### Copy Attributes

| Attribute | Flag | Deskripsi |
|-----------|------|-----------|
| Data (D) | /COPY:D | Copy data attributes |
| Attributes (A) | /COPY:A | Copy file attributes (read-only, hidden, etc) |
| Timestamps (T) | /COPY:T | Copy modified timestamps |
| Security (S) | /SEC | Copy NTFS security info |

#### Multi-threading

- **Enable**: Centang checkbox untuk enable multi-threading
- **Threads**: Set jumlah threads (1-128)
- **Default**: 8 threads
- **Tips**: 
  - Local disk to local disk: 8-16 threads
  - Network copy: 4-8 threads
  - Slow network: 2-4 threads

#### Animation & Effects (Part 4) ✨

- **Enable**: Centang "🎨 Enable Animated Gradient Background During Copy"
- **Default**: Disabled
- **Visual**: Background animasi dengan 5 color gradients
- **Features**:
  - Color sequence: Red → Orange → Blue → Green → Purple → Pink
  - Smooth animation (50ms update, 20 FPS)
  - Automatic lifecycle (start/stop dengan copy process)
  - Optional - dapat diaktifkan/dinonaktifkan sesuai preferensi
  - Minimal CPU impact (<5%)
  
**Tips:**
- Enable untuk visual feedback yang lebih menarik
- Disable jika komputer lambat atau mengalami lag
- Setting tersimpan otomatis di config.conf
- Animasi berjalan di thread terpisah (tidak block UI)

---

### Tab: File Selection

#### Include Files
- **Format**: Pisahkan dengan semicolon (`;`)
- **Contoh**: `*.txt;*.docx;*.pdf`
- **Default**: `*.*` (semua file)
- **Tips**:
  - `*.jpg;*.png;*.gif` - Copy gambar
  - `*.doc;*.docx;*.xls;*.xlsx` - Copy Office files
  - `*.exe;*.msi` - Copy installers

#### Exclude Files
- **Format**: Pisahkan dengan semicolon (`;`)
- **Contoh**: `*.tmp;Thumbs.db;.git`
- **Tips**:
  - `*.tmp;*.bak;*.tmp~` - Skip temporary files
  - `Thumbs.db;.DS_Store` - Skip OS metadata
  - `*.log;*.exe` - Skip log dan executable files

#### Exclude Directories
- **Format**: Pisahkan dengan semicolon (`;`)
- **Contoh**: `.git;node_modules;__pycache__`
- **Tips**:
  - `.git;.svn;.hg` - Skip version control
  - `node_modules;venv` - Skip dependencies
  - `__pycache__;.vscode` - Skip development files

#### File Age Filter
- **Enable**: Centang "Exclude files older than"
- **Days**: Set jumlah hari
- **Contoh**: 30 days = exclude files lebih dari 30 hari
- **Tips**: Gunakan untuk backup hanya recent files

---

### Tab: Retry & Logging

#### Retry Options

| Setting | Default | Range | Deskripsi |
|---------|---------|-------|-----------|
| Max Retries | 1 | 0-32767 | Jumlah kali retry jika copy gagal |
| Wait time | 30 sec | 0-300 | Detik menunggu sebelum retry |

**Tips:**
- Network copy: Set retry 3-5 kali dengan wait 30-60 sec
- Local copy: Set retry 1 kali dengan wait 0-10 sec

#### Logging Options

| Option | Parameter | Deskripsi |
|--------|-----------|-----------|
| Verbose | /V | Show semua file (termasuk yang skip) |
| List Only | /L | Simulasi copy (tidak benar-benar copy) |
| Log to File | /LOG | Save output ke file |

**Tips:**
- Gunakan "List Only" (/L) untuk test sebelum copy
- Gunakan "Verbose" untuk debug jika ada issue
- Gunakan "Log to File" untuk audit trail

---

### Tab: Junction & Symbolic Links

#### Copy Options

| Option | Parameter | Deskripsi |
|--------|-----------|-----------|
| Copy Junction | /SJ | Salin Junction/Symbolic Link itu sendiri, bukan file di dalam |
| Copy Symbolic Link | /SL | Salin tautan simbolik sebagai tautan, bukan file target |

**Tips:**
- Gunakan `/SJ` untuk backup struktur junction tanpa mengikuti target
- Gunakan `/SL` untuk preserve symbolic link references

#### Exclude Options

| Option | Parameter | Deskripsi |
|--------|-----------|-----------|
| Exclude Junction | /XJ | Kecualikan SEMUA junction points |
| Exclude Dir Junction | /XJD | Kecualikan junction untuk direktori saja |
| Exclude File Junction | /XJF | Kecualikan junction untuk file saja |

**Tips:**
- Gunakan `/XJ` untuk avoid infinite loops dengan circular junctions
- Gunakan `/XJD` atau `/XJF` untuk selective exclude
- Default behavior: junctions di-follow (included)

#### Contoh Kasus Penggunaan

**Kasus 1: Backup dengan preserving junctions**
- Centang: `/SJ` (Copy Junction)
- Exclude: None
- Hasil: Junction akan di-copy as-is, referensi tetap pointing ke original location

**Kasus 2: Avoid circular references**
- Centang: `/XJ` (Exclude Junction)
- Hasil: Semua junction diabaikan, hanya regular files dan folders di-copy
- Aman untuk: Network shares, system folders dengan circular junctions

**Kasus 3: Copy hanya file (skip symlinks)**
- Centang: `/XJF` (Exclude File Junction)
- Hasil: File junctions di-skip, tapi directory junctions dan file regular tetap di-copy

---

## Configuration File

### File Lokasi
- **File Name**: `config.conf`
- **Lokasi**: Di folder yang sama dengan aplikasi
- **Format**: JSON

### Contoh config.conf
```json
{
  "source": "C:\\Users\\user\\Documents\\Source",
  "destination": "\\\\server\\backup\\Documents",
  "copy_subdirs": true,
  "copy_empty": false,
  "copy_attributes": true,
  "copy_security": false,
  "copy_all_info": false,
  "recurse": false,
  "multi_thread": true,
  "multi_thread_num": 8,
  "move_files": false,
  "purge": true,
  "mirror": false,
  "include_files": "*.txt;*.docx",
  "exclude_files": "*.tmp;Thumbs.db",
  "exclude_dirs": ".git;node_modules",
  "max_age_check": false,
  "max_age_spin": 30,
  "retry_count": 1,
  "retry_wait": 30,
  "verbose": false,
  "log_only": false,
  "log_file_check": true,
  "log_file_input": "robocopy_log.txt",
  "copy_junction": false,
  "copy_symlink": false,
  "exclude_junction": false,
  "exclude_junction_dir": false,
  "exclude_junction_file": false
}
```

### Auto-Save Behavior
- Konfigurasi **otomatis disimpan** saat:
  - Klik tombol **"Save Config"**
  - Proses copy **selesai** (sukses atau error)
- Konfigurasi **otomatis dimuat** saat:
  - Aplikasi **dibuka** (pertama kali)

### Edit Manual config.conf
1. Close aplikasi
2. Edit `config.conf` dengan text editor (Notepad, VS Code, dll)
3. Simpan file
4. Buka aplikasi lagi

---

## Troubleshooting

### Aplikasi tidak buka
**Error**: `ModuleNotFoundError: No module named 'PyQt5'`

**Solusi**:
```powershell
pip install PyQt5
# atau
pip install --upgrade PyQt5
```

---

### Icon tidak muncul
**Problem**: Application window tidak punya icon

**Solusi**:
1. Pastikan file `favicon.ico` atau `logo.png` ada di folder aplikasi
2. Ukuran minimal 32x32 piksel
3. Format harus .ico atau .png
4. Nama file harus `favicon.ico`, `logo.png`, atau `icon.png`

---

### Robocopy tidak ditemukan
**Error**: `'robocopy' is not recognized as an internal or external command`

**Solusi**:
- Robocopy adalah built-in utility Windows
- Biasanya ada di `C:\Windows\System32\robocopy.exe`
- Jika tidak ada, install Windows Resource Kit atau gunakan built-in robocopy dari Windows Vista+

---

### Stop button tidak bekerja
**Problem**: Proses tidak berhenti saat klik Stop

**Solusi**:
- Aplikasi mengirim signal SIGTERM ke process
- Robocopy akan gracefully shutdown
- Jika masih tidak berhenti, cek di Task Manager dan kill `robocopy.exe` manual
- Note: Windows PowerShell mungkin require admin privileges

---

### Config tidak disimpan
**Problem**: Setting tidak tersimpan ke config.conf

**Solusi**:
1. Pastikan folder aplikasi punya write permission
2. Coba run aplikasi dengan administrator privilege
3. Check apakah file `config.conf` existing dan bisa ditulis
4. Restart aplikasi

---

### UNC Path tidak bekerja
**Problem**: Network path (\\\\server\\share) tidak copy dengan benar

**Solusi**:
1. Pastikan network path accessible: `net use \\server\share`
2. Gunakan credential yang proper
3. Check firewall dan network permissions
4. Coba dengan administrator privilege
5. Test dengan "List Only" (/L) dulu

---

### File dalam penggunaan tidak bisa di-copy
**Error**: `ERROR 32 (0x00000020) Sharing Violation`

**Solusi**:
1. Close semua aplikasi yang use file tersebut
2. Run robocopy dengan administrator privilege
3. Gunakan /COPYALL flag untuk force copy
4. Try copy di lain waktu ketika files tidak digunakan

---

### Log file terlalu besar
**Problem**: Log file mencapai GB

**Solusi**:
1. Use "Include Files" dan "Exclude Files" untuk limit copy
2. Regular cleanup old log files
3. Redirect log ke network location dengan more space
4. Use "/V" sparse (hanya run dengan verbose ketika debug)

---

## Command Line Examples

### Basic Mirror Copy
```
robocopy "C:\Source" "D:\Backup" /S /E /COPY:DAT
```

### Network Backup dengan Retry
```
robocopy "C:\Documents" "\\server\backup\docs" /MIR /MT:8 /R:3 /W:60 /LOG:"backup.log"
```

### Select File Types
```
robocopy "C:\Project" "D:\Backup" *.txt *.docx *.pdf /S /COPY:DAT
```

### Exclude Development Files
```
robocopy "C:\Dev" "D:\Backup" /S /E /XD ".git" "node_modules" "__pycache__" /XF "*.tmp" "*.log"
```

### List Only (Dry Run)
```
robocopy "C:\Source" "D:\Destination" /S /E /L /V /LOG:"preview.txt"
```

---

## Kontak & Support

Untuk pertanyaan atau bug report, silakan hubungi development team melalui internal support channel.

---

## Changelog

### Version 3.0.2 (February 13, 2026) - LATEST ⭐⭐
**Part 6 Revisi 2: Confirmation Dialog for Drag-Drop**

- **NEW**: Confirmation Dialog
  - Shows source paths with numbered list (max 5)
  - Shows destination path clearly
  - Shows direction (Source → Destination or Destination → Source)
  - Displays "... dan X item lainnya" for extra items
  - User can click OK to proceed or Cancel to abort
  - Default button is Cancel (safer)

- **IMPROVED**: Safety & Control
  - No more accidental copies
  - User can review source/destination before copy
  - Clear visual confirmation before execution
  - Full user control over copy operations

- **MAINTAINED**: All Features From v3.0.1
  - Drag-drop copy works perfectly
  - Multi-select files/folders
  - Sequential copy execution
  - Settings preserved

**Documentation**:
- PART6_REVISI2_FEATURES.md (confirmation dialog details)
- PART6_REVISI2_SUMMARY.md (comprehensive implementation)

**Testing**: ✅ 5/5 test cases pass

---

### Version 3.0.1 (February 13, 2026)
**Part 6 Revision: Fixed Drag-Drop & Multi-Select**

- **FIXED**: Drag-drop functionality
  - Was broken in v3.0.0, now fully working
  - Proper MIME data handling (URL format + text fallback)
  - Works with single and multiple files/folders

- **NEW**: Multi-Select File Support
  - Extended selection mode (Ctrl+Click, Shift+Click)
  - Range selection with Shift+Click

  - Visual highlight for selected items
  - Select all with Ctrl+A

- **NEW**: Multiple File Drag-Drop
  - Drag multiple selected files to other pane
  - Sequential copy execution (0.5s delay between)
  - Each item copied with preserved settings
  - Clear logging for each operation

- **IMPROVED**: MIME Data Handling
  - URL format (file:///) for better compatibility
  - Text fallback format support
  - Proper path encoding and parsing
  - Enhanced error handling

- **IMPROVED**: Error Handling & Validation
  - Path validation before copy
  - User-friendly error dialogs
  - Clear error messages
  - Graceful failure handling

- **MAINTAINED**: 100% backward compatibility
  - All v3.0.0 features still work
  - Config files compatible
  - Settings preserved
  - No breaking changes

**Documentation**:
- PART6_REVISION_FEATURES.md (600+ lines)
- PART6_REVISION_IMPLEMENTATION.md (900+ lines)
- PART6_REVISION_QUICK_START.md (650+ lines)
- CHANGELOG_PART6_REVISION.md (450+ lines)
- PART6_REVISION_SUMMARY.md (comprehensive)

**Testing**: ✅ 22/22 tests pass

---

### Version 3.0.0 (February 12, 2026)
- **NEW**: Context Menu Integration
  - Right-click file/folder untuk quick actions
  - Rename, Delete, Open in Explorer options
  - Confirmation dialogs untuk safety
  - Duplicate name prevention
  - Permission error handling

- **NEW**: File Operations
  - Rename files/folders dengan input dialog
  - Delete dengan confirmation (prevents accidents)
  - Recursive delete untuk folders
  - Auto-refresh after operations
  - User-friendly error messages

- **NEW**: Drag & Drop Copy
  - Drag files from Source to Destination pane
  - Bidirectional (Source↔Destination)
  - Automatic robocopy triggering
  - Respects ALL configured settings:
    - Multi-threading, filters, flags, options
    - Retry configuration, logging setup
  - Visual feedback during drag
  - Real-time progress display
  - No button press needed

- **NEW**: FileListWidget Class
  - Custom QListWidget dengan context menu support
  - Drag-drop event handling
  - File operation methods
  - Signal-based architecture

- **IMPROVED**: File Management Workflow
  - Integrated file operations
  - No external tools needed
  - Professional user experience
  - Faster copy operations

- **MAINTAINED**: 100% backward compatibility
  - All existing features still work
  - Old configurations load correctly
  - No API changes
  - Pure additive features

### Version 2.0.0 (February 12, 2026)
- **NEW**: Dual-pane file explorer interface
  - Professional side-by-side layout untuk Source & Destination
  - FileExplorerWidget class untuk reusable file explorer
  - Double-click navigation dengan full history tracking
  - Back button dan parent folder (..) support
  - File/folder listing dengan emoji icons berdasarkan file type
  - Statistics display (folder count, file count, total size)
  - Size auto-conversion (B→KB→MB→GB→TB)
- **IMPROVED**: Source & Destination tab UX
  - More intuitive folder exploration
  - Better visual feedback dengan icons
  - Faster navigation dengan history
- **MAINTAINED**: 100% backward compatibility
  - All existing features masih berfungsi
  - Old configurations masih load correctly
  - No breaking changes to API

### Version 1.0.0 (February 2026)
- **PART 4 FEATURES**: Initial major update
  - Browse to Last Folder (smart path memory)
  - Animated Gradient Background during copy
  - Animation configuration dalam config.conf
  - Performance optimizations
  
- **PART 1-3 FEATURES**: Core functionality
  - Support all robocopy major parameters
  - Configuration persistence
  - Icon support
  - About tab dengan info aplikasi
  - Real-time output logging
  - Process control (stop)

---

**Last Updated**: February 2026  
**License**: Internal Use  
**Repository**: SCProvision/PYTHON/robocopy-ui
