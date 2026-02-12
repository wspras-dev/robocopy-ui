# PART 6 QUICK START - Context Menu, Rename/Delete, Drag-Drop

**Date**: February 12, 2026  
**Version**: 3.0.0  

---

## ⚡ 30-Second Overview

Part 6 adds three file management features:

1. **Right-click menu** untuk rename, delete, dan buka di Explorer
2. **Rename & Delete** operations dengan confirmation dialogs
3. **Drag-drop** dari source ke destination untuk automatic copy

---

## 🎯 Quick Examples

### Example 1: Rename File

**Scenario**: File named "documennt.txt" needs correction

```
1. Open Source & Destination tab
2. Right-click "documennt.txt" dalam file list
3. Select "✏️ Rename"
4. Dialog appears:
   ┌─────────────────────────────┐
   │ Rename 'documennt.txt' to:  │
   │ [documennt.txt           ▼] │
   │         [OK]  [Cancel]      │
   └─────────────────────────────┘
5. Clear text, type: "document.txt"
6. Click OK
7. File renamed instantly ✅
8. List updates automatically
```

---

### Example 2: Delete Folder

**Scenario**: Old backup folder "old_backup_2024" needs removal

```
1. Open Source & Destination tab
2. Right-click "old_backup_2024" (folder)
3. Select "🗑️ Delete"
4. Confirmation dialog:
   ┌──────────────────────────────────────┐
   │ Confirm Delete                       │
   │ Apakah Anda yakin ingin menghapus    │
   │ 'old_backup_2024' (dan semua isinya) │
   │        [Yes]  [No]                   │
   └──────────────────────────────────────┘
5. Click Yes
6. Folder deleted recursively ✅
7. List updates automatically
```

---

### Example 3: Drag-Drop Copy

**Scenario**: Copy specific files dengan configured settings

```
SETUP:
1. Open Source & Destination tab
2. Navigate Source to: C:\MyFiles
3. Navigate Destination to: D:\Backup
4. Configure options:
   - Copy Options tab: Enable /MT:8 (8 threads)
   - File Selection tab: Include: *.docx;*.xlsx
   - Retry & Logging: Max Retries: 3

DRAG-DROP:
5. In Source list, see file: "Report.xlsx" (📊)
6. Drag file → Destination pane
   ┌─────────────────┐      ┌─────────────┐
   │ Source          │      │ Destination │
   │ 📁 MyFiles      │      │ 📁 Backup   │
   │ 📄 Docs.docx    │      │ (drop here) │
   │ 📊 Report.xlsx  │ ──→  │             │
   │ 🖼️ Photo.jpg    │      │             │
   └─────────────────┘      └─────────────┘
7. Drop (mouse button up)
8. Robocopy starts automatically with:
   - Source: C:\MyFiles
   - Destination: D:\Backup
   - Filters: *.docx;*.xlsx
   - Threads: 8
   - Retries: 3
   - ALL configured settings ✅
9. Progress dialog shows:
   ┌──────────────────────────┐
   │ Robocopy in Progress     │
   │ Copying: Report.xlsx     │
   │ [████████░░░░░░░░░░] 40% │
   │      [⏹ Stop]            │
   └──────────────────────────┘
10. Copy completes
11. Success message ✅
12. Lists refresh automatically
```

---

## 🎓 Features in Detail

### Feature 1: Context Menu (Right-Click)

**Available Actions**:
```
┌─────────────────────────────┐
│ ✏️  Rename       [Ctrl+F2]   │
│ 🗑️  Delete       [Delete]    │
│ ─────────────────────────    │
│ 📁 Open in Explorer          │
└─────────────────────────────┘
```

**How to use**:
```
1. Right-click any file/folder dalam list
2. Menu appears instantly
3. Select action
4. Dialog or operation proceeds
5. Result: auto-refresh
```

**Keyboard Shortcuts** (Coming in future):
- Ctrl+F2: Rename
- Delete key: Delete

---

### Feature 2: Rename File/Folder

**When to use**:
- Fix typos dalam filenames
- Standardize naming conventions
- Organize file structure
- Rename batches (one at a time)

**Steps**:
```
1. Right-click file → "✏️ Rename"
2. Dialog shows current name
3. Edit name (keep extension if possible)
4. Click OK
5. Validation:
   ✓ Name exists? → Error + cancel
   ✓ Permission? → Error + cancel
   ✓ OK? → Rename + refresh
```

