# Part 6 Revision - Quick Start Guide

**Updated**: February 13, 2026  
**Version**: 3.0.1  

---

## 🎯 What's New?

### ✨ Fixed & New Features

| Feature | v3.0.0 | v3.0.1 |
|---------|--------|--------|
| Drag-drop 1 file | ❌ Broken | ✅ Works |
| Multi-select files | ❌ No | ✅ Yes |
| Drag multiple files | ❌ No | ✅ Yes |
| Copy settings preserve | ✅ Yes | ✅ Yes |
| Context menu | ✅ Yes | ✅ Yes |

---

## 🚀 Getting Started

### Installation

1. **Download v3.0.1**
   ```
   File: rbcopy-plus.py
   Version: 3.0.1
   Size: ~50 KB
   ```

2. **Run Application**
   ```bash
   python rbcopy-plus.py
   ```

3. **No Additional Dependencies**
   - Uses same PyQt5 as before
   - No new package requirements

---

## 📖 How to Use

### Example 1: Copy 1 File

**Scenario**: Copy `document.pdf` from Source to Destination

**Steps**:
```
1. Navigate Source tab to folder with document.pdf
2. Click document.pdf (single click)
3. Drag document.pdf to Destination pane
4. Robocopy executes automatically
5. File copied to Destination
```

**Result**:
```
✅ document.pdf copied
✅ Log shows copy progress
✅ Destination explorer refreshes
```

---

### Example 2: Copy Multiple Files

**Scenario**: Copy 3 files (file1.txt, file2.doc, file3.pdf)

**Steps**:
```
1. Navigate Source tab to folder with 3 files

2. Select file1.txt
   Click: file1.txt

3. Add file2.doc to selection
   Hold Ctrl + Click: file2.doc

4. Add file3.pdf to selection
   Hold Ctrl + Click: file3.pdf

5. Observe: All 3 highlighted (selected)

6. Drag any selected file to Destination pane
   Hold left mouse → drag → release on Destination

7. Robocopy executes 3 times (sequential)
   - Copy file1.txt ... (2s)
   - Copy file2.doc ... (2s)
   - Copy file3.pdf ... (2s)

8. All 3 files in Destination
```

**Result**:
```
✅ 3 files copied sequentially
✅ 0.5s delay between each copy
✅ Settings applied to all 3
✅ Log shows all operations
✅ Total time: ~7 seconds
```

---

### Example 3: Copy Folder + Files

**Scenario**: Copy folder1/ + file.txt + document.doc

**Steps**:
```
1. Navigate Source to folder containing all 3

2. Select folder1/
   Click: folder1/

3. Add file.txt
   Hold Ctrl + Click: file.txt

4. Add document.doc
   Hold Ctrl + Click: document.doc

5. All 3 items highlighted

6. Drag to Destination pane

7. Robocopy executes 3 times:
   - Copy folder1/ with all contents
   - Copy file.txt
   - Copy document.doc

8. Destination shows folder1/, file.txt, document.doc
```

**Result**:
```
✅ Folder copied (recursive)
✅ Both files copied
✅ Everything in destination
```

---

### Example 4: Range Select (Shift+Click)

**Scenario**: Copy multiple consecutive files

**Files in Source**:
```
file1.txt
file2.doc
folder1/
file3.pdf
file4.xlsx
file5.pptx
```

**Steps**:
```
1. Click file1.txt
   Selected: [file1.txt]

2. Hold Shift + Click file4.xlsx
   Selected: [file1.txt, file2.doc, folder1/, file3.pdf, file4.xlsx]
   (5 items selected - from file1 to file4, continuous)

3. Drag to Destination

4. All 5 items copied sequentially
```

**Result**:
```
✅ 5 items selected (range)
✅ All 5 copied
✅ Order preserved
✅ Folder contents included
```

---

### Example 5: Reverse Copy (Destination → Source)

**Scenario**: Copy from Destination back to Source

**Setup**:
- Source: C:\MyData\ (empty)
- Destination: D:\Backup\ (has file1.txt, file2.doc)

**Steps**:
```
1. Source Explorer: Navigate to C:\MyData\

2. Destination Explorer: Navigate to D:\Backup\

3. In Destination pane, select file1.txt

4. Hold Ctrl + Click file2.doc

5. Both files highlighted

6. Drag to Source pane (left side)

7. Robocopy reverse copy executed:
   - file1.txt copied from Dest → Source
   - file2.doc copied from Dest → Source

8. Both files now in Source folder
```

**Result**:
```
✅ Reverse copy works
✅ Files transferred back to source
✅ All settings apply
✅ Log shows operations
```

---

## ⚙️ Settings & Configuration

### Multi-Select Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Single select | Click file |
| Add to selection | Ctrl + Click |
| Range select | Shift + Click |
| Select all | Ctrl + A |
| Clear selection | Click empty space |

### Copy Settings

All settings still apply to drag-drop copies:

```
Before dragging:
  1. Set /COPY:DAT (Copy Data, Attributes, Timestamps)
  2. Set /R:3 (Retry 3 times)
  3. Set /W:2 (Wait 2 seconds)
  4. Set /MT:8 (8 threads)
  5. Enable /S (subdirectories)

Then drag files
  → All settings apply to each copy
  → Settings shown in robocopy log
```

### Example Configuration

```
Tab: Copy Options
  ✓ /S - Copy Subdirectories
  ✓ /COPY:DAT - Copy Data, Attributes, Timestamps
  ✓ /R:3 - Retry 3 times

Tab: Source & Destination
  Source: C:\MyDocuments\
  Destination: D:\Backup\
  
  Then: Drag 2 files → Both copy with settings
```

