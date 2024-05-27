from pytube import YouTube
from pytube import Playlist
from pytube.exceptions import VideoUnavailable

def titleStringTrim(Object):
    #Replaces string text python does not like from the title
    newTitle = Object.title
    newTitle = newTitle.replace('"',"")
    newTitle = newTitle.replace('\\', '')
    newTitle = newTitle.replace('/', '')
    newTitle = newTitle.replace(':', '')
    return newTitle

def doPlaylist(ytLink):
        try:
            playlist = Playlist(ytLink)
            counter = 1
            print(f"Started Download of Playlist:{playlist.title}")
            for video in playlist.videos:
                try:
                    #Obtaining the stream with the highest abr (average bit rate)
                    #The highest abr always contains the itag = 251  
                    stream = video.streams.get_by_itag(251)
                    stream.download("C:\Github\Personal-Projects\ytmp3\YTdownloads\Playlist",titleStringTrim(video)+".mp3")
                    print(f"Downloaded: {video.title} [{counter}/{len(playlist.videos)}]")
                    counter += 1
                except VideoUnavailable:
                    print(f"Video {video.title} is unavaialable, skipping.")
                except:
                    print(f"Error Downloading {video.title}")
        except:
            print("Error: Problem with link. Please Try Again")
    

def Download(ytLink):

    #Check if link is a playlist link
    if "&list=" in ytLink:
        doPlaylist(ytLink)
    else:
        try:
            youtube = YouTube(ytLink)
            try:
                #Obtaining the stream with the highest abr (average bit rate)
                #The highest abr for audio always contains the itag = 251
                stream = youtube.streams.get_by_itag(251)
                print(f"Downloading: {youtube.title}.....")
                stream.download("C:\Github\Personal-Projects\ytmp3\YTdownloads",titleStringTrim(youtube)+".mp3")
                print(f"Downloaded: {youtube.title}")
            except VideoUnavailable:
                print(f"Video {youtube.title} is unavaialable.")
            except:
                print(f"Error Downloading {youtube.title}")
        except:
            print("Error: Problem with link. Please Try Again")

while True:
    ytLink = input("Paste YouTube link/Playlist link:")
    Download(ytLink)
    
    
