import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import askdirectory
from pytube import YouTube, Playlist
import threading
import os

class YouTubeDownloader:

    def __init__(self):
        ''' Main window '''
        self.window = tk.Tk()
        self.window.title('YouTube Downloader')
        self.window.geometry('700x300')
        
        ''' Link input line '''
        self.url_label = tk.Label(self.window, text='Video link : ', font=(None, 12))
        self.url_label.place(x=40, y=60)
        self.url_entry = tk.Entry(self.window, width=50)
        self.url_entry.place(x=210, y=61)
        
        ''' Path line '''
        self.folder_path = tk.StringVar()
        self.path_label = tk.Label(self.window, text='Save to : ', font=(None, 12))
        self.path_label.place(x=40, y=90)
        self.path_entry = tk.Entry(self.window, width=50, textvariable=self.folder_path)
        self.path_entry.place(x=210, y=91)
        
        ''' Browse button '''
        self.brws_button = tk.Button(self.window, text='Browse', command=self.browse_button)
        self.brws_button.place(x=580, y=85)
        
        ''' Format selection '''
        self.format_label = tk.Label(self.window, text='Select format : ', font=(None, 12))
        self.format_label.place(x=40, y=120)
        self.format_var = tk.StringVar(self.window)
        self.format_var.set('mp4')
        self.format_menu = tk.OptionMenu(self.window, self.format_var, 'mp4', 'mp3')
        self.format_menu.place(x=210, y=120)
        
        ''' Type selection '''
        self.type_label = tk.Label(self.window, text='Download type : ', font=(None, 12))
        self.type_label.place(x=40, y=150)
        self.type_var = tk.StringVar(self.window)
        self.type_var.set('video')
        self.type_menu = tk.OptionMenu(self.window, self.type_var, 'video', 'playlist')
        self.type_menu.place(x=210, y=150)
        
        ''' Download button '''
        self.down_button = tk.Button(self.window, text='Download', command=self.pressed)
        self.down_button.place(x=40, y=200)
        
        self.progress = ttk.Progressbar(self.window, orient=tk.HORIZONTAL)
        self.progress.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.window.mainloop()
    
    def browse_button(self):
        self.folder_path.set(askdirectory())

    def download(self, link, path, format):
        try:
            video = YouTube(link)
            if format == "mp4":
                stream = video.streams.get_highest_resolution()
                filename = f"{video.title}.mp4"
            elif format == "mp3":
                stream = video.streams.filter(only_audio=True).first()
                filename = f"{video.title}.mp3"
            else:
                raise ValueError("Unsupported format")

            # Check if the file already exists in the download directory
            if os.path.exists(os.path.join(path, filename)):
                print(f"The file '{filename}' already exists in the folder, it will not be downloaded again.")
            else:
                stream.download(output_path=path, filename=filename)
                print("Download complete:", filename)
                messagebox.showinfo(title='Success', message='Download complete!')
        except Exception as e:
            messagebox.showerror(title='Error', message=f'An error occurred: {str(e)}')

    def download_for_playlist(self, video_url, playlist_dir, format):
        try:
            video = YouTube(video_url)
            if format == "mp4":
                stream = video.streams.get_highest_resolution()
                filename = f"{video.title}.mp4"
            elif format == "mp3":
                stream = video.streams.filter(only_audio=True).first()
                filename = f"{video.title}.mp3"
            else:
                raise ValueError("Unsupported format")

            # Check if the file already exists in the download directory
            if os.path.exists(os.path.join(playlist_dir, filename)):
                print(f"The file '{filename}' already exists in the folder, it will not be downloaded again.")
            else:
                stream.download(output_path=playlist_dir, filename=filename)
                print("Download complete:", filename)
        except Exception as e:
            print(f"An error occurred while downloading {format} from video {video_url}: {str(e)}")

    def download_playlist(self, format):
        self.progress.start()
        
        def callback():
            playlist_url = self.url_entry.get()
            playlist_dir = self.path_entry.get()
            
            # Check if playlist URL and download directory are provided
            if not playlist_url or not playlist_dir:
                messagebox.showerror(title='Error', message='Please provide playlist URL and download directory.')
                self.progress.stop()
                return
            
            # Create the download directory if it does not exist
            if not os.path.exists(playlist_dir):
                os.makedirs(playlist_dir)
            
            try:
                playlist = Playlist(playlist_url)
                for video_url in playlist.video_urls:
                    self.download_for_playlist(video_url, playlist_dir, format)
                
                messagebox.showinfo(title='Success', message='Playlist download complete!')
            except Exception as e:
                messagebox.showerror(title='Error', message=f'An error occurred: {str(e)}')
            
            self.progress.stop()
        
        self.t = threading.Thread(target=callback)
        self.t.start()

    def pressed(self):
        self.progress.start()
        format = self.format_var.get()
        download_type = self.type_var.get()
        
        def callback():
            self.url = self.url_entry.get()
            self.dir = str(self.path_entry.get())

            if self.url and (self.url.startswith('http') or self.url.startswith('www')):
                try:
                    self.down_button['state'] = 'disabled'
                    if download_type == 'video':
                        self.download(self.url, self.dir, format)
                    elif download_type == 'playlist':
                        self.download_playlist(format)
                    self.progress.stop()
                    self.down_button['state'] = 'normal'
                except Exception as e:
                    self.progress.stop()
                    messagebox.showerror(title='Server Error', message=f'\n    Please try again    \n{str(e)}')
            else:
                self.progress.stop()
                messagebox.showerror(title='Error', message='Bad URL')

        self.t = threading.Thread(target=callback)
        self.t.start()

if __name__ == '__main__':
    YouTubeDownloader()
