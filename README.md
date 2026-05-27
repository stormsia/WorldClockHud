# WorldClockHud

A transparent, always-on-top world clock HUD for Windows.

![WorldClockHud](https://github.com/stormsia/WorldClockHud/raw/main/icon.ico)

## Features

- **Multiple Timezones** — Display clocks for any timezone in the world
- **Always on Top** — Stays visible above all windows (toggleable from system tray)
- **Desktop Mode** — Can also sit below all windows on your desktop
- **Draggable** — Click and drag to reposition anywhere on screen
- **System Tray** — Minimize to tray with quick-access controls
- **Auto Start** — Automatically launches on Windows startup (when installed via MSI)
- **Glassmorphism UI** — Semi-transparent dark glass aesthetic
- **Persistent Settings** — Your timezone selection and window position are saved

## Installation

### MSI Installer (Recommended)

Download the latest `.msi` from [Releases](https://github.com/stormsia/WorldClockHud/releases) and run it. The app will be installed and configured to start automatically on login.

### Portable

Download `WorldClockHud.exe` from [Releases](https://github.com/stormsia/WorldClockHud/releases) and run it directly. No installation required.

### From Source

```bash
git clone https://github.com/stormsia/WorldClockHud.git
cd WorldClockHud
pip install pyqt6 pytz psutil
python main.py
```

## Build

```bash
pip install pyinstaller pyqt6 pytz psutil
pyinstaller WorldClockHUD.spec
```

The executable will be created at `dist/WorldClockHud.exe`.

## Configuration

Settings are stored in `%APPDATA%\WorldClockHud\config.json`:

- **timezones** — List of timezone identifiers (e.g. `"UTC"`, `"America/New_York"`)
- **position** — `[x, y]` window position
- **always_on_top** — `true` / `false`

## Usage

- **Right-click** the HUD or tray icon for options
- **Left-click** tray icon to show/hide
- **Drag** the HUD to reposition
- **Settings** dialog to add/remove timezones

## License

MIT

## Author

[stormsia](https://github.com/stormsia)
