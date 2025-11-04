# Quick Start Guide - Spotify Hotkey App

## 🚀 Getting Started in 5 Minutes

### Step 1: Get Spotify API Credentials (2 minutes)

1. Go to https://developer.spotify.com/dashboard
2. Click **"Create an App"**
3. Fill in:
   - **App name**: "Spotify Hotkey" (or anything)
   - **App description**: "Personal hotkey controller"
4. Click **Create**
5. Click **"Edit Settings"**
6. Under **Redirect URIs**, add: `http://localhost:8888/callback`
7. Click **Save**
8. Go back and copy your **Client ID** and **Client Secret**

### Step 2: Configure the App (1 minute)

1. Run `SpotifyHotkey.exe`
2. Paste your **Client ID** into the first field
3. Paste your **Client Secret** into the second field
4. Click **"Connect to Spotify"**
5. A browser window will open - click **Agree** to authorize

### Step 3: (Optional) Set Target Playlist (1 minute)

If you want to use the "Add to Playlist" hotkey:

1. Open Spotify desktop or web
2. Go to your desired playlist
3. Click **"..."** → **Share** → **Copy Playlist Link**
4. Paste it into the **"Playlist ID or URI"** field in the app
5. Click **"Save Playlist"**

## 🎹 Using Hotkeys

Once connected, you can use these hotkeys from **anywhere** on your computer:

### Basic Playback
- **Ctrl+Alt+Space** - Play or pause
- **Ctrl+Alt+N** - Next track
- **Ctrl+Alt+B** - Previous track

### Quick Actions
- **Ctrl+Alt+L** - Like the current track
- **Ctrl+Alt+A** - Add current track to your saved playlist

### Volume Control
- **Ctrl+Alt+↑** - Increase volume by 10%
- **Ctrl+Alt+↓** - Decrease volume by 10%

### Playback Modes
- **Ctrl+Alt+S** - Toggle shuffle on/off
- **Ctrl+Alt+R** - Cycle repeat mode (Off → All → One → Off)

## 💡 Pro Tips

1. **Minimize to Tray**: Click the **X** button to hide the app to system tray. It keeps running and hotkeys still work!

2. **Right-click Tray Icon**:
   - Click "Show" to bring the window back
   - Click "Quit" to fully exit

3. **Notifications**: The app shows small notifications when you use hotkeys, so you know they're working

4. **Now Playing**: The app shows what's currently playing in real-time

5. **Run on Startup**: Add the .exe to your Windows startup folder to launch automatically
   - Press `Win+R`, type `shell:startup`, press Enter
   - Copy the SpotifyHotkey.exe shortcut there

## 🛠️ Troubleshooting

### Hotkeys Not Working?
- Run the app as **Administrator** (right-click → Run as administrator)
- Check if another app is using the same hotkey combination

### Can't Connect?
- Double-check your Client ID and Secret
- Make sure Redirect URI is exactly: `http://localhost:8888/callback`
- Try disconnecting and reconnecting

### "Add to Playlist" Not Working?
- Make sure you've set a target playlist
- Check that you have permission to edit the playlist
- Try using a different playlist

### Volume Control Not Working?
- Make sure Spotify is actively playing on a device
- Some devices don't support volume control via API

## 🎵 Enjoy!

You're all set! Your Spotify is now controllable from anywhere on your PC with simple hotkeys.

**Happy listening!** 🎶
