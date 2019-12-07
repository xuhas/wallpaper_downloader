"""
1. Gets  wallpaper of the week from https://theultralinx.com/2019/11/wallpaper-of-the-week-xxx/
2. Parses html to get the download link
3. Downloads the file
4. Sets MacOs wallpaper to the downloader file
"""
from urllib import request
from bs4 import BeautifulSoup
from appscript import app, mactypes

BASE_URL = "https://theultralinx.com/2019/11/wallpaper-of-the-week-"
DOWNLOAD_FOLDER = "./downloaded_wallpapers"
CURRENT_INDEX_FILE = "./data/currentIndex.txt"

def get_current_index():
    f = open(f"{CURRENT_INDEX_FILE}")
    index = f.read()
    f.close()
    return index

def get_page_HTML(current_wallpaper_index: str):
    return request.urlopen(f"{BASE_URL}{current_wallpaper_index}/").read()

def get_download_link(html) -> str:
    parsed_html = BeautifulSoup(html, features="html.parser")
    download_tag = parsed_html.body.find_all('a', target='_blank', text="Download")
    return (download_tag[0]['href'])

def download_image(download_link: str):
    return request.urlopen(download_link).read()

def save_image(image, where_to:str) -> None:
    f = open(where_to,'wb')
    f.write(image)
    f.close()

def update_MacOs_wallpaper(wallpaper_file: str) -> None:
    app('Finder').desktop_picture.set(mactypes.File(f'{DOWNLOAD_FOLDER}/{new_file_name}.jpg'))
    return

def update_current_index(current_index: str) -> None:
    current_index = str(int(current_index) + 1)
    f = open(CURRENT_INDEX_FILE, 'w')
    f.write(current_index)
    f.close



try:
    current_wallpaper_index = get_current_index()
    contents = get_page_HTML(current_wallpaper_index)
    download_link = get_download_link(contents)
    new_file_name = f"wallpaper_{current_wallpaper_index}"
    image = download_image(download_link)
    save_image(image, where_to=f'{DOWNLOAD_FOLDER}/{new_file_name}.jpg')
    update_MacOs_wallpaper(f'{DOWNLOAD_FOLDER}/{new_file_name}.jpg')
    update_current_index(current_wallpaper_index)

except Exception as e:
    print("Error")
    print(e)
    exit(1)