---

## 🔍 Visual Guide

### Multi-Select Visual Feedback

**Source Pane Before Selection**:
```
📁 file1.txt
📁 file2.doc
📁 folder1/
📁 file3.pdf
```

**After Ctrl+Click file1 & file3**:
```
📁 ▓▓▓file1.txt▓▓▓    ← HIGHLIGHTED (selected)
📁 file2.doc
📁 folder1/
📁 ▓▓▓file3.pdf▓▓▓    ← HIGHLIGHTED (selected)
```

**Cursor During Drag**:
```
🖱️ →  file1.txt
    + file3.pdf
    
Destination Pane
```

### Log Output Example

```
===== Robocopy Copy Operation 1/3 =====
Source: C:\MyDocuments\file1.txt
Destination: D:\Backup\
Started: 2026-02-13 10:30:45

ROBOCOPY 10.0 :: Robust File Copy for Windows
  
  New File                 1         1.2 MB   file1.txt
  
                Total    Copied   Skipped  Mismatch    FAILED    Extras
    Dirs :         0         0         0         0         0         0
   Files :         1         1         0         0         0         0
   Bytes :    1.2 MB    1.2 MB         0         0         0         0
   Times :   0:00:02   0:00:02                       0:00:00   0:00:00

Finished: 2026-02-13 10:30:47
Status: SUCCESS

===== Robocopy Copy Operation 2/3 =====
Source: C:\MyDocuments\file2.doc
...
```

---

## 🧪 Test Your Setup

### Quick Test Checklist

```
✅ Test 1: Single File
  1. Create C:\Test\Source\ with test.txt
  2. Drag test.txt to destination pane
  3. Verify copied to destination
  
✅ Test 2: Multi-Select
  1. Create C:\Test\Source\ with 3 files
  2. Ctrl+Click all 3 files
  3. Verify all 3 highlighted
  4. Drag to destination
  5. Verify all 3 copied
  
✅ Test 3: Settings Preserved
  1. Set /R:5 in Copy Options
  2. Drag file
  3. Check log for /R:5
```

---

## ❓ FAQ

### Q: Can I drag single file only?
**A**: Yes! Just click 1 file and drag. Works same as v3.0.0.

### Q: What if I select 10 files?
**A**: All 10 copy sequentially with 0.5s delay between each. Total time ≈ 20+ seconds depending on file sizes.

### Q: Can I cancel mid-copy?
**A**: Yes, the "Stop Copy" button works during any robocopy execution.

### Q: Does context menu still work?
**A**: Yes! Right-click still works. Can use rename, delete, open in explorer from context menu.

### Q: What about large folders?
**A**: Works fine! If copying 100+ files, just takes longer but all copy correctly.

### Q: Settings get reset?
**A**: No, all settings saved in config.conf. Close and reopen app, settings still there.

### Q: Can I mix folders and files?
**A**: Yes! Select folder + files and drag together. All copy correctly.

### Q: Reverse copy (dest→source) works?
**A**: Yes! Select files in destination pane, drag to source pane. Reverse copy works.

---

## 🐛 Troubleshooting

### Issue: Drag not starting

**Check**:
- Click file first to select
- Wait 0.5 second before dragging
- Try with single file first

**Fix**:
- Restart application
- Check if folder permissions OK
- Check if source path valid

### Issue: Drop not executing copy

**Check**:
- Verify destination path is set
- Check if destination folder exists
- Check if source path valid

**Fix**:
- Clear destination, set again
- Ensure folder writable
- Check application logs

### Issue: Only 1 file copied when 5 selected

**Check**:
- Verify all 5 files highlighted
- Check if drag covered all items
- Verify destination pane receives drop

**Fix**:
- Try Shift+Click range select
- Try single Ctrl+Click on each
- Verify drop released on pane

---

## 📊 Performance Notes

### Copy Speed

```
Typical: 5 files (1-10 MB each)
  Expected time: 5-15 seconds
  (Depends on file sizes, robocopy options, disk speed)

Large: 50 files or 100+ MB
  Expected time: 2-5 minutes
  (Depends on total size and /S flag)

Very Large: 500+ files or 1+ GB
  Consider: Do not drag all at once
  Better: Copy in batches or use single folder drag
```

### Recommended Usage

```
Per Drag-Drop Session:
  ✅ 1-10 files/folders = Optimal
  ✅ 10-50 files/folders = Good
  ⚠️  50-100 files/folders = Acceptable (may be slow)
  ❌ 100+ files/folders = Not recommended
     → Instead: Drag parent folder, use /S
```

---

## 🔗 Next Steps

1. **Try It Out**
   - Start application
   - Test single file drag
   - Test multi-select
   - Test 5-file drag

2. **Read More**
   - See PART6_REVISION_FEATURES.md for detailed features
   - See PART6_REVISION_IMPLEMENTATION.md for technical details
   - See CHANGELOG_PART6_REVISION.md for all changes

3. **Give Feedback**
   - Report issues you find
   - Suggest improvements
   - Share success stories

---

## 📞 Support

**For Issues**:
- Check PART6_TROUBLESHOOTING.md
- Check logs in application window
- Review copy options settings

**For Questions**:
- See FAQ section above
- Check quick examples at start of this guide
- Review other Part 6 documentation

---

## ✨ Summary

v3.0.1 makes file copying easier:
- ✅ Drag 1, 2, 3, or many files
- ✅ Use Ctrl+Click for selections
- ✅ All settings still apply
- ✅ Fast and responsive
- ✅ Easy to use

**Ready to use?** Start with Example 1 or 2 above!
