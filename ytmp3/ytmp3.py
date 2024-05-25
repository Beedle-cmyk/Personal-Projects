from pytube import YouTube
from pytube import Playlist

#https://www.youtube.com/watch?v=gjSqjnuPGJA

def Download(ytLink):
    
    #Checking if the link is a playlist link
    if "&list=" in ytLink:
        playlist = Playlist(ytLink)

    else:
        #Object instantiation
        youtube = YouTube(ytLink)
        try:
            #Obtaining the stream with the highest abr (average bit rate)
            #The highest abr always contains the itag = 251
            stream = youtube.streams.get_by_itag(251)
            print(f'Downloading: {youtube.title}.....')
            stream.download("C:\Github\Personal-Projects\ytmp3\YTdownloads",youtube.title+".mp3")
            print("Pass")
        except:
            print("Error")

while True:
    ytLink = input("Paste YouTube link/Playlist link:")
    Download(ytLink)