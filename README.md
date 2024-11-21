# YouTube Data Fetcher
## Overview
YouTube Data Fetcher is a Python-based project that extracts metadata and comments from a YouTube channel and saves the data into an Excel file. This tool leverages the YouTube Data API to fetch video details and comments and organizes the results into separate sheets within an Excel file.
## Features
1.	Fetches video metadata including title, description, views, likes, and duration.
2.	Retrieves the latest 100 comments and their replies for each video.
3.	Saves data into an Excel file with the channel name.
4.	Automatically handles pagination for videos and comments.
5.	Includes an API Tester to validate YouTube Data API keys.

## Prerequisites
1. Python 3.7 or higher
2. A valid YouTube Data API v3 key

## Required libraries
1. google-api-python-client
2. pandas
3. xlsxwriter

## How to Get the YouTube Data API Key
If you haven't obtained your YouTube Data API key yet, please refer to the detailed instructions in the following PDF document:

[Download the PDF Guide to Get the YouTube API Key ](https://drive.google.com/file/d/1cJaf0NYpKfYKa12XfrFgCYlf9X61ssMs/view?usp=sharing)

In the PDF, you will find step-by-step instructions on how to create a project in the Google Cloud Console, enable the YouTube Data API, and generate your API key.

## Run the Application
1. Open a terminal or command prompt.
2. Run the main.py script:
3. Provide the API key and YouTube channel URL when prompted.

## Output
1)	The extracted data will be saved in an Excel file named after the channel.
2)	The Excel file contains two sheets:
   
    a)	Video Data: Metadata for all videos
   
    b)	Comments Data: Comments and replies for all videos.


## API Tester
This project includes an API Tester to validate your YouTube Data API key before running the main script.
Usage
1.	Navigate to the project folder.
2.	Run the test_api_connection.py script:
3.	Enter your API key when prompted.
4.	If the key is valid, you'll see a success message. Otherwise, you'll get details about the error.

