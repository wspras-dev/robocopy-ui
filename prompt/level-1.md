Saya akan membuat aplikasi GUI PyQt5 untuk menjalankan robocopy.exe dengan parameter yang dapat dikonfigurasi. Pertama, mari saya lihat file yang sudah ada.

Read rbcopy-plus.py

Saya akan membuat aplikasi GUI PyQt5 lengkap untuk menjalankan robocopy.exe dengan antarmuka yang user-friendly. Aplikasi ini akan memungkinkan Anda untuk mengatur semua parameter penting robocopy.

Created rbcopy-plus.py

Sempurna! Saya telah membuat aplikasi GUI PyQt5 lengkap untuk Robocopy. Berikut fitur-fiturnya:

Fitur Utama:
📁 Tab Source & Destination
Browse folder source dan destination
Path input validation
📋 Tab Copy Options
/S - Copy subdirectories
/E - Copy empty subdirectories
/MIR - Mirror folder
/MOVE - Move files (delete after copy)
/PURGE - Delete files tidak ada di source
Copy attributes (Data, Attributes, Timestamps, Security)
Multi-threading support (1-128 threads)
🔍 Tab File Selection
Include file patterns (contoh: *.txt;*.docx)
Exclude file patterns
Exclude directories (contoh: .git;node_modules)
Filter by file age (days)
⚙️ Tab Retry & Logging
Configurate retry attempts (0-32767)
Wait time between retries
Verbose logging
List only mode (simulasi)
Save log to file
🖥️ Fitur Tambahan
Real-time output log dengan timestamp
Multi-threaded execution (UI tidak freeze)
Copy command ke clipboard
Clear log button
Exit code reporting
Cara Menggunakan:
Install PyQt5 (jika belum):
Jalankan aplikasi:
Fill parameters:
Pilih source & destination folder
Configure copy options sesuai kebutuhan
Run dengan tombol "Run Robocopy"
Aplikasi akan menjalankan robocopy.exe dengan semua parameter yang Anda konfigurasi melalui GUI!