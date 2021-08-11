from flask import Flask, render_template, request, redirect
from os import getenv
from dotenv import load_dotenv
import urllib.parse
import html
import random

from api.DiscogsAPI import Discogs
from api.YoutubeAPI import Youtube
#from SoundcloudAPI import Soundcloud

load_dotenv()


app = Flask(__name__)

discogs = Discogs(getenv("DISCOGS_TOKEN"))
youtube = Youtube(getenv("YOUTUBE_TOKEN"))
#soundcloud ...


@app.route("/")
def index():
    return render_template("index.html", bgcolor=rand_color(), shuffle=True)


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method != "POST":
        return redirect("/", code=302)

    query = request.form.get("query")
    style = request.form.get("style")
    shuffle = request.form.get("shuffle")

    query = "" if not query else query
    style = "" if not style else style
    shuffle = False if not shuffle else True
    
    enc_query = urllib.parse.quote(query.encode('utf-8'))
    enc_style = urllib.parse.quote(style.encode('utf-8'))
    
    releases = discogs.search(enc_query, enc_style, shuffle)
    tracklists = discogs.get_tracklists(releases)

    # Set youtube video id for each track
    tracklists = youtube.get_videos(tracklists)
    
    return render_template("content.html",
                           query=html.escape(query), style=html.escape(style),
                           shuffle=shuffle, bgcolor=rand_color(),
                           releases=releases, tracklists=tracklists)


def rand_color():
    return ''.join(random.choice('0123456789abcdef') for i in range(6))
