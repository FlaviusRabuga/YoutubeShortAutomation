import requests
from bs4 import BeautifulSoup

html = requests.get("https://mixkit.co/free-stock-video/luxury/")
soup = BeautifulSoup(html.text, "html.parser")
# get all links where href starts with /free-stock-video/ and have a class
links = soup.find_all("a", {"class": "item-grid-video-player__overlay-link", "href": True})
#get the href attribute from the link
links = [link["href"] for link in links]
print(links)

# add the base url to the links
links = ["https://mixkit.co" + link for link in links]
print(links)

#get the first video
video_html = requests.get(links[0])
# get the video url
soup = BeautifulSoup(video_html.text, "html.parser")
video = soup.find("video" , {"class": "video-player__viewer", "src": True})
video = video["src"]
print(video)
