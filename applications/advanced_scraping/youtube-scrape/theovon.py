import sys
from googleapiclient.discovery import build
from datetime import datetime, timedelta, timezone
import yt_dlp as youtube_dl  # Using yt-dlp for downloading videos
import os

def get_jreclips_uploads_playlist_id(youtube, channel_id):
    """
    Retrieves the uploads playlist ID for the specified channel.
    
    Args:
        youtube: The YouTube Data API client.
        channel_id (str): The ID of the YouTube channel.
    
    Returns:
        str: The uploads playlist ID.
    """
    try:
        request = youtube.channels().list(
            part='contentDetails',
            id=channel_id
        )
        response = request.execute()
        items = response.get('items', [])
        if not items:
            print("No channel found with the provided ID.")
            sys.exit(1)
        uploads_playlist_id = items[0]['contentDetails']['relatedPlaylists']['uploads']
        return uploads_playlist_id
    except Exception as e:
        print(f"An error occurred while fetching uploads playlist ID: {e}")
        sys.exit(1)

def get_videos_published_in_last_month(youtube, uploads_playlist_id):
    """
    Retrieves all video IDs from the uploads playlist published in the last month.
    
    Args:
        youtube: The YouTube Data API client.
        uploads_playlist_id (str): The uploads playlist ID.
    
    Returns:
        list: A list of video IDs.
    """
    video_ids = []
    next_page_token = None
    one_month_ago = datetime.now(timezone.utc) - timedelta(days=30)
    published_after = one_month_ago.strftime('%Y-%m-%dT%H:%M:%SZ')

    print("Fetching video IDs published in the last month...")
    
    while True:
        try:
            request = youtube.playlistItems().list(
                part='contentDetails',
                playlistId=uploads_playlist_id,
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()
            items = response.get('items', [])
            for item in items:
                video_id = item['contentDetails']['videoId']
                video_ids.append(video_id)
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
        except Exception as e:
            print(f"An error occurred while fetching video IDs: {e}")
            break

    print(f"Total videos published in the last month: {len(video_ids)}")
    return video_ids

def get_videos_statistics(youtube, video_ids):
    """
    Retrieves statistics and snippet for a list of video IDs.
    
    Args:
        youtube: The YouTube Data API client.
        video_ids (list): A list of video IDs.
    
    Returns:
        dict: A dictionary mapping video IDs to their view counts and publish dates.
    """
    view_counts = {}
    print("Fetching video statistics...")
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
                views = int(item['statistics'].get('viewCount', 0))
                published_at = item['snippet']['publishedAt']
                view_counts[video_id] = {'views': views, 'publishedAt': published_at}
        except Exception as e:
            print(f"An error occurred while fetching video statistics: {e}")
    return view_counts

def get_top_viewed_videos(view_counts, top_n=10):
    """
    Retrieves the top N most viewed videos.
    
    Args:
        view_counts (dict): A dictionary mapping video IDs to their view counts.
        top_n (int): Number of top videos to retrieve.
    
    Returns:
        list: A list of dictionaries containing video IDs, view counts, and publish dates.
    """
    # Sort videos by view count in descending order
    sorted_videos = sorted(view_counts.items(), key=lambda x: x[1]['views'], reverse=True)
    top_videos = sorted_videos[:top_n]
    # Convert to list of dictionaries
    top_videos_list = [{'video_id': vid, 'views': data['views'], 'publishedAt': data['publishedAt']} for vid, data in top_videos]
    return top_videos_list

def get_most_recent_videos(view_counts, top_n=10):
    """
    Retrieves the most recent N videos.
    
    Args:
        view_counts (dict): A dictionary mapping video IDs to their publish dates.
        top_n (int): Number of recent videos to retrieve.
    
    Returns:
        list: A list of dictionaries containing video IDs, view counts, and publish dates.
    """
    # Sort videos by publish date in descending order
    sorted_videos = sorted(view_counts.items(), key=lambda x: x[1]['publishedAt'], reverse=True)
    recent_videos = sorted_videos[:top_n]
    # Convert to list of dictionaries
    recent_videos_list = [{'video_id': vid, 'views': data['views'], 'publishedAt': data['publishedAt']} for vid, data in recent_videos]
    return recent_videos_list

def get_video_details(youtube, video_ids):
    """
    Retrieves video titles based on video IDs.
    
    Args:
        youtube: The YouTube Data API client.
        video_ids (list): A list of video IDs.
    
    Returns:
        dict: A dictionary mapping video IDs to their titles.
    """
    titles = {}
    for i in range(0, len(video_ids), 50):
        batch_ids = video_ids[i:i+50]
        try:
            request = youtube.videos().list(
                part='snippet',
                id=','.join(batch_ids),
                maxResults=50
            )
            response = request.execute()
            for item in response.get('items', []):
                video_id = item['id']
                title = item['snippet']['title']
                titles[video_id] = title
        except Exception as e:
            print(f"An error occurred while fetching video titles: {e}")
    return titles

def display_videos(videos, titles, category):
    """
    Displays the list of videos with their titles, URLs, view counts, and publish dates.
    
    Args:
        videos (list): A list of dictionaries containing video IDs, view counts, and publish dates.
        titles (dict): A dictionary mapping video IDs to their titles.
        category (str): The category name (e.g., "Most Viewed", "Most Recent").
    """
    if not videos:
        print(f"No videos found for the category: {category}.")
        return

    print(f"\nTop 10 {category} TheoVonClips Videos:\n")
    for i, video in enumerate(videos, 1):
        title = titles.get(video['video_id'], "No Title")
        url = f"https://www.youtube.com/watch?v={video['video_id']}"
        views = f"{video['views']:,}"
        published_at = video['publishedAt']
        print(f"{i}. {title}\n   URL: {url}\n   Views: {views}\n   Published At: {published_at}\n")

def download_videos(videos, titles):
    """
    Prompts the user to download selected videos.
    
    Args:
        videos (list): A list of dictionaries containing video IDs and URLs.
        titles (dict): A dictionary mapping video IDs to their titles.
    """
    if not videos:
        return

    download_option = input("\nWould you like to download any of these videos? (yes/no): ").strip().lower()

    if download_option not in ['yes', 'y']:
        print("No videos selected for download.")
        return

    while True:
        video_numbers = input("Enter the numbers of the videos you want to download (comma-separated, e.g., 1,3,5): ")
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
        title = titles.get(video['video_id'], "No Title")
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
        title = titles.get(video_id, "No Title")
        url = f"https://www.youtube.com/watch?v={video_id}"
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

def main():
    """
    The main function to execute the program.
    """
    print("=== TheoVonClips YouTube Top Videos Fetcher ===\n")

    # YouTube Data API Initialization
    api_key = 'AIzaSyAtczAs0ufhbKTlPmmq5VY62H1-hE7AC4M'  # Replace with your actual YouTube Data API key
    channel_id = 'UCxxxxxxxxxxxxxxxxxx'  # Replace with TheoVonClips' Channel ID

    # **IMPORTANT:** Ensure you have replaced the `channel_id` above with the actual Channel ID of @TheoVonClips.
    # Example: channel_id = 'UCabcd1234efgh5678ijkl90'

    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
    except Exception as e:
        print(f"An error occurred while initializing YouTube API: {e}")
        sys.exit(1)

    # Step 1: Get uploads playlist ID
    uploads_playlist_id = get_jreclips_uploads_playlist_id(youtube, channel_id)

    # Step 2: Get all video IDs published in the last month
    video_ids = get_videos_published_in_last_month(youtube, uploads_playlist_id)

    if not video_ids:
        print("No videos published in the last month.")
        sys.exit(0)

    # Step 3: Get video statistics
    view_counts = get_videos_statistics(youtube, video_ids)

    if not view_counts:
        print("No video statistics found.")
        sys.exit(0)

    # Step 4: Get 10 most recent videos
    most_recent = get_most_recent_videos(view_counts, top_n=10)

    # Step 5: Get top 10 most viewed videos
    top_viewed = get_top_viewed_videos(view_counts, top_n=10)

    # Step 6: Get video titles
    most_recent_ids = [video['video_id'] for video in most_recent]
    top_viewed_ids = [video['video_id'] for video in top_viewed]
    all_ids = list(set(most_recent_ids + top_viewed_ids))
    titles = get_video_details(youtube, all_ids)

    # Step 7: Display 10 most recent videos
    display_videos(most_recent, titles, category="Most Recent TheoVonClips")

    # Step 8: Download option for Most Recent
    print("\n--- Downloading Most Recent Videos ---")
    download_videos(most_recent, titles)

    # Step 9: Display top 10 most viewed videos
    display_videos(top_viewed, titles, category="Most Viewed TheoVonClips")

    # Step 10: Download option for Most Viewed
    print("\n--- Downloading Most Viewed Videos ---")
    download_videos(top_viewed, titles)

    print("\n=== Program Completed ===")

if __name__ == "__main__":
    main()