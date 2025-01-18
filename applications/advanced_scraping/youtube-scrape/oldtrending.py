from googleapiclient.discovery import build
from datetime import datetime, timezone

def get_old_trending_videos(category=None):
    api_key = 'YOUR_API_KEY'  # Replace with your actual API key
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Prepare the request parameters
    params = {
        'part': 'snippet',
        'type': 'video',
        'order': 'viewCount',
        'regionCode': 'US',
        'maxResults': 50  # Fetch more results to filter later
    }

    if category == 'sports':
        params['videoCategoryId'] = '17'  # Category ID for Sports
    elif category == 'comedy':
        params['videoCategoryId'] = '23'  # Category ID for Comedy
    elif category == 'politics':
        params['q'] = 'Politics'

    # Fetch the videos using the search method
    request = youtube.search().list(**params)
    response = request.execute()

    videos = []
    for item in response.get('items', []):
        # Parse the publish date
        publish_date = datetime.strptime(item['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        
        # Filter out live streams and ensure the video was published before 2017
        if item['snippet'].get('liveBroadcastContent', 'none') == 'none' and publish_date.year < 2017:
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

    print(f"\nTop 10 Most Popular {category_name} Videos in the United States (Posted Before 2017):\n")
    for i, video in enumerate(videos, 1):
        print(f"{i}. {video['title']} - {video['url']}")

def main():
    print("Fetching the top 10 most popular videos in the United States posted before 2017...")
    general_videos = get_old_trending_videos()
    display_videos(general_videos, "General")

    print("\nFetching the top 10 most popular Sports videos in the United States posted before 2017...")
    sports_videos = get_old_trending_videos(category='sports')
    display_videos(sports_videos, "Sports")

    print("\nFetching the top 10 most popular Comedy videos in the United States posted before 2017...")
    comedy_videos = get_old_trending_videos(category='comedy')
    display_videos(comedy_videos, "Comedy")

    print("\nFetching the top 10 most popular Politics-related videos in the United States posted before 2017...")
    politics_videos = get_old_trending_videos(category='politics')
    display_videos(politics_videos, "Politics")

if __name__ == "__main__":
    main()
