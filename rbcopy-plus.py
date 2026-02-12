import sys
import subprocess
import threading
import os
import json
import signal
import time
import re
from datetime import datetime, timedelta
from pathlib import Path
import shutil
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QLabel, QLineEdit, QPushButton, QTextEdit, QCheckBox,
    QComboBox, QSpinBox, QFileDialog, QMessageBox, QTabWidget,
    QTableWidget, QTableWidgetItem, QSplitter, QProgressBar, QScrollArea,
    QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QSize, QTimer
from PyQt5.QtGui import QIcon, QFont, QColor, QTextCursor, QPixmap, QLinearGradient, QPainter, QBrush


class FileExplorerWidget(QWidget):
    """Widget untuk menampilkan file dan folder explorer dengan dual-pane layout"""
    path_changed = pyqtSignal(str)  # Signal ketika user navigate folder
    
    def __init__(self, initial_path="", parent=None):
        super().__init__(parent)
        self.current_path = initial_path
        self.history = []
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI dengan navigation dan file listing"""
        layout = QVBoxLayout()
        
        # Navigation bar
        nav_layout = QHBoxLayout()
        self.path_label = QLineEdit()
        self.path_label.setReadOnly(False)
        self.path_label.setText(self.current_path)
        self.path_label.textChanged.connect(self.on_path_changed)
        
        self.back_button = QPushButton("◀ Back")
        self.back_button.setMaximumWidth(100)
        self.back_button.clicked.connect(self.go_back)
        self.back_button.setEnabled(len(self.history) > 0)
        
        self.refresh_button = QPushButton("🔄 Refresh")
        self.refresh_button.setMaximumWidth(100)
        self.refresh_button.clicked.connect(self.load_files)
        
        nav_layout.addWidget(QLabel("Path:"))
        nav_layout.addWidget(self.path_label, 1)
        nav_layout.addWidget(self.back_button)
        nav_layout.addWidget(self.refresh_button)
        layout.addLayout(nav_layout)
        
        # File list
        self.file_list = QListWidget()
        self.file_list.itemDoubleClicked.connect(self.on_item_double_clicked)
        layout.addWidget(self.file_list)
        
        # Statistics
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("background-color: #f0f0f0; padding: 5px; border-radius: 3px;")
        layout.addWidget(self.stats_label)
        
        self.setLayout(layout)
        self.load_files()
    
    def on_path_changed(self):
        """Handle path change via text input"""
        new_path = self.path_label.text().strip()
        if new_path and new_path != self.current_path:
            if os.path.isdir(new_path):
                self.history.append(self.current_path)
                self.current_path = new_path
                self.back_button.setEnabled(True)
                self.load_files()
                self.path_changed.emit(self.current_path)
    
    def load_files(self):
        """Load dan tampilkan files/folders dari current_path"""
        try:
            if not os.path.isdir(self.current_path):
                self.file_list.clear()
                self.stats_label.setText("Invalid path")
                return
            
            self.file_list.clear()
            
            # Parent folder (..)
            if self.current_path != os.path.splitdrive(self.current_path)[0]:
                parent_item = QListWidgetItem("📁 ..")
                parent_item.setData(Qt.UserRole, ("folder", os.path.dirname(self.current_path)))
                self.file_list.addItem(parent_item)
            
            # Collect folders dan files
            folders = []
            files = []
            total_size = 0
            
            try:
                entries = os.listdir(self.current_path)
                for entry in sorted(entries):
                    full_path = os.path.join(self.current_path, entry)
                    try:
                        if os.path.isdir(full_path):
                            folders.append((entry, full_path))
                        else:
                            try:
                                size = os.path.getsize(full_path)
                                total_size += size
                                files.append((entry, full_path, size))
                            except:
                                files.append((entry, full_path, 0))
                    except:
                        continue
            except PermissionError:
                pass
            
            # Add folders first
            for folder_name, folder_path in folders:
                item = QListWidgetItem(f"📁 {folder_name}")
                item.setData(Qt.UserRole, ("folder", folder_path))
                self.file_list.addItem(item)
            
            # Add files
            for file_name, file_path, file_size in files:
                # Get file extension dan icon
                _, ext = os.path.splitext(file_name)
                icon = self.get_file_icon(ext)
                size_str = self.format_size(file_size)
                
                display_text = f"{icon} {file_name} ({size_str})"
                item = QListWidgetItem(display_text)
                item.setData(Qt.UserRole, ("file", file_path, file_size))
                self.file_list.addItem(item)
            
            # Update statistics
            folder_count = len(folders)
            file_count = len(files)
            total_size_str = self.format_size(total_size)
            
            stats_text = f"Folders: {folder_count} | Files: {file_count} | Total Size: {total_size_str}"
            self.stats_label.setText(stats_text)
            
        except Exception as e:
            self.stats_label.setText(f"Error: {str(e)}")
    
    def on_item_double_clicked(self, item):
        """Handle double-click untuk navigate folder"""
        data = item.data(Qt.UserRole)
        if data[0] == "folder":
            folder_path = data[1]
            if os.path.isdir(folder_path):
                self.history.append(self.current_path)
                self.current_path = folder_path
                self.path_label.setText(self.current_path)
                self.back_button.setEnabled(True)
                self.load_files()
                self.path_changed.emit(self.current_path)
    
    def go_back(self):
        """Navigate ke folder sebelumnya"""
        if self.history:
            self.current_path = self.history.pop()
            self.path_label.setText(self.current_path)
            self.back_button.setEnabled(len(self.history) > 0)
            self.load_files()
            self.path_changed.emit(self.current_path)
    
    def set_path(self, path):
        """Set path tanpa menambah history"""
        if os.path.isdir(path):
            self.current_path = path
            self.path_label.setText(path)
            self.load_files()
    
    @staticmethod
    def get_file_icon(extension):
        """Return emoji icon berdasarkan file extension"""
        ext = extension.lower()
        
        # Documents
        if ext in ['.txt', '.doc', '.docx', '.pdf']:
            return "📄"
        # Spreadsheet
        elif ext in ['.xls', '.xlsx', '.csv']:
            return "📊"
        # Images
        elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg']:
            return "🖼️"
        # Videos
        elif ext in ['.mp4', '.avi', '.mkv', '.mov', '.wmv']:
            return "🎬"
        # Audio
        elif ext in ['.mp3', '.wav', '.flac', '.aac', '.m4a']:
            return "🎵"
        # Code
        elif ext in ['.py', '.js', '.java', '.cpp', '.c', '.h', '.html', '.css']:
            return "💻"
        # Archives
        elif ext in ['.zip', '.rar', '.7z', '.tar', '.gz']:
            return "📦"
        # Executables
        elif ext in ['.exe', '.msi', '.bat', '.sh']:
            return "⚙️"
        else:
            return "📃"
    
    @staticmethod
    def format_size(size_bytes):
        """Convert bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} PB"


