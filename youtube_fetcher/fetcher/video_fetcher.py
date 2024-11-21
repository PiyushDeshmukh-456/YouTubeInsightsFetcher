from googleapiclient.discovery import build  # Import the YouTube API client

def get_channel_videos(api_key, channel_url):
    """
    Fetches all videos from a YouTube channel given its URL, along with metadata.

    Args:
        api_key (str): Your YouTube Data API key.
        channel_url (str): The URL of the YouTube channel.

    Returns:
        list[dict]: A list of video metadata (title, ID, view count, etc.).
    """
    youtube = build('youtube', 'v3', developerKey=api_key)  # Initialize the YouTube API client

    # Extract the channel handle from the URL
    if "/@" in channel_url:
        channel_handle = channel_url.split("/@")[1]
    else:
        raise ValueError("Invalid YouTube channel URL")

    # Use the search endpoint to get the channel ID
    search_response = youtube.search().list(
        part='snippet',
        q=f"@{channel_handle}",
        type='channel'
    ).execute()

    # Extract the channel ID from the search response
    channel_id = search_response['items'][0]['id']['channelId']

    # Prepare to fetch videos
    video_data = []
    next_page_token = None

    # Loop through all pages of results
    while True:
        response = youtube.search().list(
            part='snippet',
            channelId=channel_id,
            maxResults=50,
            pageToken=next_page_token,
            type='video'
        ).execute()

        # Extract basic video data from each item in the response
        for item in response['items']:
            video_id = item['id']['videoId']
            video_details = youtube.videos().list(
                part='snippet,statistics,contentDetails',
                id=video_id
            ).execute()

            if video_details['items']:
                details = video_details['items'][0]
                video_data.append({
                    'video_id': video_id,
                    'title': details['snippet']['title'],
                    'description': details['snippet']['description'],
                    'published_date': details['snippet']['publishedAt'],
                    'view_count': details['statistics'].get('viewCount', 0),
                    'like_count': details['statistics'].get('likeCount', 0),
                    'comment_count': details['statistics'].get('commentCount', 0),
                    'duration': details['contentDetails']['duration'],
                    'thumbnail_url': details['snippet']['thumbnails']['high']['url']
                })

      
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return video_data 
