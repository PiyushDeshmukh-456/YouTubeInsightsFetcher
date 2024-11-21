from googleapiclient.discovery import build

def test_api_connection(api_key):
    youtube = build('youtube', 'v3', developerKey=api_key, cache_discovery=False)
    response = youtube.search().list(
        part='snippet',
        q='test',
        maxResults=1
    ).execute()
    print(response)

api_key = "AIzaSyAo06LBSmIYdznnpEw4COyeiOqknEnyQJU"  # Replace with your actual API key
test_api_connection(api_key)
