from pytube import YouTube

#https://www.youtube.com/watch?v=gjSqjnuPGJA

def Download(ytLink):
    #Object instantiation
    youtube = YouTube(ytLink)
    try:
       #Obtaining the stream with the highest abr (average bit rate)
       #The highest abr always contains the itag = 251
       stream = youtube.streams.get_by_itag(251)
       stream.download("C:\Github\Personal-Projects\ytmp3\YTdownloads",youtube.title+".mp3")
       print("Pass")
    except:
        print("Error")


ytLink = input("Paste YouTube link:")
Download(ytLink)