**Error Cases**:
```
Case 1: Name already exists
├─ User: Type "document.txt"
├─ System: Check if exists
├─ Result: Error dialog
└─ Action: Manual edit required

Case 2: File in use/locked
├─ User: Try to rename
├─ System: Check rename permission
├─ Result: Error dialog
└─ Action: Close file, try again

Case 3: Success
├─ User: Type new name
├─ System: No conflicts
├─ Result: Success message
└─ Action: List refreshed
```

---

### Feature 3: Delete File/Folder

**When to use**:
- Remove temporary files
- Clean up old backups
- Delete unwanted folders
- Organize file structure

**Steps**:
```
1. Right-click file/folder → "🗑️ Delete"
2. Confirmation dialog
   - For files: "Delete 'filename'?"
   - For folders: "Delete 'foldername' (and all contents)?"
3. Review message carefully
4. Click Yes = proceed, No = cancel
5. Deletion:
   ✓ Permission? → Delete
   ✓ In use? → Error
   ✓ Success → Refresh list
```

**Safety Features**:
```
Confirmation dialog (prevents accidents)
Warning for folders (shows will delete contents)
Error messages (explains why if fails)
Auto-refresh (shows updated list)
```

**Examples**:

```
Example A: Delete single file
─────────────────────────────
File: Resume_old.docx
Action: Right-click → Delete
Dialog: "Delete 'Resume_old.docx'?"
Result: Deleted ✅

Example B: Delete folder tree
──────────────────────────────
Folder: Backups/2023 (contains 50+ files)
Action: Right-click → Delete
Dialog: "Delete 'Backups/2023' (and all contents)?"
Result: Entire tree deleted recursively ✅
```

---

### Feature 4: Drag-Drop Copy

**When to use**:
- Quick copy operations
- Apply configured settings automatically
- Copy with multi-threading
- Leverage filter patterns
- Batch file operations

**Setup (One-time)**:
```
1. Open Copy Options tab
   ✓ Enable multi-threading (/MT:8)
   ✓ Enable mirror if needed
   ✓ Other flags as needed

2. Open File Selection tab
   ✓ Set include patterns
   ✓ Set exclude patterns
   ✓ Age filters if needed

3. Open Retry & Logging tab
   ✓ Set retry count (recommended: 3)
   ✓ Enable logging if desired
```

**Usage**:
```
1. Source pane: Navigate to C:\MyFiles
2. Destination pane: Navigate to D:\Backup
3. See files listed in both panes
4. Position windows side-by-side (or use splitter)
5. Find file to copy in Source list
6. Drag file toward Destination pane
7. Cursor changes to copy indicator (✓)
8. Release mouse over Destination pane
9. Robocopy triggers automatically! ✅
10. Progress displays realtime
11. Success when done
12. Lists refresh automatically
```

**Visual Indication**:
```
Before drag:
┌─────────────────────────────────────┐
│ Source                Destination   │
├──────────┬──────────────────────────┤
│ 📄 file  │ (empty)                  │
└──────────┴──────────────────────────┘

During drag:
┌─────────────────────────────────────┐
│ Source                Destination   │
├──────────┬──────────────────────────┤
│ 📄 file ~│ ✓ (drop here)            │
│   ↓↓     │                          │
└──────────┴──────────────────────────┘

After drop:
┌─────────────────────────────────────┐
│ Robocopy running...                  │
│ [████████░░░░░░░░░░░░░░░░░░] 35%   │
└─────────────────────────────────────┘

Completed:
┌─────────────────────────────────────┐
│ Source                Destination   │
├──────────┬──────────────────────────┤
│ 📄 file  │ 📄 file ✅              │
└──────────┴──────────────────────────┘
```

---

## ⚙️ Configuration

### Default Behavior

**Context Menu**:
- Always available
- No configuration needed
- Uses OS defaults for operations

**Rename/Delete**:
- No configuration
- Uses OS file permissions
- Confirmation dialogs built-in

**Drag-Drop**:
- Uses current robocopy settings
- Inherits all configured options
- No additional setup beyond robocopy config

### Applied Settings

When drag-drop triggers copy, these settings apply:

