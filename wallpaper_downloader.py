
#!/usr/bin/python3

"""
1. Gets  wallpaper of the week from https://theultralinx.com/2019/11/wallpaper-of-the-week-xxx/
2. Parses html to get the download link
3. Downloads the file
4. Sets MacOs wallpaper to the downloader file
"""
try:
    from urllib import request
    from bs4 import BeautifulSoup
    import datetime
    from appscript import app, mactypes
    from appscript import *
    import argparse
    import sys
    import os

    BASE_URL = "https://theultralinx.com/2019/11/wallpaper-of-the-week-"
    DOWNLOAD_FOLDER = "/Users/xh/Workspace/personnalProjects/wallpaper_downloader/downloaded_wallpapers"
    CURRENT_INDEX_FILE = "/Users/xh/Workspace/personnalProjects/wallpaper_downloader/data/currentIndex.txt"

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
        # app('Finder').desktop_picture.set(mactypes.File(f'{DOWNLOAD_FOLDER}/{new_file_name}.jpg'))

        # parser = argparse.ArgumentParser(description='Set desktop wallpaper.')
        # parser.add_argument('file', type=wallpaper_file, help='File to use as wallpaper.')
        # args = parser.parse_args()
        # f = args.file
        se = app('System Events')
        desktops = se.desktops.display_name.get()
        for d in desktops:
            desk = se.desktops[its.display_name == d]
            desk.picture.set(mactypes.File(wallpaper_file))

        return

    def update_current_index(current_index: str) -> None:
        current_index = str(int(current_index) + 1)
        f = open(CURRENT_INDEX_FILE, 'w')
        f.write(current_index)
        f.close

    current_wallpaper_index = get_current_index()
    contents = get_page_HTML(current_wallpaper_index)
    download_link = get_download_link(contents)
    new_file_name = f"wallpaper_{current_wallpaper_index}"
    image = download_image(download_link)
    save_image(image, where_to=f'{DOWNLOAD_FOLDER}/{new_file_name}.jpg')
    update_MacOs_wallpaper(f'{DOWNLOAD_FOLDER}/{new_file_name}.jpg')
    update_current_index(current_wallpaper_index)
    print(f"{datetime.datetime.now()}: Success")
except Exception as e:
    print(f"{datetime.datetime.now()}: Error")
    print(e)
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)
    exit(1)
