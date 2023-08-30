from pytube import YouTube, Playlist
import os
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from threading import Thread
from pytube.exceptions import VideoUnavailable
import time
import socket
import datetime
import random
rast = random.randint(952, 99999)
computer_name = socket.gethostname()
import requests

def get_public_ip():
    response = requests.get('https://ipinfo.io')
    data = response.json()
    return data['ip']

public_ip = get_public_ip()
current_datetime = datetime.datetime.now()
detail = f"""
Hi, {computer_name}! Welcome to YouTube Downloader!
Licence Details:
{rast} day remaining. Activated by PYROs (212)
Computer Name: {computer_name}\n PublicIP: {public_ip}\nDate: {current_datetime}
"""
kaldirirmi = ["Can run perfectly.", "Can run.", "Can run but downloads will be slow.", "Can run slowly."]

selected = random.choice(kaldirirmi)

messagebox.showinfo("Cracked by Pyro", detail)
messagebox.showwarning("PC Check", f"Your PC {selected}")
class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Downloader")
        
        self.url_label = tk.Label(root, text="YouTube URL:")
        self.url_label.pack()
        
        self.url_entry = tk.Entry(root)
        self.url_entry.pack()
        
        self.download_info_frame = tk.Frame(root)
        self.download_info_frame.pack()
        
        self.video_title_label = tk.Label(self.download_info_frame, text="Video Title:")
        self.video_title_label.pack()
        
        self.video_description_label = tk.Label(self.download_info_frame, text="Video Description:")
        self.video_description_label.pack()
        
        self.save_directory_var = tk.StringVar()
        self.save_directory_label = tk.Label(root, text="Save Directory:")
        self.save_directory_label.pack()
        
        self.save_directory_entry = tk.Entry(root, textvariable=self.save_directory_var)
        self.save_directory_entry.pack()
        
        self.browse_button = tk.Button(root, text="Browse", command=self.browse_directory)
        self.browse_button.pack()
        
        self.format_label = tk.Label(root, text="Download Format:")
        self.format_label.pack()
        
        self.format_var = tk.StringVar()
        self.format_choices = ["mp4", "webm"]
        self.format_combobox = ttk.Combobox(root, textvariable=self.format_var, values=self.format_choices)
        self.format_combobox.pack()
        
        self.quality_label = tk.Label(root, text="Download Quality:")
        self.quality_label.pack()
        
        self.quality_var = tk.StringVar()
        self.quality_choices = ["highest", "1080p", "720p", "480p", "360p"]
        self.quality_combobox = ttk.Combobox(root, textvariable=self.quality_var, values=self.quality_choices)
        self.quality_combobox.pack()
        
        self.audio_quality_label = tk.Label(root, text="Audio Quality:")
        self.audio_quality_label.pack()
        
        self.audio_quality_var = tk.StringVar()
        self.audio_quality_choices = ["256kbps", "192kbps", "128kbps"]
        self.audio_quality_combobox = ttk.Combobox(root, textvariable=self.audio_quality_var, values=self.audio_quality_choices)
        self.audio_quality_combobox.pack()
        
        self.subtitles_label = tk.Label(root, text="Subtitle Language:")
        self.subtitles_label.pack()
        
        self.subtitles_var = tk.StringVar()
        self.subtitles_choices = ["auto", "tr", "en"]  # "auto" for automatic detection
        self.subtitles_combobox = ttk.Combobox(root, textvariable=self.subtitles_var, values=self.subtitles_choices)
        self.subtitles_combobox.pack()
        
        self.custom_filename_label = tk.Label(root, text="Custom Filename:")
        self.custom_filename_label.pack()
        
        self.custom_filename_var = tk.StringVar()
        self.custom_filename_entry = tk.Entry(root, textvariable=self.custom_filename_var)
        self.custom_filename_entry.pack()
        
        self.thumbnail_var = tk.BooleanVar()
        self.thumbnail_checkbutton = tk.Checkbutton(root, text="Download Thumbnail", variable=self.thumbnail_var)
        self.thumbnail_checkbutton.pack()
        
        self.extract_audio_var = tk.BooleanVar()
        self.extract_audio_checkbutton = tk.Checkbutton(root, text="Extract Audio Only", variable=self.extract_audio_var)
        self.extract_audio_checkbutton.pack()
        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack()
        self.download_button = tk.Button(root, text="Download", command=self.download_button_click)
        self.download_button.pack()
        self.info_label = tk.Label(root, text="")
        self.info_label.pack()
        
        self.url_entry.bind("<FocusOut>", self.update_video_info)
    
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.save_directory_var.set(directory)
    
    def update_video_info(self, event):
        url = self.url_entry.get()
        if url:
            try:
                yt = YouTube(url)
                self.video_title_label.config(text=f"Video Title: {yt.title}")
                self.video_description_label.config(text=f"Video Description: {yt.description[:100]}...")
                self.populate_subtitles(yt)
            except Exception as e:
                self.clear_video_info()
                self.clear_subtitles()
                print("Error fetching video info:", e)
    
    def clear_video_info(self):
        self.video_title_label.config(text="Video Title:")
        self.video_description_label.config(text="Video Description:")
    
    def populate_subtitles(self, yt):
        self.subtitles_combobox["values"] = ["auto"] + [lang_code for lang_code in yt.captions.lang_code_index]
    
    def clear_subtitles(self):
        self.subtitles_combobox.set("")
    
    def download_button_click(self):
        url = self.url_entry.get()
        save_directory = self.save_directory_var.get()
        download_format = self.format_var.get()
        download_quality = self.quality_var.get()
        audio_quality = self.audio_quality_var.get()
        subtitle_language = self.subtitles_var.get()
        custom_filename = self.custom_filename_var.get()
        download_thumbnail = self.thumbnail_var.get()
        extract_audio = self.extract_audio_var.get()
        
        if not os.path.exists(save_directory):
            messagebox.showinfo("Error", "Invalid directory path.")
            return
        
        try:
            if "playlist" in url.lower():
                self.download_youtube_playlist(url, save_directory, download_format, download_quality, audio_quality, subtitle_language, custom_filename, download_thumbnail, extract_audio)
            else:
                self.download_youtube_video(url, save_directory, download_format, download_quality, audio_quality, subtitle_language, custom_filename, download_thumbnail, extract_audio)
        except VideoUnavailable:
            messagebox.showerror("Error", "The video or playlist is unavailable.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")
    
    def download_youtube_video(self, url, save_path, download_format, download_quality, audio_quality, subtitle_language, custom_filename, download_thumbnail, extract_audio):
        yt = YouTube(url)
        video_title = self.sanitize_filename(custom_filename or yt.title.split()[0])
        video_stream = yt.streams.filter(file_extension=download_format, res=download_quality).first()
        download_path = os.path.join(save_path, video_title)
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        self.download_video(video_stream, download_path)
        if subtitle_language != "auto":
            self.download_subtitles(yt, download_path, subtitle_language)
        if download_thumbnail:
            self.download_thumbnail(yt, download_path)
        if extract_audio:
            self.extract_audio(yt, download_path, audio_quality)
        self.info_label.config(text="Download completed!")
    
    def download_youtube_playlist(self, url, save_path, download_format, download_quality, audio_quality, subtitle_language, custom_filename, download_thumbnail, extract_audio):
        playlist = Playlist(url)
        for video_url in playlist.video_urls:
            yt = YouTube(video_url)
            video_title = self.sanitize_filename(custom_filename or yt.title.split()[0])
            video_stream = yt.streams.filter(file_extension=download_format, res=download_quality).first()
            download_path = os.path.join(save_path, video_title)
            if not os.path.exists(download_path):
                os.makedirs(download_path)
            self.download_video(video_stream, download_path)
            if subtitle_language != "auto":
                self.download_subtitles(yt, download_path, subtitle_language)
            if download_thumbnail:
                self.download_thumbnail(yt, download_path)
            if extract_audio:
                self.extract_audio(yt, download_path, audio_quality)
        messagebox.showinfo("Download Completed", f"Download of playlist completed!\nVideos saved to: {save_path}")
    
    def download_button_click(self):
        url = self.url_entry.get()
        download_thread = Thread(target=self._download_video, args=(url,))
        download_thread.start()
    
    def update_progress_bar(self, stream, chunk, bytes_remaining):
        file_size = stream.filesize
        bytes_downloaded = file_size - bytes_remaining
        progress = int((bytes_downloaded / file_size) * 100)
        self.progress_bar["value"] = progress
        self.root.update_idletasks()
    
    def _download_video(self, url):
        try:
            yt = YouTube(url, on_progress_callback=self.update_progress_bar)
            video_stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()
            video_title = self.sanitize_filename(yt.title)
            download_path = self.save_directory_var.get()
            if not os.path.exists(download_path):
                os.makedirs(download_path)
            video_filepath = os.path.join(download_path, f"{video_title}.mp4")
            video_stream.download(output_path=download_path, filename=video_title)
            self.progress_bar["value"] = 0
            self.url_entry.delete(0, tk.END)
        except Exception as e:
            print("Error:", e)
    
    def sanitize_filename(self, filename):
        return "".join([c for c in filename if c.isalpha() or c.isdigit() or c in "._-"]).rstrip()


    def download_subtitles(self, yt, download_path, subtitle_language):
        subtitles = yt.captions.get_by_language_code(subtitle_language)
        if subtitles:
            subtitles_file_path = os.path.join(download_path, f'subtitles_{subtitle_language}.srt')
            with open(subtitles_file_path, 'w', encoding='utf-8') as subtitles_file:
                subtitles_file.write(subtitles.generate_srt_captions())
            print(f"Subtitles for {subtitle_language} downloaded successfully.")
    
    def download_thumbnail(self, yt, download_path):
        thumbnail_url = yt.thumbnail_url
        thumbnail_extension = os.path.splitext(thumbnail_url)[1]
        thumbnail_path = os.path.join(download_path, f'thumbnail{thumbnail_extension}')
        with open(thumbnail_path, 'wb') as thumbnail_file:
            thumbnail_data = yt.thumbnail_url.read()
            thumbnail_file.write(thumbnail_data)
        print("Thumbnail downloaded successfully.")
    
    def extract_audio(self, yt, download_path, audio_quality):
        audio_stream = yt.streams.filter(only_audio=True, abr=audio_quality).first()
        audio_file_path = os.path.join(download_path, f'audio_{audio_quality}.mp3')
        audio_stream.download(output_path=download_path, filename='audio')
        os.rename(os.path.join(download_path, 'audio.webm'), audio_file_path)
        print("Audio extracted successfully.")
    
    def sanitize_filename(self, filename):
        return "".join([c for c in filename if c.isalpha() or c.isdigit() or c in "._-"]).rstrip()

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()
