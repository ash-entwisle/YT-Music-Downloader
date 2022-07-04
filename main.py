import os
from re import search
from pytube import YouTube, Playlist
from moviepy.editor import VideoFileClip

from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3  
import mutagen.id3  
from mutagen.id3 import ID3, TIT2, TIT3, TALB, TPE1, TRCK, TYER  


def download(url: str, path: str):                                                      # downloads stream and converts to mp3
    video = YouTube(url)                                                                # initialises video object with url
    stream = video.streams.get_by_itag(18)                                              # gets 360p stream
    stream.download()                                                                   # downloads the stream
    filename = stream.default_filename                                                  # gets file name of the stream
    with VideoFileClip(filename) as clip:                                               # sets up mp4 to be clipped
        clip.audio.write_audiofile(path + filename[:-4] + ".mp3")                       # takes mp3 data and saves to path
        os.remove(filename)                                                             # removes mp4
    return path + filename[:-4] + ".mp3"                                                # returns path of mp3

def setID3(path: str, trackno: str):                                                    # sets ID3 metadata
    title = path.split("/")[-1][:-4]                                                    # title = filename
    album = path.split("/")[-2]                                                         # album = album folder
    artst = path.split("/")[-3]                                                         # artist = artist folder
    mp3file = MP3(path, ID3=EasyID3)                                                    # get data
    mp3file["album"] = [album]                                                          # set album
    mp3file["title"] = [title]                                                          # set title
    mp3file["artist"] = [artist]                                                        # set artist
    mp3file["albumartist"] = [artist]                                                   # set artist
    mp3file["tracknumber"] = [trackno]                                                  # set track number
    mp3file.save()                                                                      # save

def main(url: str, artist: str, album: str):                                            # main function, unpacks url
    path = f"{artist}/{album}/"                                                         # form path
    if not os.path.exists(artist):                                                      # if there is not a folder for artist
        os.mkdir(artist)                                                                # make one
    if not os.path.exists(path):                                                        # if there is not a folder for album
        os.mkdir(path)                                                                  # make one

    if search("playlist", url):                                                         # if playlist in string:
        playlist = Playlist(url)                                                        # get a list of urls
        for i in range(len(playlist)):                                                  # for index in url
            target = download(playlist[i], path)                                        # download url, set target to path
            setID3(target, i+1)                                                         # set ID3 data

    else:                                                                               # else:
        target = download(url, path)                                                    # download url, set target to path
        setID3(target, "1")                                                             # set ID3 data
        
    return True                                                                         # if no errors, return true

if __name__ == "__main__":                                                              # when file is run, do this:
    valid = False                                                                       # assume invalid
    while not valid:                                                                    # while link is not valid
        link = input("Link   >> ")                                                      # get user to enter a link
        valid = search("^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.", link)    # checks if it is a yt link
    
    if search("\?list=", link):                                                         # if its a playlist
        split = link.split("?list=")                                                    # split to get list code
        isplaylist = input("Is this a playlist (y/N) >> ")                              # checks if user wants to treat it as a playlist
        if isplaylist.upper() in ["Y", "YES"]:                                          # if yes...
            link = f"https://www.youtube.com/playlist?list={split[-1]}"                 # forms playlist link

    artist = input("Artist >> ")                                                        # get artist
    album = input("Album  >> ")                                                         # get album
    
    complete = main(link, artist, album)                                                # runs main and waits until completion

    if complete:                                                                        # if true
        print("File(s) Downloaded Successfuly!")                                        # say done
    else:                                                                               # else
        print("An error has occured ")                                                  # say smth went wrong
