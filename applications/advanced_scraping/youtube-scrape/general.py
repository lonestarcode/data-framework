import sys
from googleapiclient.discovery import build
from datetime import datetime, timedelta, timezone
import yt_dlp as youtube_dl  # Use yt-dlp
import os

def get_most_popular_videos(category=None, timeframe='day'):
    api_key = 'AIzaSyAtczAs0ufhbKTlPmmq5VY62H1-hE7AC4M'  # Replace with your actual API key
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Calculate the cutoff date based on the timeframe
    now = datetime.now(timezone.utc)
    if timeframe == 'day':
        cutoff_date = now - timedelta(days=1)
    elif timeframe == 'week':
        cutoff_date = now - timedelta(weeks=1)
    elif timeframe == 'year':
        cutoff_date = now - timedelta(days=365)
    else:
        raise ValueError("Invalid timeframe. Choose 'day', 'week', or 'year'.")

    # Format the cutoff_date properly for the API
    published_after = cutoff_date.strftime('%Y-%m-%dT%H:%M:%SZ')

    # Prepare the request parameters
    params = {
        'part': 'snippet',
        'type': 'video',
        'order': 'viewCount',
        'regionCode': 'US',
        'publishedAfter': published_after,
        'maxResults': 50  # Fetch more results to filter later
    }

    if category == 'gaming':
        params['videoCategoryId'] = '20'  # Category ID for Gaming
    elif category == 'nfl':
        params['q'] = 'NFL'

    # Fetch the videos using the search method
    request = youtube.search().list(**params)
    response = request.execute()

    videos = []
    for item in response.get('items', []):
        # Parse the publish date
        publish_date = datetime.strptime(item['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        
        # Filter out live streams
        if item['snippet'].get('liveBroadcastContent', 'none') == 'none':
            video = {
                'title': item['snippet']['title'],
                'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            }
            videos.append(video)

        if len(videos) == 10:  # Stop after getting 10 videos
            break

    return videos

def display_videos(videos, category_name):
    if not videos:
        print(f"No videos found for {category_name}.")
        return

    print(f"\nTop 10 Most Popular {category_name} Videos in the United States:\n")
    for i, video in enumerate(videos, 1):
        print(f"{i}. {video['title']} - {video['url']}")

def download_videos(videos):
    download_option = input("\nWould you like to download any of these videos? (yes/no): ").lower()

    if download_option == 'yes':
        while True:
            video_numbers = input("Enter the numbers of the videos you want to download (comma-separated, e.g., 1,3,5): ")
            video_list = [int(num.strip()) for num in video_numbers.split(',') if num.strip().isdigit()]

            if all(1 <= num <= len(videos) for num in video_list):
                break
            else:
                print("Invalid input. Please enter valid video numbers.")

        print("\nVideos selected for download:")
        for num in video_list:
            print(f"{num}. {videos[num-1]['title']}")

        # Ask for download directory
        download_dir = input("\nEnter the directory where you want to save the videos (leave blank for current directory): ").strip()
        if not download_dir:
            download_dir = '.'
        else:
            # Create the directory if it doesn't exist
            os.makedirs(download_dir, exist_ok=True)

        # Download the selected videos using yt-dlp
        for num in video_list:
            video = videos[num-1]
            url = video['url']
            title = video['title']
            print(f"\nDownloading '{title}'...")
            try:
                ydl_opts = {
                    'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
                    'format': 'bestvideo+bestaudio/best',  # Download best available quality
                    'noplaylist': True,
                    'quiet': False,
                    'no_warnings': True,
                    'writesubtitles': False,
                    'writeautomaticsub': False,
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                print(f"Downloaded '{title}' successfully.")
            except Exception as e:
                print(f"An error occurred while downloading '{title}': {e}")
    else:
        print("No videos selected for download.")

def main():
    timeframe = input("Enter the timeframe for most popular videos (day/week/year): ").lower()
    while timeframe not in ['day', 'week', 'year']:
        print("Invalid timeframe. Please choose 'day', 'week', or 'year'.")
        timeframe = input("Enter the timeframe for most popular videos (day/week/year): ").lower()

    print(f"Fetching the top 10 most popular videos in the United States for the past {timeframe}...")
    general_videos = get_most_popular_videos(timeframe=timeframe)
    display_videos(general_videos, "General")
    download_videos(general_videos)

    print(f"\nFetching the top 10 most popular Gaming videos in the United States for the past {timeframe}...")
    gaming_videos = get_most_popular_videos(category='gaming', timeframe=timeframe)
    display_videos(gaming_videos, "Gaming")
    download_videos(gaming_videos)

    print(f"\nFetching the top 10 most popular NFL-related videos in the United States for the past {timeframe}...")
    nfl_videos = get_most_popular_videos(category='nfl', timeframe=timeframe)
    display_videos(nfl_videos, "NFL")
    download_videos(nfl_videos)

if __name__ == "__main__":
    main()