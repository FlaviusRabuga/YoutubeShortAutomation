from pytube import YouTube
from pytube import Playlist
from pydub import AudioSegment
from pydub.utils import make_chunks

# extrag video url from youtube playlist

playlist = Playlist("https://www.youtube.com/playlist?list=PLeT6vLkd5bElXBNc2ky9wNiz71G77i6EF")
index = 0
for url in playlist.video_urls:
    index += 1
    #get music from youtube
    yt = YouTube(url)
    yt.streams.filter(only_audio=True).first().download(filename="./music/music" + str(index) + ".mp3")



    myaudio = AudioSegment.from_file("./music/music" + str(index) + ".mp3")
    myaudio = myaudio[13000:25000]
    myaudio.export("./music/music" + str(index) + ".mp3", format="mp3")
