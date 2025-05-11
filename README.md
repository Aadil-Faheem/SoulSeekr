# 🛠️ SoulSeekr - Memory Scanner & Editor (WIP)

**SoulSeekr** is a lightweight, GUI-based memory scanner built with **Python + PyQt5** and powered by `pymem`.  
It allows you to attach to running processes and search memory for values — similar to Cheat Engine.

<br>
<hr>
<br>

## 📷 Screenshots
<br>

![1](https://github.com/user-attachments/assets/3d1d990a-f53f-423c-a200-713785966360)

A. Basic Layout with Process Selection

<br><br>
![2](https://github.com/user-attachments/assets/daf4d3e9-9a5e-4780-9e16-c5840ac43b02)

B. Finding Value in Selected Process

<br>
<hr>
<br>

## ✅ Current Features

- 🎯 **Process Selector**
  - List and attach to running processes
  - Manual PID entry option

- 🔍 **Memory Scanner**
  - Search for specific integer values in a process's memory
  - Display all matching addresses

- 🔄 **Next Scan (Refine Results)**
  - Filter previous scan results after value changes
  - Allows more refined results

- 📝 **Manual Address Editor**
  - Write a custom value to a known address

- ❄️ **Freeze / Lock Value**
  - Constantly write a fixed value (e.g., Infinite health, Ammo etc)

<br>
<hr>
<br>

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/Aadil-Faheem/SoulSeekr.git
cd SoulSeekr
```

### 2. Install requirements
```bash
pip install -r requirements.txt
```

If you're missing PyQt5 or pymem, install them manually:
```bash
pip install PyQt5 pymem
```

### 3. Run the app
```bash
python SoulSeekr.py
```

<br>
<hr>
<br>

## 📦 Requirements

- Python 3.8+
- Windows OS (tested)
- `pymem` for process memory access
- `PyQt5` for GUI

<br>
<hr>
<br>

## 🧠 Roadmap / Upcoming Features

- 🧭 **Pointer Scanner**
  - Resolve dynamic addresses via pointer chain scanning

- 🧮 **Hex Viewer**
  - Display raw memory near selected address (hex + ASCII)

- 💾 **Save & Load Results**
  - Export found addresses and reload them later

- 🌙 **Dark Mode**
  - Toggle for UI appearance

- 👁️ **Live Value Monitor**
  - Show real-time updates at tracked addresses

- 🧬 **Data Type Selector**
  - Support scanning as int, float, double, byte, etc.

- 📊 **Process Memory Map**
  - View loaded modules, address ranges, base addresses

<br>
<hr>
<br>

## ⚠️ Disclaimer

> This tool is for **educational and testing purposes only**.  
> Do **not** use it on protected/online games or commercial software you don’t own.  
> Use responsibly.

<br>
<hr>
<br>

## 🧑‍💻 Author

**Aadil Faheem**  
GitHub: [@Aadil-Faheem](https://github.com/Aadil-Faheem)

<br>
<hr>
<br>

## 📜 License

MIT License – do what you want, just give credit.
