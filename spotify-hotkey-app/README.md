# 🎵 Spotify Hotkey App

A lightweight Windows application for controlling Spotify with global hotkeys. Features a sleek black glass UI with Spotify green accents.

![Spotify Hotkey App](screenshot.png)

## ✨ Features

- **Global Hotkeys**: Control Spotify from anywhere
  - `Ctrl+Alt+N` - Next Track
  - `Ctrl+Alt+B` - Previous Track
  - `Ctrl+Alt+Space` - Play/Pause
  - `Ctrl+Alt+L` - Like Current Track
  - `Ctrl+Alt+A` - Add Current Track to Playlist
  - `Ctrl+Alt+↑` - Volume Up
  - `Ctrl+Alt+↓` - Volume Down
  - `Ctrl+Alt+S` - Toggle Shuffle
  - `Ctrl+Alt+R` - Cycle Repeat (Off → All → One)

- **Sleek UI**: Black glass design with Spotify green accents
- **System Tray**: Minimize to system tray, stays running in background
- **Real-time Display**: See what's currently playing
- **Volume Control**: Adjust Spotify volume with hotkeys
- **Playback Modes**: Quick shuffle and repeat toggle
- **Playlist Integration**: Quickly add tracks to your chosen playlist
- **Single Executable**: No installation required, just run the .exe

## 🚀 Quick Start

### Option 1: Download Pre-built Executable

1. Download `SpotifyHotkey.exe` from the releases
2. Run the executable
3. Follow the setup instructions below

### Option 2: Build from Source

#### Prerequisites

- Python 3.8 or higher
- Windows OS

#### Installation

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
python spotify_hotkey.py
```

#### Building Single Executable

To create a single .exe file:

```bash
pyinstaller build.spec
```

The executable will be in the `dist` folder.

## 🔧 Setup

### 1. Get Spotify API Credentials

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account
3. Click "Create an App"
4. Fill in the details:
   - **App Name**: Spotify Hotkey (or anything you want)
   - **App Description**: Personal hotkey controller
5. Click "Create"
6. Click "Edit Settings"
7. Add `http://localhost:8888/callback` to **Redirect URIs**
8. Click "Save"
9. Copy your **Client ID** and **Client Secret**

### 2. Configure the App

1. Launch SpotifyHotkey.exe
2. Paste your **Client ID** and **Client Secret**
3. Click "Connect to Spotify"
4. A browser window will open - log in and authorize the app
5. Return to the app - you should now see "Connected"

### 3. Set Target Playlist (Optional)

To use the "Add to Playlist" hotkey:

1. Open Spotify and navigate to your desired playlist
2. Click "..." → "Share" → "Copy Playlist Link"
3. Paste the link into the "Playlist ID or URI" field in the app
4. Click "Save Playlist"

You can also just paste the playlist ID (e.g., `37i9dQZF1DXcBWIGoYBM5M`)

## 🎹 Hotkeys

| Hotkey | Action |
|--------|--------|
| `Ctrl+Alt+N` | Next Track |
| `Ctrl+Alt+B` | Previous Track |
| `Ctrl+Alt+Space` | Play/Pause |
| `Ctrl+Alt+L` | Like Track ♥ |
| `Ctrl+Alt+A` | Add to Playlist |
| `Ctrl+Alt+↑` | Volume Up (+10%) |
| `Ctrl+Alt+↓` | Volume Down (-10%) |
| `Ctrl+Alt+S` | Toggle Shuffle |
| `Ctrl+Alt+R` | Cycle Repeat Mode |

> **Note**: Hotkeys work globally, even when the app is minimized or in system tray!

## 🎨 UI Preview

- **Black Glass Design**: Sleek, modern interface
- **Spotify Green Accents**: Authentic Spotify colors (#1DB954)
- **Real-time Updates**: Current track and artist display
- **Clean Layout**: All controls in one compact window
- **System Tray Integration**: Close to minimize to tray, hotkeys still work

## ⚙️ Requirements

- Windows 7 or higher
- Spotify installed and running
- Internet connection for Spotify API
- Administrator privileges (for global hotkeys)

## 🛠️ Troubleshooting

### Hotkeys Not Working
- Make sure you're running the app as Administrator
- Check if another app is using the same hotkey combinations

### Can't Connect to Spotify
- Verify your Client ID and Client Secret are correct
- Make sure the Redirect URI is set to `http://localhost:8888/callback`
- Check your internet connection

### "Add to Playlist" Not Working
- Make sure you've set a target playlist
- Verify the playlist ID is correct
- Check that you have permission to modify the playlist

## 📝 Configuration Files

The app stores configuration in your home directory:
- `~/.spotify_hotkey_config.json` - Your settings
- `~/.spotify_cache` - Spotify authentication token

## 🔒 Privacy

- Your credentials are stored locally only
- The app only accesses Spotify APIs you authorize
- No data is sent to external servers
- Source code is fully open for review

## 📦 Technical Details

- **Language**: Python 3.8+
- **GUI**: Tkinter
- **Spotify API**: spotipy
- **Hotkeys**: keyboard library
- **System Tray**: pystray + Pillow
- **Packaging**: PyInstaller (single file exe)

## 🤝 Contributing

Feel free to fork, modify, and submit pull requests!

## 📄 License

MIT License - feel free to use and modify

## ❤️ Made For

Music lovers who want quick Spotify control without leaving their workflow!

---

**Enjoy your music!** 🎶
