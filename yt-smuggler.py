import os
import time
import googleapiclient.discovery
from googleapiclient.errors import HttpError
import yt_dlp
import logging

API_KEY = os.getenv('API_KEY')
PLAYLIST_ID = os.getenv('PLAYLIST_ID')
DOWNLOAD_DIR = os.getenv('DOWNLOAD_DIR')
INTERVAL_MIN = int(os.getenv('INTERVAL_MIN', '30'))
HISTORY_FILE = os.path.join(DOWNLOAD_DIR, 'downloaded_videos.txt')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_playlist_videos(service, playlist_id):
    try:
        request = service.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50
        )
        response = request.execute()

        videos = []
        for item in response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            videos.append(video_url)

        return videos
    except HttpError as e:
        logging.error(f"An HTTP error occurred: {e}")
        return []

def get_video_details(service, video_id):
    try:
        request = service.videos().list(
            part="snippet",
            id=video_id
        )
        response = request.execute()

        if response['items']:
            video_snippet = response['items'][0]['snippet']
            channel_name = video_snippet['channelTitle']
            video_title = video_snippet['title']
            video_description = video_snippet.get('description', '')
            video_date = video_snippet.get('publishedAt', '').split('T')[0]
            return channel_name, video_title, video_description, video_date
        else:
            return None, None, None, None
    except HttpError as e:
        logging.error(f"An HTTP error occurred while fetching video details: {e}")
        return None, None, None, None

def read_downloaded_videos(file_path):
    if not os.path.exists(file_path):
        return set()
    with open(file_path, 'r') as f:
        return set(line.strip() for line in f)

def write_downloaded_videos(file_path, videos):
    with open(file_path, 'a') as f:
        for video in videos:
            f.write(f"{video}\n")

def write_nfo_file(output_path, channel_name, video_title, video_description, video_date):
    nfo_content = f"""
<episodedetails>
  <title>{video_title}</title>
  <showtitle>{channel_name}</showtitle>
  <plot>{video_description}</plot>
  <aired>{video_date}</aired>
</episodedetails>
"""
    with open(output_path, 'w') as f:
        f.write(nfo_content)

def download_videos(service, video_urls):
    successfully_downloaded = []

    for video_url in video_urls:
        video_id = video_url.split("v=")[-1]
        channel_name, video_title, video_description, video_date = get_video_details(service, video_id)

        if channel_name and video_title:
            channel_name_sanitized = ''.join(c if c.isalnum() or c in ' _-' else '_' for c in channel_name).strip(' _-')
            video_title_sanitized = ''.join(c if c.isalnum() or c in ' _-' else '_' for c in video_title).strip(' _-')
            output_template = os.path.join(DOWNLOAD_DIR, f"{channel_name_sanitized}/{video_title_sanitized}.%(ext)s")
            nfo_template = os.path.join(DOWNLOAD_DIR, f"{channel_name_sanitized}/{video_title_sanitized}.nfo") 
        else:
            output_template = os.path.join(DOWNLOAD_DIR, f"{video_id}.%(ext)s")
            nfo_template = os.path.join(DOWNLOAD_DIR, f"{video_id}.nfo")

        ydl_opts = {
            'outtmpl': output_template,
            'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoRemuxer',
                'preferedformat': 'mp4',
            }],
        }

        try:
            logging.info(f"Downloading {channel_name} - {video_title}...")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])

            write_nfo_file(nfo_template, channel_name, video_title, video_description, video_date)

            logging.info(f"Downloaded {channel_name} - {video_title}")

            successfully_downloaded.append(video_url)
        except Exception as e:
            logging.error(e)

    return successfully_downloaded

if __name__ == "__main__":
    logging.info("Starting yt-smuggler...")

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    service = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)

    while True:
        video_data = get_playlist_videos(service, PLAYLIST_ID)

        if video_data:
            downloaded_videos = read_downloaded_videos(HISTORY_FILE)

            new_videos = [url for url in video_data if url not in downloaded_videos]

            if new_videos:
                successfully_downloaded = download_videos(service, new_videos)

                if successfully_downloaded:
                    write_downloaded_videos(HISTORY_FILE, successfully_downloaded)
            else:
                logging.info("No new videos to download")
        else:
            logging.info("No videos found in the playlist")

        logging.info(f"Sleeping for {INTERVAL_MIN} minutes")
        time.sleep(INTERVAL_MIN * 60)
