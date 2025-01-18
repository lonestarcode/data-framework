import os
import time
import schedule
import tweepy
import logging
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv
from database_utils import get_video_for_platform, update_video_status, print_db_stats
from flask import Flask, request, jsonify
from your_ml_module import recommend_videos  # Import your ML logic

load_dotenv()

CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
twitter_api = tweepy.API(auth)

YOUTUBE_CLIENT_SECRETS_FILE = os.getenv('YOUTUBE_CLIENT_SECRETS_FILE')
YOUTUBE_CREDENTIALS_FILE = os.getenv('YOUTUBE_CREDENTIALS_FILE')
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

VIDEO_DIR = os.getenv('VIDEO_DIR', 'Videos_to_Upload')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

ALBUMS_DIR = 'albums'  # Directory to store albums

@app.route('/api/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    video = request.files['video']
    video.save(os.path.join('path_to_save_directory', video.filename))
    return jsonify({'message': 'Video uploaded successfully'}), 200

@app.route('/api/post-selected', methods=['POST'])
def post_selected():
    data = request.json
    platforms = data.get('platforms', [])
    captions = data.get('captions', {})

    # Logic to post to selected platforms with captions
    for platform in platforms:
        caption = captions.get(platform, '')
        # Call the respective API wrapper to post
        # Example: post_to_twitter(caption) if platform == 'twitter'

    return jsonify({'message': 'Posted to selected platforms successfully'}), 200

@app.route('/api/schedule', methods=['POST'])
def schedule_posts():
    schedule_data = request.json
    # Logic to schedule posts using the schedule library
    # Example: schedule.every().day.at(schedule_data['tweet_time']).do(tweet_video)

    return jsonify({'message': 'Schedule updated successfully'}), 200

def tweet_video():
    filename = get_video_for_platform('tweeted', 180)
    if filename:
        video_path = os.path.join(VIDEO_DIR, filename)
        try:
            twitter_api.update_with_media(video_path, status="Check out this video!")
            update_video_status(filename, 'tweeted')
            logging.info(f'Tweeted: {filename}')
        except tweepy.TweepError as e:
            logging.error(f'Tweepy error: {e}')


def upload_to_youtube_shorts():
    filename = get_video_for_platform('youtubed', 180)
    if filename:
        video_path = os.path.join(VIDEO_DIR, filename)
        try:
            credentials = Credentials.from_authorized_user_file(YOUTUBE_CREDENTIALS_FILE, SCOPES)
            youtube = build('youtube', 'v3', credentials=credentials)

            body = {
                'snippet': {
                    'title': 'Check out this YouTube Short!',
                    'description': 'Uploaded via automated script',
                    'tags': ['shorts', 'video'],
                    'categoryId': '22'
                },
                'status': {
                    'privacyStatus': 'public'
                }
            }
            media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
            request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
            response = request.execute()

            update_video_status(filename, 'youtubed')
            logging.info(f'Uploaded to YouTube Shorts: {filename}')
        except Exception as e:
            logging.error(f'YouTube upload error: {e}')


def upload_to_instagram_reels():
    filename = get_video_for_platform('instagrammed', 180)
    if filename:
        logging.info(f'Would upload to Instagram Reels: {filename}')
        update_video_status(filename, 'instagrammed')


def upload_to_tiktok():
    filename = get_video_for_platform('tiktoked', 180)
    if filename:
        logging.info(f'Would upload to TikTok: {filename}')
        update_video_status(filename, 'tiktoked')


@app.route('/api/create-album', methods=['POST'])
def create_album():
    data = request.json
    album_name = data.get('album_name')

    if not album_name:
        return jsonify({'error': 'Album name is required'}), 400

    album_path = os.path.join(ALBUMS_DIR, album_name)

    if not os.path.exists(ALBUMS_DIR):
        os.makedirs(ALBUMS_DIR)

    if os.path.exists(album_path):
        return jsonify({'error': 'Album already exists'}), 400

    os.makedirs(album_path)
    return jsonify({'message': 'Album created successfully', 'albums': os.listdir(ALBUMS_DIR)}), 200

@app.route('/api/recommend-videos', methods=['POST'])
def recommend_videos_endpoint():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    video = request.files['video']
    category = request.form.get('category', None)

    # Call your ML model to get recommendations
    recommendations = recommend_videos(video, category)

    return jsonify({'recommendations': recommendations}), 200

@app.route('/api/train-ai', methods=['POST'])
def train_ai():
    data = request.json
    category = data.get('category')

    if not category:
        return jsonify({'error': 'Category is required for AI training'}), 400

    # Logic to train AI based on the selected category
    recommendations = recommend_videos_based_on_category(category)

    return jsonify({'recommendations': recommendations}), 200

def recommend_videos_based_on_category(category):
    # Placeholder logic for recommending videos based on category
    # This should be replaced with your actual ML model logic
    # Example: Filter videos in the database by category and return recommendations
    return [
        {'title': 'Example Video 1', 'category': category},
        {'title': 'Example Video 2', 'category': category}
    ]

@app.route('/api/get-recommendations', methods=['POST'])
def get_recommendations():
    data = request.json
    category = data.get('category')

    if not category:
        return jsonify({'error': 'Category is required for recommendations'}), 400

    # Logic to get recommendations based on the selected category
    recommendations = recommend_videos_based_on_category(category)

    return jsonify({'recommendations': recommendations}), 200

@app.route('/api/categorize-video', methods=['POST'])
def categorize_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    video = request.files['video']

    # Call your ML model to predict the category
    category = predict_video_category(video)

    return jsonify({'category': category}), 200

def predict_video_category(video):
    # Placeholder logic for predicting video category
    # This should be replaced with your actual ML model logic
    # Example: Use a pre-trained model to predict the category
    return 'sports'  # Example category

def main():
    schedule.every().day.at("10:00").do(tweet_video)
    schedule.every().day.at("14:00").do(upload_to_youtube_shorts)
    schedule.every().day.at("18:00").do(upload_to_instagram_reels)
    schedule.every().day.at("22:00").do(upload_to_tiktok)
    schedule.every().hour.do(print_db_stats)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    app.run(debug=True)
