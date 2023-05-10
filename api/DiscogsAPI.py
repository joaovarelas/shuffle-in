import requests
import json
import random


class Discogs:

    def __init__(self, token):
        self.url = "https://api.discogs.com/"
        self.token = token

    def request(self, params):
        print("{}{}".format(self.url, params))
        req = requests.get("{}{}".format(self.url, params),
                           headers={"Authorization":
                                    "Discogs token={}".format(self.token)})
        return json.loads(req.text)

    def search(self, query, style, shuffle):
        params = "database/search?type=release&per_page=1&query={}&style={}".format(
            query, style)
        resp = self.request(params)

        if shuffle:
            max_pages = resp["pagination"]["pages"]
            page = random.randint(1, max_pages)

            params = "database/search?type=release&per_page=1&page={}&query={}&style={}".format(
                page, query, style)
            resp = self.request(params)

        return resp

    def get_tracks(self, release_id):
        params = "releases/{}".format(release_id)
        resp = self.request(params)
        return resp

    def get_tracklists(self, releases):
        tracklists = {}
        for release in releases["results"]:
            release_id = release["id"]
            tracklist = self.get_tracks(release_id)
            tracklists[release_id] = tracklist

        return tracklists
