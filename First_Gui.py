import shutil
import webbrowser
import pytube
import pystray
import threading
from PIL import Image
from pystray import MenuItem as item
from tkinter import filedialog
import tkinter as tk
import os
import sys
import winreg

# Define the download function for individual videos
def download_video(url):
    youtube = pytube.YouTube(url)
    video = youtube.streams.get_highest_resolution()
    save_path = filedialog.askdirectory()  # Prompt the user to select a download directory
    if save_path:
        video.download(save_path)

# Define the download function for playlists
def download_playlist(url):
    playlist = pytube.Playlist(url)
    save_path = filedialog.askdirectory()  # Prompt the user to select a download directory
    if save_path:
        for video_url in playlist.video_urls:
            youtube = pytube.YouTube(video_url)
            video = youtube.streams.get_highest_resolution()
            video.download(save_path)

# Define the function to open a URL in the default web browser
def open_url(url):
    webbrowser.open(url)
#Force Shut down The program
def force_quit():
    os._exit(0)

# Define the menu items
menu_items = [
    item('Download Video', lambda: threading.Thread(target=show_download_window, args=(download_video,)).start()),
    item('Download Playlist', lambda: threading.Thread(target=show_download_window, args=(download_playlist,)).start()),
    item('Open Website', lambda: open_url('https://example.com')),
    item('Exit', force_quit),
]

# Define the system tray icon
image = Image.open("icon.png")  # Replace "icon.png" with the path to your icon image

def show_download_window(download_function):
    # Create the download window
    download_window = tk.Tk()
    download_window.title("Download Video")

    # Function to handle the download button click
    def download_button_clicked():
        url = url_entry.get()
        threading.Thread(target=download_function, args=(url,)).start()
        download_window.destroy()

    # Create the URL label and entry
    url_label = tk.Label(download_window, text="Video URL:")
    url_label.pack()
    url_entry = tk.Entry(download_window, width=50)
    url_entry.pack()

    # Create the download button
    download_button = tk.Button(download_window, text="Download", command=download_button_clicked)
    download_button.pack()

    download_window.mainloop()

def on_menu_exit(icon, item):
    icon.stop()

# Create the system tray icon
menu = (item for item in menu_items)
pystray.Icon("Youtube Downloader", image, "Yt Downloader", menu, on_exit=on_menu_exit).run()

# Add the program to Windows startup
def add_to_startup():
    startup_path = os.path.join(os.environ["APPDATA"], "Microsoft\\Windows\\Start Menu\\Programs\\Startup")
    script_path = os.path.abspath(sys.argv[0])
    script_name = os.path.basename(script_path)
    destination = os.path.join(startup_path, script_name)

    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", 0,
                                      winreg.KEY_SET_VALUE)
        winreg.SetValueEx(registry_key, "YouTube Downloader", 0, winreg.REG_SZ, script_path)
        winreg.CloseKey(registry_key)

        # Copy the script to the startup folder
        if not os.path.exists(destination):
            shutil.copyfile(script_path, destination)
    except Exception as e:
        print("Error adding to startup:", str(e))

add_to_startup()