```python
# From Copy Options tab
- Copy flags (/S, /E, /MIR, /MOVE, /PURGE)
- Attributes (/COPY:DAT, /SEC, /COPYALL)
- Multi-threading (/MT:N)

# From File Selection tab
- Include patterns
- Exclude patterns
- File age filters

# From Retry & Logging tab
- Retry count (/R:N)
- Retry wait (/W:N)
- Verbose logging (/V)
- List only (/L)

# From Junction & Links tab
- Copy junction (/SJ)
- Copy symbolic link (/SL)
- Exclude junction options
```

---

## 🔧 Troubleshooting

### Context Menu Not Showing

**Problem**: Right-click doesn't show menu

**Solution**:
```
1. Click item to select it first
2. Then right-click
3. Menu should appear

If still not working:
- Verify you're right-clicking actual list item
- Check that list isn't empty
- Try refreshing list first
```

---

### Rename Not Working

**Problem**: "Gagal rename" error message

**Causes & Solutions**:
```
✗ File already exists with that name
  → Use different name
  → Delete existing file first

✗ File is locked/in use
  → Close file in other applications
  → Wait for antivirus scan to complete
  → Try again

✗ Permission denied
  → Run as Administrator
  → Check folder permissions
  → Try on different drive
```

---

### Delete Not Working

**Problem**: "Gagal hapus" error message

**Causes & Solutions**:
```
✗ File in use (locked)
  → Close in other apps
  → Try different file
  → Try again

✗ Permission denied
  → Run as Administrator
  → Check file/folder permissions
  → Check antivirus locks

✗ Folder not empty
  → Delete files inside first
  → Use shutil (automatic in app)
```

---

### Drag-Drop Not Triggering Copy

**Problem**: Drag-drop doesn't start robocopy

**Causes & Solutions**:
```
✗ Source path not set
  → Navigate/set source in left pane
  → Verify path is valid folder

✗ Destination path not set
  → Navigate/set destination in right pane
  → Verify path is valid folder

✗ Dropped on wrong area
  → Drop directly on destination pane
  → Not on tab or outside

✗ File doesn't exist
  → Refresh list first
  → Check if file still there
  → Try different file

✗ Copy settings not configured
  → Set minimum: source + destination
  → Other settings have defaults
  → Copy proceeds with current settings
```

---

## 💡 Tips & Tricks

### Tip 1: Quick Organization

```
Use rename + drag-drop for fast organization:

1. Source: Downloads folder (messy)
2. Destination: Documents folder (organized)
3. Rename files to standardized format
4. Drag organized files to destination
5. Copy with filters (e.g., documents only)
6. Result: Clean, organized backup
```

### Tip 2: Batch Operations

```
For multiple files, repeat quickly:

1. Configure settings once
2. For each file:
   a. Rename if needed
   b. Drag to destination
   c. Wait for completion
   d. Move to next file
```

### Tip 3: Safe Deletion

```
Before deleting important folders:

1. Check folder in explorer manually
2. Read error message carefully
3. Verify you have backup
4. Then confirm deletion
5. Don't use undo (deleted permanently)
```

### Tip 4: Drag-Drop Efficiency

```
Maximize drag-drop speed:

1. Keep Source + Dest panes visible (splitter)
2. Set up all options first
3. Multiple drag-drops reuse settings
4. No need to re-configure each time
5. Just drag → drop → watch → repeat
```

---

## 🎓 Best Practices

| Practice | ✅ Do | ❌ Don't |
|----------|------|---------|
| **Backup** | Backup before delete | Delete unique files |
| **Confirm** | Read dialogs carefully | Click OK without reading |
| **Settings** | Configure once | Change mid-operation |
| **Drag-drop** | Drop on pane itself | Drag outside boundaries |
| **Rename** | Use meaningful names | Ultra-long filenames |
| **Delete** | Review first | Delete system folders |

---

## 🚀 Next Steps

1. **Try context menu**: Right-click any file
2. **Test rename**: Change a test filename
3. **Test delete**: Delete a test file
4. **Configure copy**: Set up robocopy options
5. **Try drag-drop**: Drag test file between panes
6. **Monitor progress**: Watch robocopy output
7. **Verify results**: Check destination folder

---

## 📚 More Information

- See **PART6_FEATURES.md** for detailed feature documentation
- See **PART6_IMPLEMENTATION.md** for technical details
- See **README.md** for overall application info

---

**Version**: 3.0.0  
**Status**: ✅ Production Ready
