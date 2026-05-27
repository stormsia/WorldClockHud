<div align="center">

# 🕰️ WorldClockHUD

**A sleek, transparent, always-on-top world clock HUD for Windows.**

<img src="https://raw.githubusercontent.com/stormsia/WorldClockHud/main/icon.ico" alt="WorldClockHUD Icon" width="128" />

[![Latest Release](https://img.shields.io/github/v/release/stormsia/WorldClockHud?color=blue&style=for-the-badge)](https://github.com/stormsia/WorldClockHud/releases/latest)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows)](https://github.com/stormsia/WorldClockHud/releases/latest)
[![License](https://img.shields.io/github/license/stormsia/WorldClockHud?style=for-the-badge)](LICENSE)

</div>

---

## 📥 Download & Install

### 🌟 Recommended: MSI Installer
For the best experience, we highly recommend using the standard MSI installer. 

> [!IMPORTANT]
> **[⬇️ Download WorldClockHUD Installer (.msi)](https://github.com/stormsia/WorldClockHud/releases/latest/download/WorldClockHud.msi)**  
> *Or visit the [Latest Release page](https://github.com/stormsia/WorldClockHud/releases/latest) to see all downloads.*

**Benefits of the Installer:**
- 🚀 **Auto-Start**: Automatically launches when Windows starts (so your clocks are always there).
- 🪄 **Start Menu Integration**: Adds convenient shortcuts.
- ♻️ **Clean Management**: Easily update or uninstall through standard Windows settings.

### 📦 Portable Version
Don't want to install anything? You can just download the standalone executable:
- **[⬇️ Download Portable (.exe)](https://github.com/stormsia/WorldClockHud/releases/latest/download/WorldClockHud.exe)**

---

## ✨ Features

- 🌍 **Multiple Timezones** — Display clocks for any timezone in the world.
- 📌 **Always on Top** — Stays visible above all windows (can be toggled from the system tray).
- 🖥️ **Desktop Mode** — Option to sit below all windows, acting like a desktop widget.
- 🖐️ **Draggable** — Simply click and drag anywhere on your screen.
- ⚙️ **System Tray** — Unobtrusive, minimizes to tray with quick-access controls.
- 🎨 **Glassmorphism UI** — Beautiful, modern semi-transparent dark glass aesthetic.
- 💾 **Persistent Settings** — Remembers your timezones and exact window position.

---

## 🛠️ Usage

1. **Move the HUD**: Click anywhere on the HUD and drag it to your desired location.
2. **Settings Menu**: Right-click the HUD or the system tray icon to access settings and manage timezones.
3. **Toggle Visibility**: Left-click the system tray icon to quickly hide or show the HUD.

---

## ⚙️ Advanced

### Configuration

Settings are stored locally in `%APPDATA%\WorldClockHud\config.json`:
- `timezones`: List of timezone identifiers (e.g. `"UTC"`, `"America/New_York"`)
- `position`: Saved `[x, y]` window position on your monitor
- `always_on_top`: Boolean `true` or `false`

### Building From Source

```bash
# Clone the repository
git clone https://github.com/stormsia/WorldClockHud.git
cd WorldClockHud

# Install required dependencies
pip install uv
uv pip install -r requirements.txt --system

# Run directly
python main.py

# Or build the executable
pyinstaller WorldClockHUD.spec
```

---

## 📝 License & Author

- **Author**: [stormsia](https://github.com/stormsia)
- **License**: MIT