class AnimationThread(QThread):
    """Thread untuk animasi gradient background saat copy berlangsung"""
    color_change_signal = pyqtSignal(QLinearGradient)
    
    def __init__(self, duration=5000):  # 5 second animation cycle
        super().__init__()
        self.duration = duration
        self.is_running = True
        self.start_time = time.time()
        self.color_palettes = [
            [(255, 100, 100), (255, 200, 100)],   # Red to Orange
            [(255, 200, 100), (100, 200, 255)],   # Orange to Blue
            [(100, 200, 255), (100, 255, 200)],   # Blue to Green
            [(100, 255, 200), (200, 100, 255)],   # Green to Purple
            [(200, 100, 255), (255, 100, 150)],   # Purple to Pink
        ]
        self.current_palette_idx = 0
    
    def run(self):
        while self.is_running:
            elapsed = (time.time() - self.start_time) % (self.duration / 1000)
            progress = (elapsed / (self.duration / 1000)) % 1.0
            
            # Get current and next color palette
            palette = self.color_palettes[self.current_palette_idx]
            next_idx = (self.current_palette_idx + 1) % len(self.color_palettes)
            next_palette = self.color_palettes[next_idx]
            
            # Interpolate colors
            if progress < 0.5:
                # Animate within current palette
                color_progress = progress * 2
                start_color = palette[0]
                end_color = palette[1]
            else:
                # Transition to next palette
                color_progress = (progress - 0.5) * 2
                start_color = palette[1]
                end_color = next_palette[0]
                if color_progress >= 1.0:
                    self.current_palette_idx = next_idx
            
            # Interpolate RGB values
            r1, g1, b1 = start_color
            r2, g2, b2 = end_color
            r = int(r1 + (r2 - r1) * min(color_progress, 1.0))
            g = int(g1 + (g2 - g1) * min(color_progress, 1.0))
            b = int(b1 + (b2 - b1) * min(color_progress, 1.0))
            
            # Create gradient
            gradient = QLinearGradient(0, 0, 0, 1)
            gradient.setColorAt(0, QColor(r, g, b))
            gradient.setColorAt(1, QColor(min(r + 50, 255), min(g + 50, 255), min(b + 50, 255)))
            
            self.color_change_signal.emit(gradient)
            time.sleep(0.05)  # Update every 50ms
    
    def stop(self):
        self.is_running = False


class RobocopyThread(QThread):
    """Thread untuk menjalankan robocopy.exe tanpa freeze GUI"""
    output_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(int)
    error_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)  # Progress percentage
    time_estimate_signal = pyqtSignal(str)  # Time estimation
    file_count_signal = pyqtSignal(int, int)  # Current file, Total files

    def __init__(self, command, enable_progress=True):
        super().__init__()
        self.command = command
        self.process = None
        self.is_paused = False
        self.enable_progress = enable_progress
        self.start_time = None
        self.files_copied = 0
        self.total_files_estimated = 0

    def run(self):
        try:
            self.start_time = time.time()
            self.output_signal.emit(f"[{datetime.now().strftime('%H:%M:%S')}] Menjalankan command:\n{self.command}\n")
            self.output_signal.emit("=" * 80 + "\n")
            
            # Create process dengan NEW_PROCESS_GROUP untuk proper child process management
            self.process = subprocess.Popen(
                self.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                shell=True,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )

            # Track progress dari robocopy output
            for line in self.process.stdout:
                self.output_signal.emit(line)
                
                # Parse robocopy output untuk progress tracking
                if self.enable_progress:
                    self._parse_progress_line(line)

            returncode = self.process.wait()
            self.output_signal.emit("\n" + "=" * 80)
            self.output_signal.emit(f"[{datetime.now().strftime('%H:%M:%S')}] Proses selesai dengan exit code: {returncode}\n")
            self.finished_signal.emit(returncode)
        except Exception as e:
            self.error_signal.emit(f"Error: {str(e)}")
            self.finished_signal.emit(-1)

    def _parse_progress_line(self, line):
        """Parse robocopy output untuk extract progress information"""
        try:
            # Look for file count patterns dalam robocopy output
            if 'Files :' in line or 'Dirs  :' in line:
                # Extract count dari summary
                match = re.search(r':\s+(\d+)', line)
                if match:
                    count = int(match.group(1))
                    self.files_copied = count
                    
                    # Emit file count signal untuk UI update
                    if self.start_time:
                        self.file_count_signal.emit(self.files_copied, self.files_copied)
        except Exception as e:
            pass  # Silent fail untuk parsing

    def stop_process(self):
        """Stop robocopy process"""
        if self.process:
            try:
                # Kill process group untuk terminate semua child processes
                os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
                self.output_signal.emit(f"\n[{datetime.now().strftime('%H:%M:%S')}] Proses dihentikan oleh user.\n")
            except Exception as e:
                self.error_signal.emit(f"Error saat menghentikan proses: {str(e)}")


class RobocopyGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.robocopy_thread = None
        self.animation_thread = None
        self.config_file = Path("config.conf")
        self.init_ui()
        self.setWindowTitle("Robocopy UI - Advanced File Copy Tool")
        self.setGeometry(100, 100, 1200, 800)
        self.setup_window_icon()
        self.load_config()
        self.show()

    def closeEvent(self, event):
        """Handle window close event dengan confirmation dialog"""
        if self.robocopy_thread and self.robocopy_thread.isRunning():
            reply = QMessageBox.warning(
                self,
                "Proses Sedang Berjalan",
                "Proses copy robocopy masih sedang berjalan.\n\nYakin akan mengakhiri aplikasi?\nProses akan dihentikan.",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.robocopy_thread.stop_process()
                event.accept()
            else:
                event.ignore()
        else:
            reply = QMessageBox.question(
                self,
                "Konfirmasi Keluar",
                "Yakin akan mengakhiri aplikasi?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()

    def setup_window_icon(self):
        """Setup window icon from favicon.ico or logo.png"""
        icon_paths = ["favicon.ico", "logo.png", "icon.png"]
        for icon_path in icon_paths:
            if Path(icon_path).exists():
                self.setWindowIcon(QIcon(icon_path))
                break

    def init_ui(self):
        """Initialize semua UI elements"""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Title
        title_label = QLabel("Robocopy Advanced GUI")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)

        # Tab Widget
        tabs = QTabWidget()
        main_layout.addWidget(tabs)

        # Tab 1: Source & Destination
        tabs.addTab(self.create_source_dest_tab(), "Source & Destination")

        # Tab 2: Copy Options
        tabs.addTab(self.create_copy_options_tab(), "Copy Options")

        # Tab 3: File Selection
        tabs.addTab(self.create_file_selection_tab(), "File Selection")

        # Tab 4: Retry & Logging
        tabs.addTab(self.create_retry_logging_tab(), "Retry & Logging")

        # Tab 5: Junction & Symbolic Links
        tabs.addTab(self.create_junction_links_tab(), "Junction & Links")

        # Tab 6: About
        tabs.addTab(self.create_about_tab(), "About")

        # Output section
        output_group = QGroupBox("Output Log")
        output_layout = QVBoxLayout()
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet("background-color: #f0f0f0; font-family: Courier;")
        output_layout.addWidget(self.output_text)
        output_group.setLayout(output_layout)
        main_layout.addWidget(output_group, 1)

        # Control buttons
        button_layout = QHBoxLayout()
        
        self.run_button = QPushButton("▶ Run Robocopy")
        self.run_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        self.run_button.clicked.connect(self.run_robocopy)
        button_layout.addWidget(self.run_button)

        self.stop_button = QPushButton("⏹ Stop")
        self.stop_button.setStyleSheet("background-color: #f44336; color: white; font-weight: bold; padding: 10px;")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_robocopy)
        button_layout.addWidget(self.stop_button)

        self.clear_button = QPushButton("🗑 Clear Log")
        self.clear_button.clicked.connect(self.clear_log)
        button_layout.addWidget(self.clear_button)

        self.copy_button = QPushButton("📋 Copy Command")
        self.copy_button.clicked.connect(self.copy_command)
        button_layout.addWidget(self.copy_button)

        self.save_config_button = QPushButton("💾 Save Config")
        self.save_config_button.clicked.connect(self.save_config)
        button_layout.addWidget(self.save_config_button)

        main_layout.addLayout(button_layout)

    def create_source_dest_tab(self):
        """Tab untuk source dan destination folder dengan dual-pane explorer (Part 5)"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Title
        title = QLabel("Source & Destination File Explorer (Part 5)")
        title_font = QFont()
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Dual-pane layout
        panes_layout = QHBoxLayout()

        # Source pane
        source_group = QGroupBox("Source Folder")
        source_layout = QVBoxLayout()
        
        # Source path input
        source_input_layout = QHBoxLayout()
        self.source_input = QLineEdit()
        self.source_input.setPlaceholderText("Enter source folder path...")
        source_browse = QPushButton("Browse...")
        source_browse.clicked.connect(lambda: self.browse_folder(self.source_input))
        source_input_layout.addWidget(QLabel("Path:"))
        source_input_layout.addWidget(self.source_input, 1)
        source_input_layout.addWidget(source_browse)
        source_layout.addLayout(source_input_layout)
        
        # Source file explorer
        self.source_explorer = FileExplorerWidget()
        self.source_explorer.path_changed.connect(self.on_source_path_changed)
        self.source_input.textChanged.connect(self.on_source_input_changed)
        source_layout.addWidget(self.source_explorer)
        
        source_group.setLayout(source_layout)
        panes_layout.addWidget(source_group)

        # Destination pane
        dest_group = QGroupBox("Destination Folder")
        dest_layout = QVBoxLayout()
        
        # Destination path input
        dest_input_layout = QHBoxLayout()
        self.dest_input = QLineEdit()
        self.dest_input.setPlaceholderText("Enter destination folder path...")
        dest_browse = QPushButton("Browse...")
        dest_browse.clicked.connect(lambda: self.browse_folder(self.dest_input))
        dest_input_layout.addWidget(QLabel("Path:"))
        dest_input_layout.addWidget(self.dest_input, 1)
        dest_input_layout.addWidget(dest_browse)
        dest_layout.addLayout(dest_input_layout)
        
        # Destination file explorer
        self.dest_explorer = FileExplorerWidget()
        self.dest_explorer.path_changed.connect(self.on_dest_path_changed)
        self.dest_input.textChanged.connect(self.on_dest_input_changed)
        dest_layout.addWidget(self.dest_explorer)
        
        dest_group.setLayout(dest_layout)
        panes_layout.addWidget(dest_group)

        layout.addLayout(panes_layout, 1)

        widget.setLayout(layout)
        return widget
    
    def on_source_path_changed(self, path):
        """Update source input ketika user navigate di explorer"""
        self.source_input.blockSignals(True)
        self.source_input.setText(path)
        self.source_input.blockSignals(False)
    
    def on_source_input_changed(self, path):
        """Update source explorer ketika user input path"""
        if path and os.path.isdir(path):
            self.source_explorer.set_path(path)
    
    def on_dest_path_changed(self, path):
        """Update destination input ketika user navigate di explorer"""
        self.dest_input.blockSignals(True)
        self.dest_input.setText(path)
        self.dest_input.blockSignals(False)
    
    def on_dest_input_changed(self, path):
        """Update destination explorer ketika user input path"""
        if path and os.path.isdir(path):
            self.dest_explorer.set_path(path)

    def create_copy_options_tab(self):
        """Tab untuk copy options"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Copy flags group
        copy_group = QGroupBox("Copy Flags")
        copy_layout = QVBoxLayout()

        self.copy_subdirs = QCheckBox("/S - Copy Subdirectories (including empty)")
        self.copy_subdirs.setChecked(True)
        copy_layout.addWidget(self.copy_subdirs)

        self.copy_empty = QCheckBox("/E - Copy Subdirectories (including empty)")
        copy_layout.addWidget(self.copy_empty)

        self.copy_attributes = QCheckBox("/COPY:DAT - Copy Data, Attributes, Timestamps")
        self.copy_attributes.setChecked(True)
        copy_layout.addWidget(self.copy_attributes)

        self.copy_security = QCheckBox("/SEC - Copy files with security info")
        copy_layout.addWidget(self.copy_security)

        self.copy_all_info = QCheckBox("/COPYALL - Copy All info (D, A, T, S, O, U, X)")
        copy_layout.addWidget(self.copy_all_info)

        copy_group.setLayout(copy_layout)
        layout.addWidget(copy_group)

        # File attributes group
        attr_group = QGroupBox("File Attributes & Options")
        attr_layout = QVBoxLayout()

        self.recurse = QCheckBox("/R - Recurse to subdirectories")
        attr_layout.addWidget(self.recurse)

        self.multi_thread = QCheckBox("/MT[:N] - Multi-threaded copies")
        multi_layout = QHBoxLayout()
        self.multi_thread_num = QSpinBox()
        self.multi_thread_num.setRange(1, 128)
        self.multi_thread_num.setValue(8)
        self.multi_thread_num.setEnabled(False)
        self.multi_thread.toggled.connect(self.multi_thread_num.setEnabled)
        multi_layout.addWidget(self.multi_thread)
        multi_layout.addWidget(QLabel("Threads:"))
        multi_layout.addWidget(self.multi_thread_num)
        multi_layout.addStretch()
        attr_layout.addLayout(multi_layout)

        self.move_files = QCheckBox("/MOVE - Move files (delete after copy)")
        attr_layout.addWidget(self.move_files)

        self.purge = QCheckBox("/PURGE - Delete destination files/dirs not in source")
        attr_layout.addWidget(self.purge)

        self.mirror = QCheckBox("/MIR - Mirror (equivalent /S /E /PURGE)")
        attr_layout.addWidget(self.mirror)

        attr_group.setLayout(attr_layout)
        layout.addWidget(attr_group)

        # Animation group (Part 4)
        anim_group = QGroupBox("Animation & Effects (Part 4)")
        anim_layout = QVBoxLayout()

        self.enable_animation = QCheckBox("🎨 Enable Animated Gradient Background During Copy")
        self.enable_animation.setChecked(False)
        anim_layout.addWidget(self.enable_animation)

        anim_layout.addWidget(QLabel("Saat copy berlangsung, background form akan menampilkan animasi\ngradient dengan perubahan warna untuk visualisasi proses copy."))
        
        anim_group.setLayout(anim_layout)
        layout.addWidget(anim_group)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def create_file_selection_tab(self):
        """Tab untuk file selection"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Include files
        include_group = QGroupBox("Include Files (File Patterns)")
        include_layout = QVBoxLayout()
        include_layout.addWidget(QLabel("Masukkan file patterns, pisahkan dengan semicolon (;)"))
        include_layout.addWidget(QLabel("Contoh: *.txt;*.docx;*.pdf"))
        self.include_files = QLineEdit()
        self.include_files.setPlaceholderText("*.* (semua file)")
        include_layout.addWidget(self.include_files)
        include_group.setLayout(include_layout)
        layout.addWidget(include_group)

        # Exclude files
        exclude_group = QGroupBox("Exclude Files (File Patterns)")
        exclude_layout = QVBoxLayout()
        exclude_layout.addWidget(QLabel("File patterns untuk exclude"))
        exclude_layout.addWidget(QLabel("Contoh: *.tmp;Thumbs.db;.git"))
        self.exclude_files = QLineEdit()
        self.exclude_files.setPlaceholderText("Optional - kosongkan jika tidak ada")
        exclude_layout.addWidget(self.exclude_files)
        exclude_group.setLayout(exclude_layout)
        layout.addWidget(exclude_group)

        # Exclude directories
        exclude_dir_group = QGroupBox("Exclude Directories")
        exclude_dir_layout = QVBoxLayout()
        exclude_dir_layout.addWidget(QLabel("Directory names untuk exclude"))
        exclude_dir_layout.addWidget(QLabel("Contoh: .git;node_modules;__pycache__"))
        self.exclude_dirs = QLineEdit()
        self.exclude_dirs.setPlaceholderText("Optional - kosongkan jika tidak ada")
        exclude_dir_layout.addWidget(self.exclude_dirs)
        exclude_dir_group.setLayout(exclude_dir_layout)
        layout.addWidget(exclude_dir_group)

        # Max file age
        age_group = QGroupBox("File Age Filter (Optional)")
        age_layout = QHBoxLayout()
        self.max_age_check = QCheckBox("Exclude files older than (days)")
        self.max_age_spin = QSpinBox()
        self.max_age_spin.setRange(0, 9999)
        self.max_age_spin.setValue(30)
        self.max_age_spin.setEnabled(False)
        self.max_age_check.toggled.connect(self.max_age_spin.setEnabled)
        age_layout.addWidget(self.max_age_check)
        age_layout.addWidget(self.max_age_spin)
        age_layout.addStretch()
        age_group.setLayout(age_layout)
        layout.addWidget(age_group)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def create_retry_logging_tab(self):
        """Tab untuk retry dan logging options"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Retry options
        retry_group = QGroupBox("Retry Options")
        retry_layout = QVBoxLayout()

        retry_layout.addWidget(QLabel("Retry Configuration:"))
        
        retry_inner = QHBoxLayout()
        retry_inner.addWidget(QLabel("Max Retries:"))
        self.retry_count = QSpinBox()
        self.retry_count.setRange(0, 32767)
        self.retry_count.setValue(1)
        self.retry_count.setMaximumWidth(100)
        retry_inner.addWidget(self.retry_count)

        retry_inner.addWidget(QLabel("Wait time (seconds):"))
        self.retry_wait = QSpinBox()
        self.retry_wait.setRange(0, 300)
        self.retry_wait.setValue(30)
        self.retry_wait.setMaximumWidth(100)
        retry_inner.addWidget(self.retry_wait)
        retry_inner.addStretch()
        retry_layout.addLayout(retry_inner)

        retry_group.setLayout(retry_layout)
        layout.addWidget(retry_group)

        # Logging options
        log_group = QGroupBox("Logging Options")
        log_layout = QVBoxLayout()

        self.verbose = QCheckBox("/V - Verbose (show all skipped files)")
        log_layout.addWidget(self.verbose)

        self.log_only = QCheckBox("/L - List only (don't copy, delete or timestamp)")
        log_layout.addWidget(self.log_only)

        self.log_file_check = QCheckBox("Save log to file")
        self.log_file_input = QLineEdit()
        self.log_file_input.setPlaceholderText("robocopy_log.txt")
        self.log_file_input.setText("robocopy_log.txt")
        self.log_file_input.setEnabled(False)
        self.log_file_check.toggled.connect(self.log_file_input.setEnabled)
        
        log_file_layout = QHBoxLayout()
        log_file_layout.addWidget(self.log_file_check)
        log_file_layout.addWidget(self.log_file_input)
        log_layout.addLayout(log_file_layout)

        # Progress monitoring option (Part 3)
        self.enable_progress = QCheckBox("Enable Progress Monitoring (show real-time progress & time estimation)")
        self.enable_progress.setChecked(True)
        log_layout.addWidget(self.enable_progress)

        log_group.setLayout(log_layout)
        layout.addWidget(log_group)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def create_junction_links_tab(self):
        """Tab untuk Junction dan Symbolic Link options"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Information group
        info_group = QGroupBox("Informasi")
        info_layout = QVBoxLayout()
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setText("""
        <b>Junction dan Symbolic Link Options</b><br><br>
        <b>/SJ (Salin Junction):</b><br>
        Menyalin Junction/Symbolic Link itu sendiri ke tujuan, bukan menyalin file di dalam direktori target.<br><br>
        
        <b>/SL (Salin Symbolic Link):</b><br>
        Menyalin tautan simbolik sebagai tautan, bukan menyalin file target.<br><br>
        
        <b>/XJ (Kecualikan Persimpangan):</b><br>
        Mengecualikan semua titik persimpangan (biasanya disertakan secara default), mencegah potensi perulangan tak terbatas.<br><br>
        
        <b>/XJD (Kecualikan Direktori Junction):</b><br>
        Secara khusus mengecualikan titik junction untuk direktori.<br><br>
        
        <b>/XJF (Kecualikan File Junction):</b><br>
        Secara khusus mengecualikan titik junction untuk file.
        """)
        info_layout.addWidget(info_text)
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)

        # Copy options group
        copy_group = QGroupBox("Copy Options")
        copy_layout = QVBoxLayout()

        self.copy_junction = QCheckBox("/SJ - Salin Junction/Symbolic Link itu sendiri")
        copy_layout.addWidget(self.copy_junction)

        self.copy_symlink = QCheckBox("/SL - Salin Symbolic Link sebagai tautan")
        copy_layout.addWidget(self.copy_symlink)

        copy_group.setLayout(copy_layout)
        layout.addWidget(copy_group)

        # Exclude options group
        exclude_group = QGroupBox("Exclude Options")
        exclude_layout = QVBoxLayout()

        self.exclude_junction = QCheckBox("/XJ - Kecualikan semua Junction points")
        exclude_layout.addWidget(self.exclude_junction)

        self.exclude_junction_dir = QCheckBox("/XJD - Kecualikan Junction untuk Direktori")
        exclude_layout.addWidget(self.exclude_junction_dir)

        self.exclude_junction_file = QCheckBox("/XJF - Kecualikan Junction untuk File")
        exclude_layout.addWidget(self.exclude_junction_file)

        exclude_group.setLayout(exclude_layout)
        layout.addWidget(exclude_group)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def create_about_tab(self):
        """Tab untuk informasi aplikasi dan developer"""
        widget = QWidget()
        layout = QVBoxLayout()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        # Logo section
        logo_group = QGroupBox("Application Logo")
        logo_layout = QVBoxLayout()
        logo_label = QLabel()
        
        logo_paths = [ "icon.png","favicon.ico", "logo.png"]
        for logo_path in logo_paths:
            if Path(logo_path).exists():
                pixmap = QPixmap(logo_path)
                if not pixmap.isNull():
                    scaled_pixmap = pixmap.scaledToWidth(200, Qt.SmoothTransformation)
                    logo_label.setPixmap(scaled_pixmap)
                    logo_label.setAlignment(Qt.AlignCenter)
                    break
        
        logo_layout.addWidget(logo_label)
        logo_group.setLayout(logo_layout)
        scroll_layout.addWidget(logo_group)

        # Application info
        app_info_group = QGroupBox("Application Information")
        app_info_layout = QVBoxLayout()
        
        app_info_text = QTextEdit()
        app_info_text.setReadOnly(True)
        app_info_text.setText("""
        <b>Robocopy Advanced GUI</b><br><br>
        <b>Version:</b> 1.0.0<br>
        <b>Release Date:</b> February 2026<br><br>
        
        <b>Description:</b><br>
        Robocopy Advanced GUI adalah aplikasi antarmuka grafis yang dirancang untuk 
        memudahkan pengguna Windows dalam menjalankan perintah Robocopy (Robust File Copy) 
        dengan parameter yang dapat dikonfigurasi melalui GUI yang user-friendly.<br><br>
        
        <b>Features:</b><br>
        • Browse folder source dan destination<br>
        • Konfigurasi copy options (mirror, move, purge, dll)<br>
        • File selection dengan include/exclude patterns<br>
        • Retry dan logging configuration<br>
        • Multi-threaded copy support<br>
        • Junction dan Symbolic Link management<br>
        • Real-time output logging<br>
        • Configuration save/load<br>
        • Copy command to clipboard<br><br>
        
        <b>System Requirements:</b><br>
        • Windows 7 atau lebih baru<br>
        • Python 3.7+<br>
        • PyQt5<br>

        """)
        app_info_layout.addWidget(app_info_text)
        app_info_group.setLayout(app_info_layout)
        scroll_layout.addWidget(app_info_group)

        # Developer info
        dev_info_group = QGroupBox("Developer Information")
        dev_info_layout = QVBoxLayout()
        
        dev_info_text = QTextEdit()
        dev_info_text.setReadOnly(True)
        dev_info_text.setText("""
        <b>Development Team</b><br><br><br>
        <b>Personal:</b><br>
        • github.com/wspras-dev<br>
        • Widayat S Prasetiyo<br>
        • wspras@yahoo.com<br><br>

        <b>Project:</b> Robocopy Advanced GUI<br><br>
        <b>Repository:</b>  github.com/wspras-dev/robocopy-ui<br><br>
        
        <b>Technologies Used:</b><br>
        • Python 3<br>
        • PyQt5 (GUI Framework)<br>
        • Windows Robocopy.exe<br><br>
        
        <b>Key Features Implementation:</b><br>
        • Multi-threaded subprocess management<br>
        • Configuration persistence (JSON)<br>
        • Icon support (favicon.ico, logo.png)<br>
        • Process control (stop/pause)<br>
        • Real-time output streaming<br><br>
        
        <b>Support & Documentation:</b><br>
        Untuk informasi lebih lanjut, lihat file README.md yang tersedia dalam project.<br><br>
        
        <b>License:</b> Internal Use<br>
        <b>Last Updated:</b> February 2026<br>
        """)
        dev_info_layout.addWidget(dev_info_text)
        dev_info_group.setLayout(dev_info_layout)
        scroll_layout.addWidget(dev_info_group)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        widget.setLayout(layout)
        return widget

    def browse_folder(self, input_widget):
        """Browse folder dialog - opens at last used folder from input_widget"""
        # Get current path from input widget
        current_path = input_widget.text().strip()
        
        # If path exists and is a directory, use it as starting point
        start_dir = current_path if current_path and os.path.isdir(current_path) else ""
        
        folder = QFileDialog.getExistingDirectory(self, "Select Folder", start_dir)
        if folder:
            input_widget.setText(folder)

    def build_robocopy_command(self):
        """Build robocopy command dari UI inputs"""
        source = self.source_input.text().strip()
        dest = self.dest_input.text().strip()

        if not source or not dest:
            QMessageBox.warning(self, "Error", "Source dan Destination folder harus diisi!")
            return None

        # Basic command
        cmd = f'robocopy "{source}" "{dest}"'

        # File patterns
        include = self.include_files.text().strip()
        if include and include != "*.*":
            files = " ".join([f'"{f.strip()}"' for f in include.split(";")])
            cmd += f" {files}"
        else:
            cmd += " *.*"

        # Copy options
        if self.copy_subdirs.isChecked():
            cmd += " /S"
        if self.copy_empty.isChecked():
            cmd += " /E"
        if self.mirror.isChecked():
            cmd += " /MIR"
        if self.move_files.isChecked():
            cmd += " /MOVE"
        if self.purge.isChecked():
            cmd += " /PURGE"

        # Copy attributes
        if self.copy_attributes.isChecked():
            cmd += " /COPY:DAT"
        if self.copy_security.isChecked():
            cmd += " /SEC"
        if self.copy_all_info.isChecked():
            cmd += " /COPYALL"

        # Multi-thread
        if self.multi_thread.isChecked():
            threads = self.multi_thread_num.value()
            cmd += f" /MT:{threads}"

        # Retry options
        retry = self.retry_count.value()
        wait = self.retry_wait.value()
        cmd += f" /R:{retry} /W:{wait}"

        # Exclude patterns
        if self.exclude_files.text().strip():
            exclude_files = self.exclude_files.text().strip().split(";")
            for f in exclude_files:
                cmd += f' /XF "{f.strip()}"'

        if self.exclude_dirs.text().strip():
            exclude_dirs = self.exclude_dirs.text().strip().split(";")
            for d in exclude_dirs:
                cmd += f' /XD "{d.strip()}"'

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

        # File age filter
        if self.max_age_check.isChecked():
            days = self.max_age_spin.value()
            cmd += f" /MAXAGE:{days}"

        # Logging
        if self.verbose.isChecked():
            cmd += " /V"
        if self.log_only.isChecked():
            cmd += " /L"

        # Log file
        if self.log_file_check.isChecked():
            log_file = self.log_file_input.text().strip()
            if log_file:
                cmd += f' /LOG:"{log_file}"'

        return cmd

    def run_robocopy(self):
        """Run robocopy command dengan confirmation dialog"""
        command = self.build_robocopy_command()
        if not command:
            return

        # Show confirmation dialog (Fitur Part 3)
        source = self.source_input.text().strip()
        dest = self.dest_input.text().strip()
        reply = QMessageBox.question(
            self,
            "Konfirmasi Robocopy",
            f"Yakin akan memproses robocopy?\n\n"
            f"Source: {source}\n"
            f"Destination: {dest}\n\n"
            f"Proses ini akan berjalan di background.\n"
            f"Anda dapat memberhentikan dengan tombol 'STOP'.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            return

        # Disable all buttons except STOP (Fitur Part 3)
        self._disable_all_buttons_except_stop()
        
        self.output_text.append(f"\n{'='*80}")
        
        # Start animation if enabled (Part 4)
        if self.enable_animation.isChecked():
            self.animation_thread = AnimationThread()
            self.animation_thread.color_change_signal.connect(self.apply_animated_gradient)
            self.animation_thread.start()
        
        # Create thread dengan enable_progress option (Fitur Part 3)
        enable_progress = self.enable_progress.isChecked()
        self.robocopy_thread = RobocopyThread(command, enable_progress=enable_progress)
        self.robocopy_thread.output_signal.connect(self.append_output)
        self.robocopy_thread.finished_signal.connect(self.on_robocopy_finished)
        self.robocopy_thread.error_signal.connect(self.on_robocopy_error)
        self.robocopy_thread.file_count_signal.connect(self.on_file_count_update)
        self.robocopy_thread.start()

    def _disable_all_buttons_except_stop(self):
        """Disable semua tombol kecuali STOP saat proses berjalan (Fitur Part 3)"""
        self.run_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.clear_button.setEnabled(False)
        self.copy_button.setEnabled(False)
        self.save_config_button.setEnabled(False)

    def _enable_all_buttons(self):
        """Re-enable semua tombol setelah proses selesai (Fitur Part 3)"""
        self.run_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.clear_button.setEnabled(True)
        self.copy_button.setEnabled(True)
        self.save_config_button.setEnabled(True)

    def on_file_count_update(self, current, total):
        """Handle file count update dari thread (Fitur Part 3)"""
        # Ini bisa di-enhance untuk show progress bar atau file counter
        pass

    def apply_animated_gradient(self, gradient):
        """Apply animated gradient to main widget (Part 4)"""
        main_widget = self.centralWidget()
        if main_widget:
            palette = main_widget.palette()
            # Set background gradient
            palette.setBrush(main_widget.backgroundRole(), QBrush(gradient))
            main_widget.setPalette(palette)
            main_widget.setAutoFillBackground(True)

    def stop_animation(self):
        """Stop animation thread (Part 4)"""
        if self.animation_thread and self.animation_thread.isRunning():
            self.animation_thread.stop()
            self.animation_thread.wait()
            
            # Reset background to default
            main_widget = self.centralWidget()
            if main_widget:
                palette = main_widget.palette()
                palette.setBrush(main_widget.backgroundRole(), QBrush())
                main_widget.setPalette(palette)
                main_widget.setAutoFillBackground(False)

    def stop_robocopy(self):
        """Stop robocopy process"""
        if self.robocopy_thread and self.robocopy_thread.isRunning():
            self.robocopy_thread.stop_process()
            # Stop animation (Part 4)
            self.stop_animation()
            # Re-enable buttons (Fitur Part 3)
            self._enable_all_buttons()

    def on_robocopy_finished(self, returncode):
        """Called when robocopy thread finishes dengan completion notification (Fitur Part 3)"""
        # Stop animation (Part 4)
        self.stop_animation()
        
        # Re-enable all buttons (Fitur Part 3)
        self._enable_all_buttons()
        
        if returncode == 0:
            status_msg = "✓ Robocopy berhasil dijalankan!"
            self.output_text.append(f"\n{status_msg}")
            # Show completion notification (Fitur Part 3)
            QMessageBox.information(
                self,
                "Proses Selesai",
                f"{status_msg}\n\n"
                f"Waktu saat ini: {datetime.now().strftime('%H:%M:%S')}\n\n"
                f"Cek output log di atas untuk detail proses.",
                QMessageBox.Ok
            )
        else:
            status_msg = f"✗ Robocopy selesai dengan exit code: {returncode}"
            self.output_text.append(f"\n{status_msg}")
            # Show completion notification dengan warning (Fitur Part 3)
            QMessageBox.warning(
                self,
                "Proses Selesai dengan Error",
                f"{status_msg}\n\n"
                f"Waktu saat ini: {datetime.now().strftime('%H:%M:%S')}\n\n"
                f"Cek output log di atas untuk detail error.",
                QMessageBox.Ok
            )
        
        # Auto-save config
        self.save_config()

    def on_robocopy_error(self, error):
        """Called when robocopy error occurs"""
        # Stop animation (Part 4)
        self.stop_animation()
        
        # Re-enable all buttons (Fitur Part 3)
        self._enable_all_buttons()
        self.output_text.append(f"\n✗ Error: {error}")
        QMessageBox.critical(self, "Error", f"Terjadi error:\n{error}")

    def append_output(self, text):
        """Append text to output log"""
        self.output_text.insertPlainText(text)
        self.output_text.moveCursor(QTextCursor.End)

    def clear_log(self):
        """Clear output log"""
        self.output_text.clear()

    def copy_command(self):
        """Copy command to clipboard"""
        command = self.build_robocopy_command()
        if command:
            from PyQt5.QtWidgets import QApplication
            QApplication.clipboard().setText(command)
            QMessageBox.information(self, "Success", "Command copied to clipboard!")

    def save_config(self):
        """Save configuration to config.conf"""
        try:
            config_data = {
                "source": self.source_input.text(),
                "destination": self.dest_input.text(),
                "copy_subdirs": self.copy_subdirs.isChecked(),
                "copy_empty": self.copy_empty.isChecked(),
                "copy_attributes": self.copy_attributes.isChecked(),
                "copy_security": self.copy_security.isChecked(),
                "copy_all_info": self.copy_all_info.isChecked(),
                "recurse": self.recurse.isChecked(),
                "multi_thread": self.multi_thread.isChecked(),
                "multi_thread_num": self.multi_thread_num.value(),
                "move_files": self.move_files.isChecked(),
                "purge": self.purge.isChecked(),
                "mirror": self.mirror.isChecked(),
                "include_files": self.include_files.text(),
                "exclude_files": self.exclude_files.text(),
                "exclude_dirs": self.exclude_dirs.text(),
                "max_age_check": self.max_age_check.isChecked(),
                "max_age_spin": self.max_age_spin.value(),
                "retry_count": self.retry_count.value(),
                "retry_wait": self.retry_wait.value(),
                "verbose": self.verbose.isChecked(),
                "log_only": self.log_only.isChecked(),
                "log_file_check": self.log_file_check.isChecked(),
                "log_file_input": self.log_file_input.text(),
                "copy_junction": self.copy_junction.isChecked(),
                "copy_symlink": self.copy_symlink.isChecked(),
                "exclude_junction": self.exclude_junction.isChecked(),
                "exclude_junction_dir": self.exclude_junction_dir.isChecked(),
                "exclude_junction_file": self.exclude_junction_file.isChecked(),
                "enable_progress": self.enable_progress.isChecked(),
                "enable_animation": self.enable_animation.isChecked(),
            }
            
            with open(self.config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
            
            QMessageBox.information(self, "Success", "Konfigurasi berhasil disimpan ke config.conf")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error menyimpan konfigurasi:\n{str(e)}")

    def load_config(self):
        """Load configuration from config.conf"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config_data = json.load(f)
                
                # Load all settings
                self.source_input.setText(config_data.get("source", ""))
                self.dest_input.setText(config_data.get("destination", ""))
                self.copy_subdirs.setChecked(config_data.get("copy_subdirs", True))
                self.copy_empty.setChecked(config_data.get("copy_empty", False))
                self.copy_attributes.setChecked(config_data.get("copy_attributes", True))
                self.copy_security.setChecked(config_data.get("copy_security", False))
                self.copy_all_info.setChecked(config_data.get("copy_all_info", False))
                self.recurse.setChecked(config_data.get("recurse", False))
                self.multi_thread.setChecked(config_data.get("multi_thread", False))
                self.multi_thread_num.setValue(config_data.get("multi_thread_num", 8))
                self.move_files.setChecked(config_data.get("move_files", False))
                self.purge.setChecked(config_data.get("purge", False))
                self.mirror.setChecked(config_data.get("mirror", False))
                self.include_files.setText(config_data.get("include_files", ""))
                self.exclude_files.setText(config_data.get("exclude_files", ""))
                self.exclude_dirs.setText(config_data.get("exclude_dirs", ""))
                self.max_age_check.setChecked(config_data.get("max_age_check", False))
                self.max_age_spin.setValue(config_data.get("max_age_spin", 30))
                self.retry_count.setValue(config_data.get("retry_count", 1))
                self.retry_wait.setValue(config_data.get("retry_wait", 30))
                self.verbose.setChecked(config_data.get("verbose", False))
                self.log_only.setChecked(config_data.get("log_only", False))
                self.log_file_check.setChecked(config_data.get("log_file_check", False))
                self.log_file_input.setText(config_data.get("log_file_input", "robocopy_log.txt"))
                self.copy_junction.setChecked(config_data.get("copy_junction", False))
                self.copy_symlink.setChecked(config_data.get("copy_symlink", False))
                self.exclude_junction.setChecked(config_data.get("exclude_junction", False))
                self.exclude_junction_dir.setChecked(config_data.get("exclude_junction_dir", False))
                self.exclude_junction_file.setChecked(config_data.get("exclude_junction_file", False))
                self.enable_progress.setChecked(config_data.get("enable_progress", True))
                self.enable_animation.setChecked(config_data.get("enable_animation", False))
        except Exception as e:
            print(f"Error loading config: {str(e)}")


def main():
    app = QApplication(sys.argv)
    gui = RobocopyGUI()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
