import sys
import ctypes
import os
import win32api
import win32con
from ctypes import wintypes
from PyQt5 import QtWidgets, QtGui
import pymem
import psutil

class MEMORY_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("BaseAddress", ctypes.c_void_p),
        ("AllocationBase", ctypes.c_void_p),
        ("AllocationProtect", wintypes.DWORD),
        ("RegionSize", ctypes.c_size_t),
        ("State", wintypes.DWORD),
        ("Protect", wintypes.DWORD),
        ("Type", wintypes.DWORD),
    ]

PAGE_READABLE = [0x02, 0x04, 0x20, 0x40]  # PAGE_READONLY, PAGE_READWRITE, PAGE_EXECUTE_READ, PAGE_EXECUTE_READWRITE

class SoulSeekr(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.previous_scan_results = []
        self.last_scan_type = ""
        self.initUI()

    def initUI(self):
        self.setWindowTitle("SoulSeekr - Memory Scanner")
        self.setGeometry(100, 100, 700, 500)

        layout = QtWidgets.QVBoxLayout()

        self.processComboBox = QtWidgets.QComboBox()
        self.refreshProcessList()
        layout.addWidget(self.processComboBox)

        self.refreshButton = QtWidgets.QPushButton("🔄 Refresh Process List")
        self.refreshButton.clicked.connect(self.refreshProcessList)
        layout.addWidget(self.refreshButton)

        self.pidInput = QtWidgets.QLineEdit()
        self.pidInput.setPlaceholderText("Or enter PID directly")
        layout.addWidget(self.pidInput)

        self.attachButton = QtWidgets.QPushButton("🔗 Attach to Process")
        self.attachButton.clicked.connect(self.attachToProcess)
        layout.addWidget(self.attachButton)

        self.inputField = QtWidgets.QLineEdit()
        self.inputField.setPlaceholderText("Enter value to scan")
        layout.addWidget(self.inputField)

        self.scanTypeComboBox = QtWidgets.QComboBox()
        self.scanTypeComboBox.addItems(["Exact", "Bigger", "Smaller"])
        layout.addWidget(self.scanTypeComboBox)

        self.firstScanButton = QtWidgets.QPushButton("🔍 First Scan")
        self.firstScanButton.clicked.connect(self.performScan)
        layout.addWidget(self.firstScanButton)

        self.nextScanButton = QtWidgets.QPushButton("🔄 Next Scan")
        self.nextScanButton.clicked.connect(self.nextScan)
        layout.addWidget(self.nextScanButton)

        self.output = QtWidgets.QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.setLayout(layout)

    def isSystemProcess(self, exe):
        system_dirs = [
            os.environ.get("SystemRoot", r"C:\\Windows"),
            os.path.join(os.environ.get("SystemRoot", r"C:\\Windows"), "System32"),
        ]
        return any(exe.lower().startswith(sd.lower()) for sd in system_dirs)

    def refreshProcessList(self):
        self.processComboBox.clear()
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                pid = proc.info['pid']
                name = proc.info['name']
                exe = proc.exe() if hasattr(proc, 'exe') else ""
                if not exe or self.isSystemProcess(exe):
                    continue
                icon = QtGui.QIcon(exe) if os.path.exists(exe) else QtGui.QIcon()
                self.processComboBox.addItem(icon, f"{name} ({pid})", pid)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

    def attachToProcess(self):
        pid_text = self.pidInput.text()
        pid = int(pid_text) if pid_text.isdigit() else self.processComboBox.currentData()
        try:
            self.pm = pymem.Pymem()
            self.pm.open_process_from_id(pid)
            self.output.append(f"✅ Attached to PID: {pid}")
        except Exception as e:
            self.output.append(f"❌ Failed to attach: {str(e)}")

    def performScan(self):
        if not hasattr(self, 'pm'):
            self.output.append("❌ Attach to a process first.")
            return

        value = self.inputField.text()
        scan_type = self.scanTypeComboBox.currentText()
        if not value:
            self.output.append("⚠️ Please enter a value to scan.")
            return

        found_addresses = []
        try:
            int_value = int(value)
            address = 0
            mbi = MEMORY_BASIC_INFORMATION()

            while ctypes.windll.kernel32.VirtualQueryEx(self.pm.process_handle, ctypes.c_void_p(address), ctypes.byref(mbi), ctypes.sizeof(mbi)):
                if mbi.State == 0x1000 and mbi.Protect in PAGE_READABLE:
                    try:
                        chunk = self.pm.read_bytes(mbi.BaseAddress, mbi.RegionSize)
                        for i in range(0, len(chunk) - 4):
                            val = int.from_bytes(chunk[i:i+4], 'little')
                            if (scan_type == "Exact" and val == int_value) or \
                               (scan_type == "Bigger" and val > int_value) or \
                               (scan_type == "Smaller" and val < int_value):
                                found_addresses.append(mbi.BaseAddress + i)
                    except:
                        pass
                address += mbi.RegionSize

            self.output.append(f"🔍 Found {len(found_addresses)} addresses.")
            self.previous_scan_results = found_addresses
            self.last_scan_type = scan_type
            self.displayResults(found_addresses)

        except Exception as e:
            self.output.append(f"❌ Scan failed: {str(e)}")

    def nextScan(self):
        if not self.previous_scan_results:
            self.output.append("❌ No previous scan found. Perform a First Scan first.")
            return

        search_value = self.inputField.text()
        if not search_value:
            self.output.append("⚠️ Please enter a value to filter by.")
            return

        scan_type = self.last_scan_type
        match_func = self.getComparisonFunction(scan_type, search_value)
        if match_func is None:
            self.output.append("⚠️ Invalid scan type or value.")
            return

        new_results = []
        for address in self.previous_scan_results:
            try:
                value = self.pm.read_int(address)
                if match_func(value):
                    new_results.append(address)
            except:
                continue

        self.output.append(f"🔄 Refined: {len(new_results)} addresses matched.")
        self.previous_scan_results = new_results
        self.displayResults(new_results)

    def getComparisonFunction(self, scan_type, target_value):
        try:
            val = int(target_value)
            if scan_type == "Exact":
                return lambda x: x == val
            elif scan_type == "Bigger":
                return lambda x: x > val
            elif scan_type == "Smaller":
                return lambda x: x < val
        except:
            return None

    def displayResults(self, addresses):
        self.output.append("\nAddresses:")
        for addr in addresses:
            self.output.append(hex(addr))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    seeker = SoulSeekr()
    seeker.show()
    sys.exit(app.exec_())
