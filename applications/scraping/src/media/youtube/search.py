import sys
import os
import yt_dlp as youtube_dl  # Using yt-dlp for downloading videos
from googleapiclient.discovery import build
from datetime import datetime, timezone
from operator import itemgetter
from tqdm import tqdm  # Optional: for progress bar

def initialize_youtube(api_key):
    """
    Initializes the YouTube Data API client.
    
    Args:
        api_key (str): Your YouTube Data API key.
    
    Returns:
        Resource: YouTube API client.
    """
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube
    except Exception as e:
        print(f"An error occurred while initializing YouTube API: {e}")
        sys.exit(1)

def search_videos(youtube, query, max_results=50):
    """
    Searches for videos matching the query.
    
    Args:
        youtube (Resource): YouTube API client.
        query (str): Search keywords.
        max_results (int): Maximum number of results to fetch.
    
    Returns:
        list: A list of video IDs.
    """
    video_ids = []
    try:
        request = youtube.search().list(
            part='id',
            q=query,
            type='video',
            maxResults=50,  # Maximum allowed per request
            order='relevance'
        )
        while request and len(video_ids) < max_results:
            response = request.execute()
            for item in response.get('items', []):
                video_ids.append(item['id']['videoId'])
                if len(video_ids) >= max_results:
                    break
            request = youtube.search().list_next(request, response)
    except Exception as e:
        print(f"An error occurred during the search: {e}")
        sys.exit(1)
    
    print(f"Total videos found: {len(video_ids)}")
    return video_ids

def get_videos_statistics(youtube, video_ids):
    """
    Retrieves statistics and snippet for a list of video IDs.
    
    Args:
        youtube (Resource): YouTube API client.
        video_ids (list): A list of video IDs.
    
    Returns:
        list: A list of dictionaries containing video details.
    """
    videos = []
    for i in range(0, len(video_ids), 50):
        batch_ids = video_ids[i:i+50]
        try:
            request = youtube.videos().list(
                part='statistics,snippet',
                id=','.join(batch_ids),
                maxResults=50
            )
            response = request.execute()
            for item in response.get('items', []):
                video_id = item['id']
                title = item['snippet']['title']
                published_at = item['snippet']['publishedAt']
                view_count = int(item['statistics'].get('viewCount', 0))
                videos.append({
                    'video_id': video_id,
                    'title': title,
                    'publishedAt': published_at,
                    'views': view_count
                })
        except Exception as e:
            print(f"An error occurred while fetching video statistics: {e}")
    
    print(f"Total videos with statistics: {len(videos)}")
    return videos

def get_top_recent_videos(videos, top_n=10):
    """
    Retrieves the top N most recent videos.
    
    Args:
        videos (list): List of video dictionaries.
        top_n (int): Number of top videos to retrieve.
    
    Returns:
        list: Top N most recent videos.
    """
    sorted_videos = sorted(videos, key=lambda x: x['publishedAt'], reverse=True)
    return sorted_videos[:top_n]

def get_top_viewed_videos(videos, top_n=10):
    """
    Retrieves the top N most viewed videos.
    
    Args:
        videos (list): List of video dictionaries.
        top_n (int): Number of top videos to retrieve.
    
    Returns:
        list: Top N most viewed videos.
    """
    sorted_videos = sorted(videos, key=lambda x: x['views'], reverse=True)
    return sorted_videos[:top_n]

def display_videos(videos, category):
    """
    Displays a list of videos.
    
    Args:
        videos (list): List of video dictionaries.
        category (str): Category name (e.g., "Most Recent", "Most Viewed").
    """
    if not videos:
        print(f"No videos found for the category: {category}.")
        return

    print(f"\n=== Top {len(videos)} {category} Videos ===\n")
    for idx, video in enumerate(videos, 1):
        title = video['title']
        url = f"https://www.youtube.com/watch?v={video['video_id']}"
        views = f"{video['views']:,}"
        published_at = video['publishedAt']
        print(f"{idx}. {title}\n   URL: {url}\n   Views: {views}\n   Published At: {published_at}\n")

