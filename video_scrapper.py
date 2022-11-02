import requests
from bs4 import BeautifulSoup
import moviepy.editor as mp
import ffmpeg

# URL of the page to be scraped
# html = requests.get("https://mixkit.co/free-stock-video/luxury/")
html = requests.get("https://mixkit.co/free-stock-video/discover/sport-cars/")
soup = BeautifulSoup(html.text, "html.parser")

# get all links where href starts with /free-stock-video/ and have a class
links = soup.find_all("a", {"class": "item-grid-video-player__overlay-link", "href": True})
#get the href attribute from the link
links = [link["href"] for link in links]
# add the base url to the links
links = ["https://mixkit.co" + link for link in links]

#get the first 10 videos
links = links[:3]
video_count = 0
for link in links:
    video_count += 1
    video_html = requests.get(link)
    soup = BeautifulSoup(video_html.text, "html.parser")
    video = soup.find("video" , {"class": "video-player__viewer", "src": True})
    video = video["src"]
    print(video)

    # download the video
    video = requests.get(video)
    with open("./videos/video" + str(video_count) + ".mp4", "wb") as f:
        f.write(video.content)

    # crop to 9:16 with ffmpeg-python
    stream = ffmpeg.input("./videos/video" + str(video_count) + ".mp4")
    stream = ffmpeg.filter(stream, "crop", 405, 720, 0, 0)
    stream = ffmpeg.output(stream, "./videos/video" + str(video_count) + "_formated.mp4")
    ffmpeg.run(stream)



    #resize video without stretching
    # clip = mp.VideoFileClip("./videos/video" + str(video_count) + ".mp4")
    # clip = clip.resize(height=1920)
    # #change ratio to 9:16
    # clip = clip.crop(x1=0, y1=0, x2=1080, y2=1920)
    # clip.write_videofile("./videos/video" + str(video_count) + ".mp4")