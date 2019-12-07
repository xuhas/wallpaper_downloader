# wallpaper_downloader


Small project that gets the new wallpaper from [this site](https://theultralinx.com/)

1. Gets  wallpaper of the week from https://theultralinx.com/2019/11/wallpaper-of-the-week-xxx/
2. Parses html to get the download link
3. Downloads the file
4. Sets MacOs wallpaper to the downloader file

Last step would be to create a `crontab` job and set it to whatever frequency. 

eg: Weekly
```
0 0 0 * * MON
```