# Contoh Generated Commands - Junction & Symbolic Links Feature

## Test Case 1: Hanya /SJ (Copy Junction)
**Opsi yang diaktifkan:**
- Source: `C:\TestFolder`
- Destination: `D:\Backup`
- Copy Junction: ✓ checked
- Copy Subdirectories (/S): ✓ checked

**Generated Command:**
```
robocopy "C:\TestFolder" "D:\Backup" *.* /S /SJ /R:1 /W:30
```

**Penjelasan:** Junction dan symlink akan di-copy sebagai link itu sendiri, tidak mengikuti target.

---

## Test Case 2: Hanya /SL (Copy Symbolic Link)
**Opsi yang diaktifkan:**
- Source: `\\server\share`
- Destination: `E:\NetworkBackup`
- Copy Symbolic Link: ✓ checked
- Copy Subdirectories (/S): ✓ checked
- Multi-thread: ✓ 4 threads

**Generated Command:**
```
robocopy "\\server\share" "E:\NetworkBackup" *.* /S /SL /MT:4 /R:1 /W:30
```

**Penjelasan:** Symbolic links akan di-copy sebagai symlink, bukan target file-nya.

---

## Test Case 3: /XJ (Exclude All Junctions)
**Opsi yang diaktifkan:**
- Source: `C:\ComplexFolder`
- Destination: `D:\SafeBackup`
- Exclude Junction: ✓ checked
- Copy Subdirectories (/S): ✓ checked
- Exclude Files: `*.tmp;*.log`

**Generated Command:**
```
robocopy "C:\ComplexFolder" "D:\SafeBackup" *.* /S /XJ /XF "*.tmp" /XF "*.log" /R:1 /W:30
```

**Penjelasan:** Semua junction points akan diabaikan, mencegah infinite loops.

---

## Test Case 4: /XJD (Exclude Directory Junctions Only)
**Opsi yang diaktifkan:**
- Source: `C:\MixedFolder`
- Destination: `D:\Backup`
- Exclude Directory Junction: ✓ checked
- Copy Subdirectories (/S): ✓ checked

**Generated Command:**
```
robocopy "C:\MixedFolder" "D:\Backup" *.* /S /XJD /R:1 /W:30
```

**Penjelasan:** Hanya directory junctions yang diabaikan. File junctions dan regular files tetap di-copy.

---

## Test Case 5: /XJF (Exclude File Junctions Only)
**Opsi yang diaktifkan:**
- Source: `C:\MixedFolder`
- Destination: `D:\Backup`
- Exclude File Junction: ✓ checked
- Copy Subdirectories (/S): ✓ checked

**Generated Command:**
```
robocopy "C:\MixedFolder" "D:\Backup" *.* /S /XJF /R:1 /W:30
```

**Penjelasan:** Hanya file junctions yang diabaikan. Directory junctions dan regular files tetap di-copy.

---

## Test Case 6: Combined - /SJ + /MT + /MIR
**Opsi yang diaktifkan:**
- Source: `C:\Development\Projects`
- Destination: `\\backup-server\projects`
- Copy Junction: ✓ checked
- Mirror: ✓ checked
- Multi-thread: ✓ 8 threads
- Verbose: ✓ checked

**Generated Command:**
```
robocopy "C:\Development\Projects" "\\backup-server\projects" *.* /MIR /SJ /MT:8 /V /R:1 /W:30
```

**Penjelasan:** 
- `/MIR`: Mirror mode (sync source dan destination)
- `/SJ`: Junction akan di-copy as-is
- `/MT:8`: 8 threads untuk paralel copying
- `/V`: Verbose output untuk melihat detail

---

## Test Case 7: Complex Real-World Scenario
**Opsi yang diaktifkan:**
- Source: `C:\UserData`
- Destination: `\\nas\backups\UserData`
- Copy Subdirectories (/S): ✓ checked
- Exclude Junction: ✓ checked
- Exclude Files: `*.tmp;*.bak;Thumbs.db`
- Exclude Dirs: `.git;node_modules;__pycache__`
- Multi-thread: ✓ 4 threads
- Verbose: ✓ checked
- Log to File: ✓ checked (`backup_log.txt`)
- Retry: 3 attempts, 60 seconds wait

**Generated Command:**
```
robocopy "C:\UserData" "\\nas\backups\UserData" *.* /S /XJ /XF "*.tmp" /XF "*.bak" /XF "Thumbs.db" /XD ".git" /XD "node_modules" /XD "__pycache__" /MT:4 /V /LOG:"backup_log.txt" /R:3 /W:60
```

**Penjelasan:**
- Backup dengan exclude junctions untuk avoid circular references
- Skip temporary dan metadata files
- Skip version control dan dependency folders
- 4 threads untuk network performance
- Verbose logging dengan file output
- 3 retries dengan 60 second wait untuk network resilience

---

## Test Case 8: Symlink Preservation (Advanced)
**Opsi yang diaktifkan:**
- Source: `C:\LinkCollection`
- Destination: `D:\LinkBackup`
- Copy Symbolic Link: ✓ checked
- Copy Junction: ✓ checked
- Copy Subdirectories (/S): ✓ checked
- Mirror: ✓ checked

**Generated Command:**
```
robocopy "C:\LinkCollection" "D:\LinkBackup" *.* /S /MIR /SJ /SL /R:1 /W:30
```

**Penjelasan:**
- `/SJ`: Junction di-copy as-is
- `/SL`: Symbolic links di-copy as-is
- `/MIR`: Synchronize dengan delete
- Hasil: Perfect replica dengan semua links intact

---

## Rumusan Command Building Logic

```
Base Command: robocopy "SOURCE" "DESTINATION" FILEPATTERNS

+ Copy Options (/S, /E, /MIR, /MOVE, /PURGE, /COPYALL)
+ Attributes Options (/COPY:DAT, /SEC)
+ Multi-threading (/MT:N)
+ Retry Options (/R:N, /W:N)
+ File Filters (/XF, /XD, /MAXAGE)
+ [NEW] Junction/Link Options (/SJ, /SL, /XJ, /XJD, /XJF)  <-- Position in command
+ Logging Options (/V, /L, /LOG)
```

Position penting: Junction/Link options ditempatkan setelah exclude filters dan sebelum logging options untuk consistency.

---

## Testing Recommendations

### Unit Test untuk Junction Options:
1. Verify setiap checkbox generate parameter yang benar
2. Verify kombinasi parameters valid
3. Verify config save/load works untuk junction options
4. Test actual robocopy execution dengan test folders

### Integration Test:
1. Test dengan folder yang contain actual junctions/symlinks
2. Compare output dengan expected robocopy behavior
3. Verify log files mencatat junction handling correctly

### Edge Cases:
1. Circular junctions dengan /XJ
2. Mixed junctions dan symlinks
3. Network paths dengan junctions
4. Combination dengan mirror mode

---

**Version**: 1.0.0 - Part 2
**Date**: February 2026
