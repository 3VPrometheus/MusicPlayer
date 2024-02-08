# MusicPlayer
A simple music player, with YouTube download functionality.

To run the music player:

from MusicPlayerApp import MP

MusicPlayer = MP()

MusicPlayer.initialiseMixer()
MusicPlayer.initialiseWidgets()
MusicPlayer.RunMusicPlayer()

You can use this to play any audio file that is of the .wav format. You can also use the YouTube download feature I have added, to download audio directly from youtube (automatically converted to .wav).
Currently, there are some "key" missing features, such as the ability to skip through a playing song using a slider, or a label showing what position the song is at. These feature will be added at some point in the future as I continue to work on this simple project. In all honesty, though this was very enjoyable to code up; through several frustrating coding sessions, I decided to leave sections of the program as-is as long as it worked. They will be improved later, and I am always open to any suggestions should you have any.

I am aware that there can be many improvements to the program, such as effieciency, separation of concerns, additional features, etc. but this is just something that I created, and decided to share, to learn tkinter for any future projects that may require a GUI.

One of my other reasons for making this is because I got sick of listening to 3 30 second unskipabble ads on Spotify, and decided to give them a run for their money (Not really, of course, but the advertisements *are* a real pain in the ass!). 

For the time being, this is the first working version that is open for anybody to use as they please.
