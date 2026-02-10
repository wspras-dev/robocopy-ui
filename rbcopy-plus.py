import sys
import subprocess
import threading
import os
from datetime import datetime
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QLabel, QLineEdit, QPushButton, QTextEdit, QCheckBox,
    QComboBox, QSpinBox, QFileDialog, QMessageBox, QTabWidget,
    QTableWidget, QTableWidgetItem, QSplitter, QProgressBar
)
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QSize
from PyQt5.QtGui import QIcon, QFont, QColor, QTextCursor


class RobocopyThread(QThread):
    """Thread untuk menjalankan robocopy.exe tanpa freeze GUI"""
    output_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(int)
    error_signal = pyqtSignal(str)

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        try:
            self.output_signal.emit(f"[{datetime.now().strftime('%H:%M:%S')}] Menjalankan command:\n{self.command}\n")
            self.output_signal.emit("=" * 80 + "\n")
            
            process = subprocess.Popen(
                self.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                shell=True
            )

            for line in process.stdout:
                self.output_signal.emit(line)

            returncode = process.wait()
            self.output_signal.emit("\n" + "=" * 80)
            self.output_signal.emit(f"[{datetime.now().strftime('%H:%M:%S')}] Proses selesai dengan exit code: {returncode}\n")
            self.finished_signal.emit(returncode)
        except Exception as e:
            self.error_signal.emit(f"Error: {str(e)}")
            self.finished_signal.emit(-1)


class RobocopyGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.robocopy_thread = None
        self.init_ui()
        self.setWindowTitle("Robocopy UI - Advanced File Copy Tool")
        self.setGeometry(100, 100, 1200, 800)
        self.show()

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

        clear_button = QPushButton("🗑 Clear Log")
        clear_button.clicked.connect(self.clear_log)
        button_layout.addWidget(clear_button)

        copy_button = QPushButton("📋 Copy Command")
        copy_button.clicked.connect(self.copy_command)
        button_layout.addWidget(copy_button)

        main_layout.addLayout(button_layout)

    def create_source_dest_tab(self):
        """Tab untuk source dan destination folder"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Source folder
        source_group = QGroupBox("Source Folder")
        source_layout = QHBoxLayout()
        self.source_input = QLineEdit()
        self.source_input.setPlaceholderText("Masukkan path folder source...")
        source_browse = QPushButton("Browse...")
        source_browse.clicked.connect(lambda: self.browse_folder(self.source_input))
        source_layout.addWidget(QLabel("Source:"))
        source_layout.addWidget(self.source_input, 1)
        source_layout.addWidget(source_browse)
        source_group.setLayout(source_layout)
        layout.addWidget(source_group)

        # Destination folder
        dest_group = QGroupBox("Destination Folder")
        dest_layout = QHBoxLayout()
        self.dest_input = QLineEdit()
        self.dest_input.setPlaceholderText("Masukkan path folder destination...")
        dest_browse = QPushButton("Browse...")
        dest_browse.clicked.connect(lambda: self.browse_folder(self.dest_input))
        dest_layout.addWidget(QLabel("Destination:"))
        dest_layout.addWidget(self.dest_input, 1)
        dest_layout.addWidget(dest_browse)
        dest_group.setLayout(dest_layout)
        layout.addWidget(dest_group)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

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

        log_group.setLayout(log_layout)
        layout.addWidget(log_group)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def browse_folder(self, input_widget):
        """Browse folder dialog"""
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
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
        """Run robocopy command"""
        command = self.build_robocopy_command()
        if not command:
            return

        self.run_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.output_text.append(f"\n{'='*80}")
        
        self.robocopy_thread = RobocopyThread(command)
        self.robocopy_thread.output_signal.connect(self.append_output)
        self.robocopy_thread.finished_signal.connect(self.on_robocopy_finished)
        self.robocopy_thread.error_signal.connect(self.on_robocopy_error)
        self.robocopy_thread.start()

    def stop_robocopy(self):
        """Stop robocopy process"""
        if self.robocopy_thread and self.robocopy_thread.isRunning():
            QMessageBox.information(self, "Info", "Untuk stop process, please close robocopy.exe dari Task Manager")

    def on_robocopy_finished(self, returncode):
        """Called when robocopy thread finishes"""
        self.run_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        
        if returncode == 0:
            self.output_text.append("\n✓ Robocopy berhasil dijalankan!")
        else:
            self.output_text.append(f"\n✗ Robocopy selesai dengan exit code: {returncode}")

    def on_robocopy_error(self, error):
        """Called when robocopy error occurs"""
        self.run_button.setEnabled(True)
        self.stop_button.setEnabled(False)
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


def main():
    app = QApplication(sys.argv)
    gui = RobocopyGUI()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
