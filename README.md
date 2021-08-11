# shuffle-in
Python Flask webapp designed to shuffle between random musics of different styles. More than 10 Million of discography available (according to Discogs).

# Quick setup

## Requirements

Install Python3 requirements via pip: `pip3 install -r requirements.txt --user`

## Tokens

Grab API tokens from Discogs, Youtube & Soundcloud. 

Create `.env` file with the following structure:

```
DISCOGS_TOKEN=XXXXXXXX
YOUTUBE_TOKEN=XXXXXXXX
SOUNDCLOUD_TOKEN=XXXXXXXX
FLASK_APP=shuffle.py
```

## Run

Run as `python3 -m flask run`

