from googleapiclient.discovery import build  

def get_video_comments(api_key, video_id, max_comments=100):
    """
    Fetches the latest comments and replies for a given video.

    Args:
        api_key (str): Your YouTube Data API key.
        video_id (str): The ID of the video.
        max_comments (int): The maximum number of comments to fetch.

    Returns:
        list[dict]: A list of comment metadata (comment ID, text, author, etc.).
    """
    youtube = build('youtube', 'v3', developerKey=api_key, cache_discovery=False)

    comments_data = []
    next_page_token = None
    while len(comments_data) < max_comments:
        try:
            response = youtube.commentThreads().list(
                part='snippet,replies',
                videoId=video_id,
                textFormat='plainText',
                pageToken=next_page_token
            ).execute()

            # Extract comment data from the response
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                comment_data = {
                    'video_id': video_id,
                    'comment_id': item['id'],
                    'comment_text': comment['textDisplay'],
                    'author_name': comment['authorDisplayName'],
                    'published_date': comment['publishedAt'],
                    'like_count': comment['likeCount'],
                    'reply_to': None  # Top-level comment
                }
                comments_data.append(comment_data)

                # Fetch replies if any
                if 'replies' in item:
                    for reply in item['replies']['comments']:
                        reply_data = {
                            'video_id': video_id,
                            'comment_id': reply['id'],
                            'comment_text': reply['snippet']['textDisplay'],
                            'author_name': reply['snippet']['authorDisplayName'],
                            'published_date': reply['snippet']['publishedAt'],
                            'like_count': reply['snippet']['likeCount'],
                            'reply_to': item['id']  
                        }
                        comments_data.append(reply_data)

            # Check for additional pages of comments
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break  

        except Exception as e:
            print(f"Error fetching comments for video {video_id}: {e}")
            break

    return comments_data  
