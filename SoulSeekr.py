import sys
import pymem
import pymem.process
import psutil
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QLabel, QComboBox, QLineEdit, QTextEdit, QHBoxLayout)

class CheatEngine(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SoulSeekr")
        self.pm = None
        self.process_name = None

        layout = QVBoxLayout()

        self.process_dropdown = QComboBox()
        self.refresh_process_list()
        layout.addWidget(QLabel("Select a Process:"))
        layout.addWidget(self.process_dropdown)

        search_layout = QHBoxLayout()
        self.pid_input = QLineEdit()
        self.pid_input.setPlaceholderText("Enter PID")
        self.search_btn = QPushButton("Search by PID")
        self.search_btn.clicked.connect(self.search_by_pid)
        search_layout.addWidget(self.pid_input)
        search_layout.addWidget(self.search_btn)
        layout.addLayout(search_layout)

        self.attach_btn = QPushButton("Attach")
        self.attach_btn.clicked.connect(self.attach_to_process)
        layout.addWidget(self.attach_btn)

        self.scan_input = QLineEdit()
        self.scan_input.setPlaceholderText("Enter value to scan")
        layout.addWidget(self.scan_input)

        self.scan_btn = QPushButton("First Scan")
        self.scan_btn.clicked.connect(self.first_scan)
        layout.addWidget(self.scan_btn)

        self.output = QTextEdit()
        layout.addWidget(self.output)

        self.setLayout(layout)

    def refresh_process_list(self):
        self.process_dropdown.clear()
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                self.process_dropdown.addItem(f"{proc.info['name']} ({proc.info['pid']})", proc.info['pid'])
            except:
                continue

    def search_by_pid(self):
        pid_text = self.pid_input.text()
        if pid_text.isdigit():
            pid = int(pid_text)
            try:
                name = psutil.Process(pid).name()
                self.process_dropdown.addItem(f"{name} ({pid})", pid)
                self.process_dropdown.setCurrentIndex(self.process_dropdown.count() - 1)
                self.output.append(f"Found process: {name} ({pid})")
            except psutil.NoSuchProcess:
                self.output.append("No process with that PID found.")
        else:
            self.output.append("Invalid PID.")

    def attach_to_process(self):
        pid = self.process_dropdown.currentData()
        try:
            self.pm = pymem.Pymem()
            self.pm.open_process(pid)
            self.process_name = psutil.Process(pid).name()
            self.output.append(f"Attached to {self.process_name} (PID: {pid})")
        except Exception as e:
            self.output.append(f"Failed to attach: {e}")

    def first_scan(self):
        if not self.pm:
            self.output.append("Attach to a process first.")
            return

        try:
            value_to_find = int(self.scan_input.text())
        except ValueError:
            self.output.append("Please enter a valid integer.")
            return

        try:
            module = pymem.process.module_from_name(self.pm.process_handle, self.process_name)
            start = module.lpBaseOfDll
            end = start + module.SizeOfImage
            found = []

            for address in range(start, end, 4):
                try:
                    if self.pm.read_int(address) == value_to_find:
                        found.append(address)
                except:
                    continue

            if found:
                self.output.append(f"Found {len(found)} result(s):")
                for addr in found:
                    self.output.append(hex(addr))
            else:
                self.output.append("No matching value found.")

        except Exception as e:
            self.output.append(f"Scan failed: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CheatEngine()
    window.show()
    sys.exit(app.exec_())
