# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

# This sample executes a search request for the specified search term.
# Sample usage:
#   python search.py --q=surfing --max-results=10
# NOTE: To use the sample, you must provide a developer key obtained
#       in the Google APIs Console. Search for "REPLACE_ME" in this code
#       to find the correct place to provide that key..

import os
import sys
import argparse
import json
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# APP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(BASE_DIR)
# print(APP_DIR)
sys.path.append(BASE_DIR)
# sys.path.append(APP_DIR)

from zenvar import *




# scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

# def main():
#     # Disable OAuthlib's HTTPS verification when running locally.
#     # *DO NOT* leave this option enabled in production.
#     os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

#     api_service_name = "youtube"
#     api_version = "v3"
#     client_secrets_file = GGL_KEY

#     # Get credentials and create an API client
#     flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
#         client_secrets_file, scopes)
#     credentials = flow.run_console()
#     youtube = googleapiclient.discovery.build(
#         api_service_name, api_version, credentials=credentials)

#     request = youtube.channels().list(
#         part="snippet,contentDetails,statistics",
#         id="UC_x5XG1OV2P6uZZ5FSM9Ttw"
#     )
#     response = request.execute()

#     print(response)


DEVELOPER_KEY = GGL_KEY
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def search(query, is_channel=True, is_video=True, is_playlist=True, n_result_max=23):

    youtube = build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY,
        )

    # channels.list(part="id", mine=true)
    # channels.list(part="id", forUsername="username")

    # Call the search.list method to retrieve results matching the specified
    # query term.

    type_lst = []
    if is_channel:
        type_lst.append('channel')
    if is_video:
        type_lst.append('video')
    if is_playlist:
        type_lst.append('playlist')
    
    type_s = ','.join(type_lst)
    print(type_s)
    
    response_dct = youtube.search().list(
        q=query,
        part='id,snippet',
        type=type_s,
        maxResults=n_result_max,
    ).execute()

    videos = []
    channels = []
    playlists = []

    # print(json.dumps(
    #         response_dct,
    #         # sort_keys=True,
    #         indent=4,
    #         )
    # )

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in response_dct['items']:

        result = search_result['id']['kind']
        snippet_dct = search_result['snippet']
        if result == 'youtube#video':
            videos.append('%s (%s)' % (search_result['snippet']['title'],
                                    search_result['id']['videoId']))
        
        elif result == 'youtube#channel':
            channels.append('{} ({}) {} {}'.format(snippet_dct['title'],
                                                snippet_dct['channelId'],
                                                snippet_dct['publishedAt'],
                                                snippet_dct['description'],
                                            )
            )

        elif result == 'youtube#playlist':
            playlists.append('%s (%s)' % (search_result['snippet']['title'],
                                        search_result['id']['playlistId']))

    print('Videos:\n   -', '\n   -'.join(videos), '\n') 
    print('Channels:\n', '\n'.join(channels), '\n')
    print('Playlists:\n', '\n'.join(playlists), '\n')


    youtube = build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY,
        )
    
    # youtube.channel().list(
    #     forusername=query,
    # ).execute()
    # print('Channels:\n', '\n'.join(youtube), '\n')


# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--q', help='Search term', default='Google')
#     parser.add_argument('--max-results', help='Max results', default=25)
#     args = parser.parse_args()

#     try:
#         youtube_search(args)
#     except HttpError as e:
#         print('An HTTP error {} occurred:\n{}').format(e.resp.status, e.content)


if __name__ == '__main__':

    search("apprendre la photo", is_video=False)
    search("marketing mania", is_playlist=False)
    search("my new life", is_video=False, is_playlist=False)
    # main()
