import random
from time import sleep
import requests
from bs4 import BeautifulSoup
import moviepy.editor as mp
import ffmpeg
import os

# URL of the page to be scraped
# html = requests.get("https://mixkit.co/free-stock-video/luxury/")
html = requests.get(
    "https://mixkit.co/free-stock-video/discover/elegance/?page=5")
soup = BeautifulSoup(html.text, "html.parser")

# get all links where href starts with /free-stock-video/ and have a class
links = soup.find_all(
    "a", {"class": "item-grid-video-player__overlay-link", "href": True})
# get the href attribute from the link
links = [link["href"] for link in links]
# add the base url to the links
links = ["https://mixkit.co" + link for link in links]


def combine_audio(vidname, audname, outname, fps=60):
    import moviepy.editor as mpe
    my_clip = mpe.VideoFileClip(vidname)
    audio_background = mpe.AudioFileClip(audname)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(outname, fps=fps)


# get the first 10 videos
# links = links[:3]
video_count = 1
for link in links:
    video_html = requests.get(link)
    soup = BeautifulSoup(video_html.text, "html.parser")
    video = soup.find("video", {"class": "video-player__viewer", "src": True})
    video = video["src"]
    print(video)

    # download the video
    video = requests.get(video)
    with open("./videos/video" + str(video_count) + ".mp4", "wb") as f:
        f.write(video.content)

    # check video duration
    video = mp.VideoFileClip("./videos/video" + str(video_count) + ".mp4")
    if (video.duration < 12):
        video.close()
        # delete the video
        os.remove("./videos/video" + str(video_count) + ".mp4")
        continue


    # add audio
    combine_audio("./videos/video" + str(video_count) + ".mp4", "./music/music" + str(video_count) + ".mp3",
                  "./videos/video" + str(video_count) + "_with_audio.mp4")

    # crop to 9:16 with moviepy
    video = mp.VideoFileClip("./videos/video" + str(video_count) + "_with_audio.mp4")
    video = video.subclip(0, 12)
    video = video.resize(height=1920)
    video = video.crop(x1=0, y1=0, x2=1080, y2=1920)


    # add text to the video
    # random_quote = 
    # get text from file
    with open("./quotes/quotes.txt", "r") as f:
        quotes = f.readlines()
    # print random quote
    random_quote = random.choice(quotes)
    print(random_quote)
    txt_clip = mp.TextClip(random_quote, fontsize=70, color='white')
    txt_clip = txt_clip.set_pos('center').set_duration(12)
    video = mp.CompositeVideoClip([video, txt_clip])


    video.write_videofile("./videos/video" + str(video_count) + "_formated.mp4")

    
    # crop to 9:16 with ffmpeg-python
    # stream = ffmpeg.input("./videos/video" + str(video_count) + "_with_audio.mp4")
    # audio = ffmpeg.input("./music/music" + str(video_count) + ".mp3")
    # stream = ffmpeg.filter(stream, "crop", 405, 720, 0, 0)
    # stream = ffmpeg.output(stream, audio,  "./videos/video" + str(video_count) + "_formated.mp4")
    # ffmpeg.run(stream)
    

    video_count += 1
    if (video_count == 2):
        break
