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

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
PROJECT_DIR = os.path.join(BASE_DIR, 'web_project')
sys.path.append(BASE_DIR)
sys.path.append(PROJECT_DIR)

class ZYouTube:
    
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'

    DEFAULT_N_RESULT_MAX = 50

    def __init__(self, key):

        self.key = key


    def get_video_from_channel(self, channel_id='', n_video=0):

        # https://www.googleapis.com/youtube/v3/search?key={your_key_here}&channelId={channel_id_here}&part=snippet,id&order=date&maxResults=20
        video_lst = []

        # n = self.DEFAULT_N_RESULT_MAX
        if n_video > 0:
            n = n_video
        else:
            n = self.DEFAULT_N_RESULT_MAX


        is_first = True
        enable = True
        page_id = ''
        idx = 1

        while enable:

            response_dct = self.search("", is_channel=False, is_video=True, is_playlist=False, channel_id=channel_id, page_id=page_id, n_max=n)
            # print('Hello', json.dumps(response_dct,indent=4))
            next_page_id = response_dct['next_page_token']

            if is_first is True:
                is_first = False

            video_lst.extend(response_dct['video_lst'])

            if next_page_id:
                page_id = next_page_id
                print(page_id)
            else:
                enable = False
        
            print(idx, len(response_dct['video_lst']))
            print(len(video_lst))
            idx += 1

        # print(json.dumps(page_info,indent=4))             # sort_keys=True,

        return video_lst


    # def get_video(self, video_id='', channel_id='', n_max=0):

    #     video_lst = []

    #     # https://www.googleapis.com/youtube/v3/search?key={your_key_here}&channelId={channel_id_here}&part=snippet,id&order=date&maxResults=20


    #     # n = self.DEFAULT_N_RESULT_MAX
    #     self._search("", is_channel=False, is_video=True, is_playlist=False, channel_id='UCuX05oOKyjib6CONyOpj5cw', n_max=720)

    #     response_dct = youtube.channels().list(**params_dct).execute()
    #     # print(json.dumps(response_dct,indent=4))             # sort_keys=True,

    #     if response_dct['pageInfo']['resultsPerPage']:

    #         etag = response_dct['etag']
    #         channel_dct = response_dct['items'][0]

    #     return video_lst


    # def get_playlist(playlist_id='', channel_id='', n_max=0):

    #     playlist_lst = []

    #     # self.DEFAULT_N_RESULT_MAX
    #     search("apprendre la photo", is_channel=False, is_video=True, is_playlist=False, channel_id='UCuX05oOKyjib6CONyOpj5cw', n_max=720)

    #     return playlist_lst


    def get_channel(self, channel_id, n_max=0):
        
        etag = ''
        channel_dct = {}

        params_dct = {}
        params_dct['part'] = 'snippet,contentDetails,statistics,topicDetails,status,brandingSettings,contentOwnerDetails,localizations'
        if n_max > 0:
            params_dct['maxResults'] = n_max
        else:
            params_dct['maxResults'] = self.DEFAULT_N_RESULT_MAX

        if channel_id:
            params_dct['id'] = channel_id

            youtube = self.__build()
            response_dct = youtube.channels().list(**params_dct).execute()
            print(json.dumps(response_dct,indent=4))             # sort_keys=True,

            if response_dct['pageInfo']['resultsPerPage'] > 0:
                # channel found

                etag = response_dct['etag']
                channel_dct = response_dct['items'][0]

        return etag, channel_dct


    def search(self, query, is_channel=True, is_video=True, is_playlist=True, channel_id='', page_id='', n_max=0):
        """
        Call the search.list method to retrieve results matching the specified query term.
        """
        
        youtube = self.__build()

        # channels.list(part="id", mine=true)
        # channels.list(part="id", forUsername="username")

        type_lst = []
        if is_channel:
            type_lst.append('channel')
        if is_video:
            type_lst.append('video')
        if is_playlist:
            type_lst.append('playlist')
        
        type_s = ','.join(type_lst)

        params_dct = {
            'part':'id,snippet', 
            'type':type_s, 
            }

        if query:
            params_dct['q'] = query

        if n_max > 0:
            params_dct['maxResults'] = n_max
        else:
            params_dct['maxResults'] = self.DEFAULT_N_RESULT_MAX

        if is_video and channel_id :
            params_dct['channelId'] = channel_id

        if page_id:
            params_dct['pageToken'] = page_id

        etag = ''
        response_dct = youtube.search().list(**params_dct).execute()
        
        next_page_token = ''
        if 'nextPageToken' in response_dct:
            next_page_token = response_dct['nextPageToken']
            

        video_lst = []
        channel_lst = []
        playlist_lst = []

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
                video_dct = {}
                video_dct['id'] = search_result['id']['videoId']
                video_dct['etag'] = search_result['etag']
                video_dct['channel_id'] = snippet_dct['channelId']
                video_dct['channel_title'] = snippet_dct['channelTitle']
                video_dct['published_t'] = snippet_dct['publishedAt']
                video_dct['title'] = snippet_dct['title']
                video_dct['description'] = snippet_dct['description']
                video_dct['thumbnail_url'] = snippet_dct['thumbnails']['high']['url']

                video_lst.append(video_dct)
            
            elif result == 'youtube#channel':
                channel_dct = {}
                channel_dct['id'] = search_result['id']['channelId']
                channel_dct['published_t'] = snippet_dct['publishedAt']
                channel_dct['title'] = snippet_dct['title']
                channel_dct['description'] = snippet_dct['description']
                channel_dct['thumbnail_url'] = snippet_dct['thumbnails']['high']['url']

                channel_lst.append(channel_dct)

            elif result == 'youtube#playlist':
                playlist_dct = {}
                playlist_dct['id'] = search_result['id']['playlistId']
                playlist_dct['channel_id'] = snippet_dct['channelId']
                playlist_dct['channel_title'] = snippet_dct['channelTitle']
                playlist_dct['published_t'] = snippet_dct['publishedAt']
                playlist_dct['title'] = snippet_dct['title']
                playlist_dct['description'] = snippet_dct['description']
                playlist_dct['thumbnail_url'] = snippet_dct['thumbnails']['high']['url']

                playlist_lst.append(playlist_dct)

        # print('Videos:\n   -', '\n   -'.join(videos), '\n') 
        # print('Channels:\n', '\n'.join(channels), '\n')
        # print('Playlists:\n', '\n'.join(playlists), '\n')

        # "kind": "youtube#searchListResponse",
        #     "etag": "WJVnc8CiPr-4mzU_pQLrtfOuBsU",
        #     "nextPageToken": "CDIQAA",
        #     "regionCode": "FR",
        #     "pageInfo": {
        #         "totalResults": 481,
        #         "resultsPerPage": 50
        #     },
        #     "items": [
        #         {
        #             "kind": "youtube#searchResult",
        #             "etag": "9UpEKXy1qwmoHVvK-sHEvIjNJFk",
        #             "id": {
        #                 "kind": "youtube#video",
        #                 "videoId": "wDAmezoNHJY"
        #             },
        #             "snippet": {
        #                 "publishedAt": "2020-05-24T16:00:33Z",
        #                 "channelId": "UCuX05oOKyjib6CONyOpj5cw",
        #                 "title": "\ud83d\udcf7Les VRAIES 5 ERREURS du de\u0301butant en photo",
        #                 "description": "Vous en avez sans doute d\u00e9j\u00e0 vu passer, des articles ou des vid\u00e9os sur \"les 5 erreurs du d\u00e9butant en photo\". Si tous ne sont pas inutiles, je pense qu'ils ...",
        #                 "thumbnails": {
        #                     "default": {
        #                         "url": "https://i.ytimg.com/vi/wDAmezoNHJY/default.jpg",
        #                         "width": 120,
        #                         "height": 90
        #                     },
        #                     "medium": {
        #                         "url": "https://i.ytimg.com/vi/wDAmezoNHJY/mqdefault.jpg",
        #                         "width": 320,
        #                         "height": 180
        #                     },
        #                     "high": {
        #                         "url": "https://i.ytimg.com/vi/wDAmezoNHJY/hqdefault.jpg",
        #                         "width": 480,
        #                         "height": 360
        #                     }
        #                 },
        #                 "channelTitle": "Apprendre la Photo",
        #                 "liveBroadcastContent": "none",
        #                 "publishTime": "2020-05-24T16:00:33Z"
        #             }
        #         },

        resp_dct = {}
        resp_dct['next_page_token'] = next_page_token
        resp_dct['channel_lst'] = channel_lst
        resp_dct['video_lst'] = video_lst
        resp_dct['playlist_lst'] = playlist_lst

        return resp_dct


    def __build(self):

        youtube = build(
            self.YOUTUBE_API_SERVICE_NAME,
            self.YOUTUBE_API_VERSION,
            developerKey=self.key,
            )

        return youtube


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

    from settings.zenvar import GGL_KEY

    ytb_obj = ZYouTube(GGL_KEY)

    # etag, response_dct = ytb_obj._search("apprendre la photo", is_video=False)
    etag, response_dct = ytb_obj.search("thomas hammoudi", is_video=False)
    # etag, channel_dct = ytb_obj.get_channel(channel_id='UCuX05oOKyjib6CONyOpj5cw')
    print(json.dumps(response_dct,indent=4))             # sort_keys=True,

    video_lst = ytb_obj.get_video_from_channel(channel_id='UC2DfEpPYB1kxmJFX2MoiG_A', n_video=500)
    print('N videos:', len(video_lst))

    # # search("marketing mania", is_playlist=False)
    # channel_dct = youtube.channels().list(
    #     part='snippet,contentDetails,statistics,topicDetails,status,brandingSettings,contentOwnerDetails,localizations',        # auditDetails
    #     id='UCSmUdD2Dd_v5uqBuRwtEZug',
    # ).execute()
    # print(json.dumps(channel_dct,indent=4))             # sort_keys=True,
    # search("apprendre la photo", is_channel=False, is_video=True, is_playlist=False, channel_id='UCSmUdD2Dd_v5uqBuRwtEZug', n_max=720)

    # # search("my new life", is_video=False, is_playlist=False)
    # channel_dct = youtube.channels().list(
    #     part='snippet,contentDetails,statistics,topicDetails,status,brandingSettings,contentOwnerDetails,localizations',
    #     id='UCPMBFQQ5IDvxnW-vZfVWhLA',
    # ).execute()
    # print(json.dumps(channel_dct,indent=4))             # sort_keys=True,
    # search("apprendre la photo", is_channel=False, is_video=True, is_playlist=False, channel_id='UCPMBFQQ5IDvxnW-vZfVWhLA', n_max=720)
