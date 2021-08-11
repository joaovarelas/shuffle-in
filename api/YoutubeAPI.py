import requests
import json
import threading
from youtubesearchpython import VideosSearch

class Youtube:
    
    def __init__(self, token):
        self.url = "https://youtube.googleapis.com/"
        self.token = token

    def request(self, params):
        req = requests.get("{}{}".format(self.url, params))
        return json.loads(req.text)

    def search(self, query):
        params = "youtube/v3/search?maxResults=1&key={}&q={}".format(self.token, query)
        resp = self.request(params)
        return resp

    
    async_video_list = None
    def get_videos(self, tracklists):
        for release in tracklists.values():
            tracklist = release["tracklist"]
            
            self.async_video_list = [None]*len(tracklist)
            threads = []
            
            for i in range(len(tracklist)):
                track = tracklist[i]
                query = "{} {} {}".format(track["title"],
                                          release["artists_sort"],
                                          release["title"])
                                          

                t = threading.Thread(target=self.get_videos_async, args=(query, i,))
                threads.append(t)
              
            [t.start() for t in threads]
            [t.join() for t in threads]

            for i in range(len(tracklist)):
                tracklist[i]["youtube_id"] = self.async_video_list[i]
                        
        return tracklists
    

    def get_videos_async(self, query, i):
        print(query)
        video_search = VideosSearch(query, limit = 1).result()
        if video_search["result"]:
            self.async_video_list[i] = video_search["result"][0]["id"]

        return

    
    '''
    # Sync
    def get_videos(self, tracklists):
        for tracklist in tracklists.values():
            for track in tracklist["tracklist"]:
                title = "{} {}".format(tracklist["artists_sort"],
                                       track["title"])
                video_search = VideosSearch(title, limit = 1).result()
                track["youtube_id"] = video_search["result"][0]["id"]
                
        return tracklists
    '''
                         
    '''
    # Youtube V3 API (exceed quota)
    def get_videos(self, tracklists):
        for tracklist in tracklists.values():
            for track in tracklist["tracklist"]:
                title = "{} {}".format(tracklist["artists_sort"],
                                       track["title"])
                video = self.search(title)
                print(video)
                video_id = video["items"][0]["id"]["videoId"]
                track["video_id"] = video_id

        return tracklists
    '''
        

