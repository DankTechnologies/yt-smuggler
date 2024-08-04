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

## Example Output

Written to STDOUT, i.e. [the right way](https://12factor.net/logs)

```bash
2024-08-04 05:50:42,222 - INFO - Starting yt-smuggler...
2024-08-04 05:50:42,223 - INFO - file_cache is only supported with oauth2client<4.0.0
2024-08-04 05:50:42,448 - INFO - Downloading Charlie Anderson - This will change the way you make pizza sauce...
2024-08-04 05:50:57,978 - INFO - Downloaded Charlie Anderson - This will change the way you make pizza sauce
2024-08-04 05:50:58,049 - INFO - Downloading NOT ANOTHER COOKING SHOW - Why I Love My Pasta, Prosciutto and Peas...
2024-08-04 05:51:08,236 - INFO - Downloaded NOT ANOTHER COOKING SHOW - Why I Love My Pasta, Prosciutto and Peas
2024-08-04 05:51:08,303 - INFO - Downloading Sip and Feast - The Easy Italian Potato Salad To Make All Summer Long....
2024-08-04 05:51:21,426 - INFO - Downloaded Sip and Feast - The Easy Italian Potato Salad To Make All Summer Long.
2024-08-04 05:51:21,472 - INFO - Downloading Derek Sarno - Flavor Mastering Tofu 101...
2024-08-04 05:51:35,858 - INFO - Downloaded Derek Sarno - Flavor Mastering Tofu 101
2024-08-04 05:51:35,945 - INFO - Downloading Smart Home Solver - The Smart Home Sensors I NEVER knew I needed!...
2024-08-04 05:51:48,819 - INFO - Downloaded Smart Home Solver - The Smart Home Sensors I NEVER knew I needed!
2024-08-04 05:51:48,820 - INFO - Sleeping for 30 minutes
```