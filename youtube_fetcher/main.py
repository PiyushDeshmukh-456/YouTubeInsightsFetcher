import os
import pandas as pd
from fetcher.video_fetcher import get_channel_videos
from fetcher.comments_fetcher import get_video_comments
from googleapiclient.discovery import build  # Import the YouTube API client

def save_data_to_excel(video_data, comments_data, output_file):
    """
    Saves the video data and comments data to an Excel file.

    Args:
        video_data (list[dict]): List of video metadata.
        comments_data (list[dict]): List of comment data.
        output_file (str): The name of the output Excel file.
    """
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        # Convert video data to DataFrame and write to Excel
        video_df = pd.DataFrame(video_data)
        video_df.to_excel(writer, sheet_name='Video Data', index=False)

        # Convert comments data to DataFrame and write to Excel
        comments_df = pd.DataFrame(comments_data)
        comments_df.to_excel(writer, sheet_name='Comments Data', index=False)

def get_channel_name(api_key, channel_url):
    """
    Fetches the name of the YouTube channel given its URL.

    Args:
        api_key (str): Your YouTube Data API key.
        channel_url (str): The URL of the YouTube channel.

    Returns:
        str: The name of the YouTube channel.
    """
    youtube = build('youtube', 'v3', developerKey=api_key, cache_discovery=False)

    # Extract the channel handle from the URL
    if "/@" in channel_url:
        channel_handle = channel_url.split("/@")[1]
    else:
        raise ValueError("Invalid YouTube channel URL. Ensure it contains a handle (e.g., /@channelhandle).")

    # Use the search endpoint to get the channel ID
    search_response = youtube.search().list(
        part='snippet',
        q=f"@{channel_handle}",
        type='channel'
    ).execute()

    # Extract the channel name from the search response
    channel_name = search_response['items'][0]['snippet']['channelTitle']
    return channel_name

def main():
    api_key = input("Enter your YouTube Data API key: ")
    channel_url = input("Enter the YouTube channel URL: ")

    # Fetch the channel name
    print("Fetching channel name...")
    channel_name = get_channel_name(api_key, channel_url)
    print(f"Channel Name: {channel_name}")

    # Fetch video data
    print("Fetching video data...")
    video_data = get_channel_videos(api_key, channel_url)

    if not video_data:
        print("No video data found.")
        return

    print(f"Found {len(video_data)} videos. Fetching comments...")

    # Fetch comments for each video
    comments_data = []
    for video in video_data:
        video_id = video['video_id']
        comments = get_video_comments(api_key, video_id)
        comments_data.extend(comments)

    # Create a safe filename using the channel name
    safe_channel_name = "".join(c for c in channel_name if c.isalnum() or c in (' ', '_', '-')).rstrip()
    output_file = f"{safe_channel_name}_YouTube_Channel_Data.xlsx"

    # Save data to Excel
    save_data_to_excel(video_data, comments_data, output_file)
    print(f"Data saved to {output_file}")

if __name__ == "__main__":
    main()
