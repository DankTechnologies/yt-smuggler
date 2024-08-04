# yt-smuggler

**yt-smuggler** monitors a public YouTube playlist and downloads newly-added videos to a specified download folder

* Uses `Channel Name/Video Title.mp4` naming convention
* Creates NFO file with video details, for nice presentation in Jellyfin/Plex
* Uses simple text file for tracking downloads

## Motivations

I like using the YouTube ReVanced app on my phone as a front-end, for subscribing to channels, checking for new videos, and seeing what the algorithm serves up.  However, I'd rather watch the videos through my server's Jellyfin/Plex, like I do with everything else.

After not finding anything addressing this need, I scratched the itch and created this glue-y cron job.  Let me know if you find it helpful.

## Tech Stack

* Python 3.10
* [google-api-python-client](https://pypi.org/project/google-api-python-client/) for interacting with YouTube API
* [yt-dlp](https://pypi.org/project/yt-dlp/) for downloading YouTube videos

## YouTube API Key

This is needed for the playlist and video details queries.  [Steps to obtain here](https://stevesie.com/docs/pages/youtube-api-token) and elsewhere on the web

## Docker Build and Run

```bash
docker build -t yt-smuggler .

docker run --rm -it -e API_KEY='xxxx' -e PLAYLIST_ID='yyyy' -e DOWNLOAD_DIR='/download' -v $PWD:/download yt-smuggler
```
