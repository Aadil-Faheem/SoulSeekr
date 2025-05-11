
![Chic Website Homepage Fashion Collage Banner](https://github.com/user-attachments/assets/01db407e-58d0-4170-a945-cf8307ff237d)

<br>
<div align="center">

<h1><strong>☠️SoulSeekr - Memory Scanner & Editor (WIP)</strong></h1>

**SoulSeekr** is a lightweight, GUI-based memory manipulation script built with **Python + PyQt5** and powered by `pymem`.  
It allows you to attach to running processes, Search memory for values, Update them and Freeze them — similar to Cheat Engine.

</div>
<br>
<hr>

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

## 📷 Videos/ScreenShots

<div align="center">
  
[![Watch the demo](https://img.youtube.com/vi/_fO4bzilDqs/hqdefault.jpg)](https://youtu.be/_fO4bzilDqs)

<h1><strong>Watch The Demo!</strong></h1>

</div>

![3](https://github.com/user-attachments/assets/8090f376-c3cc-4609-840b-e3bc927a74ab)
![4](https://github.com/user-attachments/assets/c002affe-4adc-4664-a3cc-205b8287dc14)


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
