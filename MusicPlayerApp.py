from tkinter import Tk, Listbox, Button, Menu, Label, Entry, Toplevel, messagebox, StringVar, SINGLE, ACTIVE, END, HORIZONTAL
import tkinter.font as font
from tkinter.ttk import Combobox
from tkinter import filedialog
import os
from pygame import mixer as pygamemixer
import shutil
from dLoaderLibs import SearchYoutube, downloadYouTubeAudio, convert_to_wav
import pydub
class MP:
    '''Music Player
    Music player class with YouTube download functionality, using the youtubesearchpython and pytube modules
    currently programmed to work only with .wav files, as .mp3/.mp4 files occasionally fail to load.
    Other sound files that are not .wav may still be used, but are converted to wav before being implemented into
    the music player.

    Example Use:

    from MusicPlayerApp import MP

    MusicPlayer = MP()

    MusicPlayer.initialiseMixer() 
    MusicPlayer.initialiseWidgets()
    MusicPlayer.RunMusicPlayer()
    '''
    def __init__(self):

        # PyGame audio mixer
        self.music_mixer = pygamemixer
        self.music_mixer.pre_init(44100, 16, 2, 4096)
        # Music Player main window
        self.root = Tk()
        self.root.title("Music Player")
        self.root.resizable(False, False)

        # Widgets for YouTube downloader form (Toplevel window)
        self.downloader_widgets = {
            "title_label": None,
            "search_label": None,
            "search_input": None,
            "num_results_label": None,
            "results_dropdown": None,
            "display_button": None,
            "results_listbox": None,
            "filename_label": None,
            "filename_input": None,
            "download_button": None
        }

        # font variable to, upon widget declaration, select which font to use
        self.defined_font = font.Font(family='Helvetica')

        # Main window widgets
        # Widgets are all added to self.root in the order they are declared here.
        # Changing the order of widgets in this dictionary changes the order in which
        # they are displayed in the main window.
        self.main_window_widgets = {
            "songs_list" : Listbox(self.root,selectmode=SINGLE,bg="maroon",fg="white",font=('arial',15),height=12,width=44,selectbackground="gray",selectforeground="black"),
            "option_menu": Menu(self.root),
            "play_button" : Button(self.root,text="Play",width=8,command=self.Play, bg="black", fg="white"),
            "pause_button" : Button(self.root,text="Pause",width=8,command=self.Pause, bg="black", fg="white"),
            "stop_button" : Button(self.root,text="Stop",width=8,command=self.Stop, bg="black", fg="white"),
            "resume_button" : Button(self.root,text="Resume",width=8,command=self.Resume, bg="black", fg="white"),
            "previous_button" : Button(self.root,text="Prev",width=8,command=self.Previous, bg="black", fg="white"),
            "next_button" : Button(self.root,text="Next",width=8,command=self.Next, bg="black", fg="white")
        }
        
        # Variable to store the song folder currently C:\Users\username\MusicPlayer\Songs\
        # You can change this to whatever/wherever you want it to be.
        self.song_folder = os.path.join(os.environ['HOMEDRIVE'], os.environ['HOMEPATH'], "MusicPlayer", "Songs", "")

        # If the song folder does not already exist, create it
        if not os.path.exists(self.song_folder):
            os.makedirs(self.song_folder)

        # Dictionary to store information on each YouTube search result
        # stores different values each time SearchYoutube() is called
        # stored as {"videoID" : videoTitle, ...}
        self.search_results = {}
        self.video_duration = []

    def initialiseWidgets(self):
        '''Function to initialise the widgets of the main window (the music player)
        '''
        # Configure and initialise song list and main window buttons
        # This is the widget that shows in, descending order, all songs
        self.main_window_widgets["songs_list"].grid(columnspan=9)

        for i, widget in enumerate(self.main_window_widgets.values()):
            if isinstance(widget, Button): # Check to only configure font for buttons
                widget['font'] = self.defined_font
                widget.grid(row=2, column=i)

        # Configure and initialise option menu bar, with its respective options
        self.root.config(menu=self.main_window_widgets['option_menu'])
        self.main_window_widgets['option_menu'].add_command(label="Add Song", command=self.addsong)
        self.main_window_widgets['option_menu'].add_command(label="Delete Song", command=self.deletesong)
        self.main_window_widgets['option_menu'].add_command(label="Download Song", command=self.OpenSongDownloaderWindow)

        self.add_downloaded_songs_to_listbox()

    def initialiseMixer(self):
        self.music_mixer.init()

    def Play(self):
        selected_song=self.main_window_widgets['songs_list'].get(ACTIVE)
        if len(selected_song):
            self.music_mixer.music.load(f"{self.song_folder}{selected_song}.wav")
            self.music_mixer.music.play()

            selected_index = self.main_window_widgets['songs_list'].curselection() # Returns a tuple of, (x,) where x is selected index
            
            self.main_window_widgets['songs_list'].selection_clear(0, END)
            self.main_window_widgets['songs_list'].activate(selected_index[0])
            self.main_window_widgets['songs_list'].selection_set(selected_index[0])
        else:
            messagebox.showerror(title="No song selected!", message="Please select a song")
    
    def Pause(self):
        self.music_mixer.music.pause()

    def Stop(self):
        self.music_mixer.music.stop()

    def Resume(self):
        self.music_mixer.music.unpause()
    
    def _play_next_song(self, next_song_index : int):
        '''
        This method is used in the Previous() and Next() functions below
        next_song_index is not always the index of next song,
        see _play_next_song() function calls in Previous() and Next() below
        
        '''
        current_song = self.main_window_widgets['songs_list'].get(next_song_index)
        self.music_mixer.music.load(f"{self.song_folder}{current_song}.wav")
        self.music_mixer.music.play()
        self.main_window_widgets['songs_list'].selection_clear(0, END)
        self.main_window_widgets['songs_list'].activate(next_song_index)
        self.main_window_widgets['songs_list'].selection_set(next_song_index)

    def Previous(self):
        '''Plays the song before the currently selected song in the songs list
        '''

        if not self.main_window_widgets['songs_list'].curselection():
            messagebox.showerror(title="No song selected", message="Please select a song first")
            return
        else:
            all_songs = self.main_window_widgets['songs_list'].get(0, END)
            selected_index = self.main_window_widgets['songs_list'].curselection()
            # If the selected song is not at the start of the song list, play the previous song
            if selected_index[0] - 1 >= 0:
                self._play_next_song(selected_index[0] - 1)
            else:
                # else, play the song at the end of the song list
                self._play_next_song(len(all_songs) - 1)

    def Next(self):
        '''Plays the song after the currently selected song in the songs list
        '''
        if not self.main_window_widgets['songs_list'].curselection():
            messagebox.showerror(title="No song selected", message="Please select a song first")
            return
        else:
            all_songs = self.main_window_widgets['songs_list'].get(0, END)
            selected_index = self.main_window_widgets['songs_list'].curselection()
            # Play the first song in the song list if chosen song is at the end of the list
            
            if selected_index[0] + 1 != len(all_songs):
                self._play_next_song(selected_index[0] + 1)
            else:
                self._play_next_song(0)

    def add_downloaded_songs_to_listbox(self):
        '''Called on program startup to add all song files in song directory to the songs list for playing
        '''
        for file in os.listdir(self.song_folder):
            if file.endswith(('.wav')):
                self.main_window_widgets['songs_list'].insert(END, file.replace(".wav", ""))

    def addsong(self):
        ''' First option of the music player option menu
        Asks the user for a .wav file through the OS's default file explorer, then adds the song
        to the songs list.
        '''
        # temp_song is a tuple with the first value being the chosen file's name
        # usually returns a 2nd (empty) value
        temp_song = filedialog.askopenfilenames(initialdir=self.song_folder, title="Choose a song", filetypes=(("wav Files","*.wav"),))
        all_songs = self.main_window_widgets['songs_list'].get(0, END)

        for song in temp_song:
            song_file = (song[song.rindex("/")+1:]).replace(".wav", "")
            # Only add the selected song to the song list if it is not there already
            if song_file not in all_songs:
                self.main_window_widgets['songs_list'].insert(END, song_file)
            # If the chosen file is not already in the designated song folder,
            # copy it to the song folder
            if not os.path.isfile(f"{self.song_folder}{song_file}"):
                shutil.copy(f"{song}", f"{self.song_folder}{song_file}")

    def deletesong(self):
        if self.main_window_widgets['songs_list'].size() > 0:
            current_song = self.main_window_widgets['songs_list'].curselection()

            if current_song:
                if messagebox.askyesno(message="Are you sure? This will permanently delete the song!"):
                    self.music_mixer.stop()
                    os.remove(os.path.join(self.song_folder, f"{self.main_window_widgets['songs_list'].get(current_song[0])}.wav"))
                    self.main_window_widgets['songs_list'].delete(current_song[0])
            else:
                messagebox.showerror(title="Error!", message="No song selected")
        else:
            messagebox.showerror(title="Error!", message="Song list is empty, cannot delete anything!")

    def display_results(self):
        search_term = self.downloader_widgets['search_input'].get()
        if not search_term:
            messagebox.showerror(title="Error!", message="Please enter a search term")
            return
        
        try:
            num_results = int(self.downloader_widgets['results_dropdown'].get())
        except ValueError:
            messagebox.showerror(title="Error!", message="Something went wrong...")
        
        self.search_results, self.video_duration = SearchYoutube(search_term, num_results)
        self.downloader_widgets["results_listbox"].delete(0, END)
        
        # search_results.keys() returns video IDs, .values() returns the video titles
        if len(self.search_results) == 0:
            messagebox.showwarning(title="Error", message="All videos are longer than 10 minutes. Try to use different keywords, such as short")
        else:
            for index, result in enumerate(self.search_results.values()):
                self.downloader_widgets["results_listbox"].insert(END, f"{result} --> {self.video_duration[index]}")

        self.downloader_widgets["filename_input"].delete(0, END)
        self.downloader_widgets["filename_input"].insert(0, search_term)

    def download_song(self):
        vidLink = "https://youtube.com/watch?v="
        selected_index = self.downloader_widgets["results_listbox"].curselection()
        user_file_name = self.downloader_widgets["filename_input"].get()

        if len(self.downloader_widgets["results_listbox"].get(0, END)) == 0:
            messagebox.showerror(title="Error", message="There is no music to select from to download. Please try a different search term.")
            return
        elif not selected_index:
            messagebox.showerror(title="Error", message="Please select an item to download")
            return

        if not user_file_name:
            messagebox.showerror(title="Error", message="You must enter a file name")
            return
        
        selected_result = self.downloader_widgets["results_listbox"].get(selected_index)

        video_id = list(self.search_results.keys())[selected_index[0]]
        vidLink += video_id
        downloadYouTubeAudio(vidLink, self.song_folder, user_file_name)
        convert_to_wav(os.path.join(self.song_folder, f"{user_file_name}.mp4"), os.path.join(self.song_folder, f"{user_file_name}.wav")) # After downloading, convert the file to WAV

        self.main_window_widgets["songs_list"].insert(END, user_file_name)
        messagebox.showinfo(message=f"Succesfully downloaded{selected_result}")

    
    def create_downloader_widgets(self, window):
        '''Initialise widgets for the Toplevel YouTube downloader form window.
        Changing the order in which each widget is declared here does not change
        the order in which they are added to the downloader window.
        To change the order, modify the order of the self.downloader_widgets dictionary
        '''
        self.downloader_widgets["title_label"] = Label(window, text="YouTube Music Downloader", font=("Helvetica", 16))
        self.downloader_widgets["search_label"] = Label(window, text="Enter Search Term:")
        self.downloader_widgets["search_input"] = Entry(window, width=40)
        self.downloader_widgets["num_results_label"] = Label(window, text="Select Number of Results:")
        self.downloader_widgets["results_dropdown"] = Combobox(window, values=[i+1 for i in range(20)])
        self.downloader_widgets["display_button"] = Button(window, text="Display Results", command=self.display_results)
        self.downloader_widgets["results_listbox"] = Listbox(window, selectmode=SINGLE, width=50, height=10)
        self.downloader_widgets["filename_label"] = Label(window, text="Enter what to name the file (without extension):")
        self.downloader_widgets["filename_input"] = Entry(window, width=40)
        self.downloader_widgets["download_button"] = Button(window, text="Download", command=self.download_song)

    def init_download_window(self):
        downloader_window = Toplevel(self.root)
        # Hide the window, to prevent it being shown on program startup
        downloader_window.withdraw()
        self.create_downloader_widgets(downloader_window)
        return downloader_window
    
    def OpenSongDownloaderWindow(self):
        '''Used by the "Download Song" option of the music player menu.
        Opens the Toplevel YouTube downloader form
        '''
        downloader_window = self.init_download_window()
        downloader_window.resizable(False, False)
        # Reveal the window
        downloader_window.deiconify()
        # Variable used to store the value of search results to show
        num_results_holder = StringVar()
        self.downloader_widgets["results_dropdown"].config(textvariable=num_results_holder, width=5)

        self.root.after(100, lambda: self.downloader_widgets["results_dropdown"].set("10"))
        
        for widget in self.downloader_widgets.values():
            widget.pack()
        
        # Prevent music player from being used while the song downloader window is active
        downloader_window.grab_set()

    def RunMusicPlayer(self):
        '''Begins the tkinter mainloop of the music player
        '''
        self.root.mainloop()