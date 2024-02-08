from pytube import YouTube
from youtubesearchpython import VideosSearch
import os
from moviepy.editor import AudioFileClip


def convert_to_wav(input_file, output_file) -> None:
    if not os.path.exists(input_file):
        print(f"Error: File not found at {input_file}")
        return
    try:
        audio = AudioFileClip(input_file)
    except Exception as e:
        print(f"Error loading audio file: {e}")
        return

    audio.write_audiofile(output_file, codec='pcm_s16le', fps=44100)

    print(f"Conversion completed. Output saved to {output_file}")

    # Remove the original audio file after successful conversion
    try:
        os.remove(input_file)
        print(f"Original audio file removed: {input_file}")
    except Exception as e:
        print(f"Error removing original audio file: {e}")


def SearchYoutube(searchTerm : str, numResults : int) -> tuple[dict[str, str], list[str]]:
    '''Returns a dictionary - videoIDs - in the format {"videoID" - "videoTitle"}
    where video id is the id later used in the youtube.com/watch?v=... link
    
    Also returns a list of corresponding video durations, used to display how long each video is
    when displaying search results
    '''
    videos = VideosSearch(searchTerm, numResults).result()

    videoIDs = {}
    video_duration = []

    for video in videos["result"]:
        if video['duration'] == None:
            continue
        elif len(video['duration'].split(":")) > 2 or int(video['duration'].split(":")[0]) > 10:
            continue
        else:
            videoIDs[video['id']] = video['title']
            video_duration.append(video['duration'])

    return videoIDs, video_duration

def downloadYouTubeAudio(videoLink : str, download_dir : str, file_name : str) -> None:

    YouTube(url=videoLink).streams.filter(only_audio=True).first().download(output_path=download_dir, filename=f"{file_name}.mp4")