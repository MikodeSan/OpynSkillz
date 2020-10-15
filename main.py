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
# import argparse

import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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

def youtube_search(query):

    youtube = build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY,
        )

    # channels.list(part="id", mine=true)
    # channels.list(part="id", forUsername="username")

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=query,
        part='id,snippet',
        type='channel',
        maxResults=32,
    ).execute()

    videos = []
    channels = []
    playlists = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get('items', []):

        if search_result['id']['kind'] == 'youtube#video':
            videos.append('%s (%s)' % (search_result['snippet']['title'],
                                    search_result['id']['videoId']))
        
        elif search_result['id']['kind'] == 'youtube#channel':
            channels.append('%s (%s)' % (search_result['snippet']['title'],
                                    search_result['id']['channelId']))
        
        elif search_result['id']['kind'] == 'youtube#playlist':
            playlists.append('%s (%s)' % (search_result['snippet']['title'],
                                        search_result['id']['playlistId']))

    print('Videos:\n   -', '\n   -'.join(videos), '\n') 
    print('Channels:\n', '\n'.join(channels), '\n')
    print('Playlists:\n', '\n'.join(playlists), '\n')


    # if __name__ == '__main__':
    #   parser = argparse.ArgumentParser()
    #   parser.add_argument('--q', help='Search term', default='Google')
    #   parser.add_argument('--max-results', help='Max results', default=25)
    #   args = parser.parse_args()

    #   try:
    #     youtube_search(args)
    #   except HttpError, e:
    #     print 'An HTTP error %d occurred:\n%s' % (e.resp.status, e.content)


if __name__ == '__main__':

    youtube_search("apprendre la photo")
    youtube_search("marketing mania")
    youtube_search("my new life")
    # main()