def prompt_download(videos, category):
    """
    Prompts the user to download selected videos.
    
    Args:
        videos (list): List of video dictionaries.
        category (str): Category name for display purposes.
    """
    if not videos:
        return

    download_option = input(f"\nWould you like to download any of the {category} videos? (yes/no): ").strip().lower()

    if download_option not in ['yes', 'y']:
        print("No videos selected for download.")
        return

    while True:
        video_numbers = input(f"Enter the numbers of the {category} videos you want to download (comma-separated, e.g., 1,3,5): ")
        video_list = []
        try:
            video_list = [int(num.strip()) for num in video_numbers.split(',') if num.strip().isdigit()]
            if not video_list:
                raise ValueError
            if any(num < 1 or num > len(videos) for num in video_list):
                raise ValueError
            break
        except ValueError:
            print("Invalid input. Please enter valid video numbers separated by commas.")

    print("\nVideos selected for download:")
    for num in video_list:
        video = videos[num-1]
        title = video['title']
        print(f"{num}. {title}")

    # Ask for download directory
    download_dir = input("\nEnter the directory where you want to save the videos (leave blank for current directory): ").strip()
    if not download_dir:
        download_dir = '.'
    else:
        # Create the directory if it doesn't exist
        try:
            os.makedirs(download_dir, exist_ok=True)
        except Exception as e:
            print(f"Failed to create directory '{download_dir}': {e}")
            sys.exit(1)

    # Download the selected videos using yt-dlp
    for num in video_list:
        video = videos[num-1]
        video_id = video['video_id']
        title = video['title']
        url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"\nDownloading '{title}'...")
        try:
            ydl_opts = {
                'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',  # Prefer MP4 formats
                'merge_output_format': 'mp4',  # Ensure the final file is MP4
                'noplaylist': True,
                'quiet': False,
                'no_warnings': True,
                'writesubtitles': False,
                'writeautomaticsub': False,
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',  # Convert to mp4 if necessary
                }],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print(f"Downloaded '{title}' successfully.")
        except Exception as e:
            print(f"An error occurred while downloading '{title}': {e}")

def main():
    """
    The main function to execute the program.
    """
    print("=== YouTube Video Search and Downloader ===\n")

    # YouTube Data API Initialization
    api_key = 'AIzaSyAtczAs0ufhbKTlPmmq5VY62H1-hE7AC4M'  # Replace with your actual YouTube Data API key

    if api_key == 'YOUR_YOUTUBE_API_KEY':
        print("Please replace 'YOUR_YOUTUBE_API_KEY' with your actual YouTube Data API key in the script.")
        sys.exit(1)

    youtube = initialize_youtube(api_key)

    # Prompt user for search keywords
    query = input("Enter search keywords: ").strip()
    if not query:
        print("No search keywords entered. Exiting.")
        sys.exit(0)

    # Step 1: Search for videos matching the keywords
    video_ids = search_videos(youtube, query, max_results=100)  # Fetch up to 100 videos

    if not video_ids:
        print("No videos found for the given search keywords.")
        sys.exit(0)

    # Step 2: Get video statistics
    videos = get_videos_statistics(youtube, video_ids)

    if not videos:
        print("No video statistics found.")
        sys.exit(0)

    # Step 3: Get top 10 most recent videos
    most_recent = get_top_recent_videos(videos, top_n=10)

    # Step 4: Get top 10 most viewed videos
    top_viewed = get_top_viewed_videos(videos, top_n=10)

    # Step 5: Display most recent videos
    display_videos(most_recent, category="Most Recent")

    # Step 6: Prompt download for most recent videos
    prompt_download(most_recent, category="Most Recent")

    # Step 7: Display top viewed videos
    display_videos(top_viewed, category="Most Viewed")

    # Step 8: Prompt download for top viewed videos
    prompt_download(top_viewed, category="Most Viewed")

    print("\n=== Program Completed ===")

if __name__ == "__main__":
    main()
