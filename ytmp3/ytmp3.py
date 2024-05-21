from pytube import YouTube

#https://www.youtube.com/watch?v=gjSqjnuPGJA
def Download(ytLink):
    youtube = YouTube(ytLink)
    youtube.streams.filter(only_audio=True)
    try:
       stream = youtube.streams.get_by_itag(251)
       stream.download("C:\Github\Personal-Projects\ytmp3\YTdownloads",youtube.title+".mp3")
       print("Pass")
    except:
        print("Error")


ytLink = input("Paste YouTube link:")
Download(ytLink)

