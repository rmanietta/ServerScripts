#YT-DLP Tips

## Download full playlist as mp4 upto 1080p

```
yt-dlp -f "bestvideo[height<=1080]+bestaudio/best" --merge-output-format mp4 -o "%(playlist_index)s - %(title)s.%(ext)s" "PLAYLIST_URL"
```


## Cookies from browser

```
yt-dlp --cookies-from-browser {firefox|chromium} "URL"
```

