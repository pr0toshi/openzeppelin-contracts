import tkinter as tk
from tkinter import ttk, messagebox
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import keyboard
import threading
import json
import os
from pathlib import Path

# Spotify Colors
SPOTIFY_GREEN = "#1DB954"
SPOTIFY_BLACK = "#191414"
GLASS_BLACK = "#1a1a1a"
TEXT_WHITE = "#FFFFFF"

class SpotifyHotkeyApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Spotify Hotkey Controller")
        self.root.geometry("400x600")
        self.root.configure(bg=SPOTIFY_BLACK)
        self.root.resizable(False, False)

        # Config file path
        self.config_path = Path.home() / ".spotify_hotkey_config.json"
        self.config = self.load_config()

        # Spotify client
        self.sp = None
        self.current_track = None
        self.target_playlist_id = None

        # Build UI
        self.build_ui()

        # Setup hotkeys
        self.setup_hotkeys()

        # Try to authenticate
        if self.config.get('client_id') and self.config.get('client_secret'):
            self.authenticate()

    def load_config(self):
        """Load configuration from file"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return {}

    def save_config(self):
        """Save configuration to file"""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)

    def build_ui(self):
        """Build the glass-style UI"""
        # Header
        header_frame = tk.Frame(self.root, bg=SPOTIFY_BLACK)
        header_frame.pack(fill=tk.X, padx=10, pady=10)

        title_label = tk.Label(
            header_frame,
            text="🎵 Spotify Hotkey",
            font=("Segoe UI", 20, "bold"),
            bg=SPOTIFY_BLACK,
            fg=SPOTIFY_GREEN
        )
        title_label.pack()

        # Status indicator
        self.status_label = tk.Label(
            header_frame,
            text="● Disconnected",
            font=("Segoe UI", 9),
            bg=SPOTIFY_BLACK,
            fg="#ff4444"
        )
        self.status_label.pack()

        # Authentication Frame
        auth_frame = tk.Frame(self.root, bg=GLASS_BLACK, relief=tk.FLAT, bd=2)
        auth_frame.pack(fill=tk.X, padx=20, pady=10)

        auth_title = tk.Label(
            auth_frame,
            text="Spotify API Credentials",
            font=("Segoe UI", 11, "bold"),
            bg=GLASS_BLACK,
            fg=TEXT_WHITE
        )
        auth_title.pack(pady=5)

        # Client ID
        tk.Label(auth_frame, text="Client ID:", bg=GLASS_BLACK, fg=TEXT_WHITE, font=("Segoe UI", 9)).pack(anchor=tk.W, padx=10)
        self.client_id_entry = tk.Entry(auth_frame, bg="#2a2a2a", fg=TEXT_WHITE, insertbackground=TEXT_WHITE, relief=tk.FLAT, font=("Segoe UI", 9))
        self.client_id_entry.pack(fill=tk.X, padx=10, pady=2)
        if self.config.get('client_id'):
            self.client_id_entry.insert(0, self.config['client_id'])

        # Client Secret
        tk.Label(auth_frame, text="Client Secret:", bg=GLASS_BLACK, fg=TEXT_WHITE, font=("Segoe UI", 9)).pack(anchor=tk.W, padx=10, pady=(5,0))
        self.client_secret_entry = tk.Entry(auth_frame, bg="#2a2a2a", fg=TEXT_WHITE, insertbackground=TEXT_WHITE, relief=tk.FLAT, show="*", font=("Segoe UI", 9))
        self.client_secret_entry.pack(fill=tk.X, padx=10, pady=2)
        if self.config.get('client_secret'):
            self.client_secret_entry.insert(0, self.config['client_secret'])

        # Redirect URI (fixed)
        tk.Label(auth_frame, text="Redirect URI: http://localhost:8888/callback", bg=GLASS_BLACK, fg="#888888", font=("Segoe UI", 8)).pack(pady=2)

        # Connect button
        self.connect_btn = tk.Button(
            auth_frame,
            text="Connect to Spotify",
            command=self.authenticate,
            bg=SPOTIFY_GREEN,
            fg=SPOTIFY_BLACK,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            activebackground="#1ed760",
            activeforeground=SPOTIFY_BLACK
        )
        self.connect_btn.pack(pady=10, padx=10, fill=tk.X)

        # Now Playing Frame
        now_playing_frame = tk.Frame(self.root, bg=GLASS_BLACK, relief=tk.FLAT, bd=2)
        now_playing_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            now_playing_frame,
            text="Now Playing",
            font=("Segoe UI", 11, "bold"),
            bg=GLASS_BLACK,
            fg=TEXT_WHITE
        ).pack(pady=5)

        self.track_label = tk.Label(
            now_playing_frame,
            text="No track playing",
            font=("Segoe UI", 10),
            bg=GLASS_BLACK,
            fg=TEXT_WHITE,
            wraplength=350
        )
        self.track_label.pack(pady=5)

        self.artist_label = tk.Label(
            now_playing_frame,
            text="",
            font=("Segoe UI", 9),
            bg=GLASS_BLACK,
            fg="#b3b3b3"
        )
        self.artist_label.pack()

        # Playlist Frame
        playlist_frame = tk.Frame(self.root, bg=GLASS_BLACK, relief=tk.FLAT, bd=2)
        playlist_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            playlist_frame,
            text="Target Playlist (for Add hotkey)",
            font=("Segoe UI", 11, "bold"),
            bg=GLASS_BLACK,
            fg=TEXT_WHITE
        ).pack(pady=5)

        tk.Label(playlist_frame, text="Playlist ID or URI:", bg=GLASS_BLACK, fg=TEXT_WHITE, font=("Segoe UI", 9)).pack(anchor=tk.W, padx=10)
        self.playlist_entry = tk.Entry(playlist_frame, bg="#2a2a2a", fg=TEXT_WHITE, insertbackground=TEXT_WHITE, relief=tk.FLAT, font=("Segoe UI", 9))
        self.playlist_entry.pack(fill=tk.X, padx=10, pady=2)
        if self.config.get('playlist_id'):
            self.playlist_entry.insert(0, self.config['playlist_id'])

        save_playlist_btn = tk.Button(
            playlist_frame,
            text="Save Playlist",
            command=self.save_playlist,
            bg="#2a2a2a",
            fg=SPOTIFY_GREEN,
            font=("Segoe UI", 9),
            relief=tk.FLAT,
            cursor="hand2"
        )
        save_playlist_btn.pack(pady=5)

        # Hotkeys Frame
        hotkeys_frame = tk.Frame(self.root, bg=GLASS_BLACK, relief=tk.FLAT, bd=2)
        hotkeys_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        tk.Label(
            hotkeys_frame,
            text="Global Hotkeys",
            font=("Segoe UI", 11, "bold"),
            bg=GLASS_BLACK,
            fg=TEXT_WHITE
        ).pack(pady=5)

        hotkeys = [
            ("Ctrl+Alt+N", "Next Track"),
            ("Ctrl+Alt+B", "Previous Track"),
            ("Ctrl+Alt+Space", "Play/Pause"),
            ("Ctrl+Alt+L", "Like Track"),
            ("Ctrl+Alt+A", "Add to Playlist"),
        ]

        for hotkey, description in hotkeys:
            hk_frame = tk.Frame(hotkeys_frame, bg=GLASS_BLACK)
            hk_frame.pack(fill=tk.X, padx=10, pady=2)

            tk.Label(
                hk_frame,
                text=hotkey,
                font=("Segoe UI", 9, "bold"),
                bg=GLASS_BLACK,
                fg=SPOTIFY_GREEN,
                width=20,
                anchor=tk.W
            ).pack(side=tk.LEFT)

            tk.Label(
                hk_frame,
                text=description,
                font=("Segoe UI", 9),
                bg=GLASS_BLACK,
                fg=TEXT_WHITE,
                anchor=tk.W
            ).pack(side=tk.LEFT)

        # Footer
        footer_label = tk.Label(
            self.root,
            text="Made with ♥ for Spotify lovers",
            font=("Segoe UI", 8),
            bg=SPOTIFY_BLACK,
            fg="#666666"
        )
        footer_label.pack(side=tk.BOTTOM, pady=5)

    def authenticate(self):
        """Authenticate with Spotify"""
        client_id = self.client_id_entry.get().strip()
        client_secret = self.client_secret_entry.get().strip()

        if not client_id or not client_secret:
            messagebox.showerror("Error", "Please enter both Client ID and Client Secret")
            return

        try:
            self.config['client_id'] = client_id
            self.config['client_secret'] = client_secret
            self.save_config()

            scope = "user-read-playback-state user-modify-playback-state user-library-modify user-library-read playlist-modify-public playlist-modify-private"

            auth_manager = SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri="http://localhost:8888/callback",
                scope=scope,
                cache_path=str(Path.home() / ".spotify_cache")
            )

            self.sp = spotipy.Spotify(auth_manager=auth_manager)

            # Test connection
            user = self.sp.current_user()

            self.status_label.config(text=f"● Connected as {user['display_name']}", fg="#44ff44")
            messagebox.showinfo("Success", f"Connected to Spotify as {user['display_name']}!")

            # Start update thread
            self.start_update_thread()

        except Exception as e:
            messagebox.showerror("Authentication Error", f"Failed to connect:\n{str(e)}")
            self.status_label.config(text="● Disconnected", fg="#ff4444")

    def save_playlist(self):
        """Save target playlist ID"""
        playlist_input = self.playlist_entry.get().strip()
        if playlist_input:
            # Extract ID from URI if needed
            if 'spotify:playlist:' in playlist_input:
                playlist_id = playlist_input.split(':')[-1]
            elif 'open.spotify.com/playlist/' in playlist_input:
                playlist_id = playlist_input.split('/')[-1].split('?')[0]
            else:
                playlist_id = playlist_input

            self.target_playlist_id = playlist_id
            self.config['playlist_id'] = playlist_id
            self.save_config()
            messagebox.showinfo("Success", "Playlist saved!")
        else:
            messagebox.showwarning("Warning", "Please enter a playlist ID or URI")

    def setup_hotkeys(self):
        """Setup global hotkeys"""
        try:
            keyboard.add_hotkey('ctrl+alt+n', self.next_track)
            keyboard.add_hotkey('ctrl+alt+b', self.previous_track)
            keyboard.add_hotkey('ctrl+alt+space', self.play_pause)
            keyboard.add_hotkey('ctrl+alt+l', self.like_track)
            keyboard.add_hotkey('ctrl+alt+a', self.add_to_playlist)
        except Exception as e:
            print(f"Hotkey setup error: {e}")

    def next_track(self):
        """Skip to next track"""
        if self.sp:
            try:
                self.sp.next_track()
                self.update_now_playing()
            except Exception as e:
                print(f"Next track error: {e}")

    def previous_track(self):
        """Go to previous track"""
        if self.sp:
            try:
                self.sp.previous_track()
                self.update_now_playing()
            except Exception as e:
                print(f"Previous track error: {e}")

    def play_pause(self):
        """Toggle play/pause"""
        if self.sp:
            try:
                playback = self.sp.current_playback()
                if playback and playback['is_playing']:
                    self.sp.pause_playback()
                else:
                    self.sp.start_playback()
            except Exception as e:
                print(f"Play/pause error: {e}")

    def like_track(self):
        """Like current track"""
        if self.sp and self.current_track:
            try:
                track_id = self.current_track['item']['id']
                self.sp.current_user_saved_tracks_add([track_id])
                self.show_notification("Track Liked! ♥")
            except Exception as e:
                print(f"Like track error: {e}")

    def add_to_playlist(self):
        """Add current track to target playlist"""
        if self.sp and self.current_track and self.target_playlist_id:
            try:
                track_uri = self.current_track['item']['uri']
                self.sp.playlist_add_items(self.target_playlist_id, [track_uri])
                self.show_notification("Added to Playlist!")
            except Exception as e:
                self.show_notification(f"Error: {str(e)}")
        elif not self.target_playlist_id:
            self.show_notification("No playlist set!")

    def show_notification(self, message):
        """Show a temporary notification"""
        notif = tk.Toplevel(self.root)
        notif.title("")
        notif.geometry("250x80")
        notif.configure(bg=GLASS_BLACK)
        notif.overrideredirect(True)

        # Position at bottom right of main window
        x = self.root.winfo_x() + self.root.winfo_width() // 2 - 125
        y = self.root.winfo_y() + self.root.winfo_height() - 100
        notif.geometry(f"+{x}+{y}")

        tk.Label(
            notif,
            text=message,
            font=("Segoe UI", 12, "bold"),
            bg=GLASS_BLACK,
            fg=SPOTIFY_GREEN
        ).pack(expand=True)

        notif.after(1500, notif.destroy)

    def update_now_playing(self):
        """Update now playing display"""
        if self.sp:
            try:
                self.current_track = self.sp.current_playback()
                if self.current_track and self.current_track['item']:
                    track = self.current_track['item']
                    track_name = track['name']
                    artists = ", ".join([artist['name'] for artist in track['artists']])

                    self.track_label.config(text=track_name)
                    self.artist_label.config(text=artists)
                else:
                    self.track_label.config(text="No track playing")
                    self.artist_label.config(text="")
            except Exception as e:
                print(f"Update error: {e}")

    def start_update_thread(self):
        """Start background thread to update now playing"""
        def update_loop():
            import time
            while True:
                self.update_now_playing()
                time.sleep(2)

        thread = threading.Thread(target=update_loop, daemon=True)
        thread.start()

    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = SpotifyHotkeyApp()
    app.run()
