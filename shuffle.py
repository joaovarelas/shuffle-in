import requests, urllib
import json, random, base64
import re, time

from flask import *
app = Flask(__name__)



# Example Music Styles
styles = ['Pop','Rock','Jazz','House','Techno','Trap',
          'Vaporwave','Drum n Bass','Psy-Trance']


# Index Page
@app.route('/', methods=['GET', 'POST'])
def index():    
    style = request.form.get('style') if request.form.get('style') else None
    
    return render_template('index.html', bgcolor=rand_color(),
                           styles=styles, style=style)




# Play Page
@app.route('/play', methods=['GET','POST'])
def play():
    if not request.form.get('style') or not request.form.get('style') in styles:
        return render_error_template(**locals())
    
    style = request.form.get('style')
    music = get_random_music(style) #Discogs

    # Search on YouTube
    query = ('%s %s %s'%(music['artist'],music['track'],music['album_name']))
    video = get_youtube_id(query)
    if not video:
        return render_error_template(**locals())

    
    # Video2mp3 (disabled)
    #mp3url = get_youtube_mp3(video['id'])
    #if not mp3url:
    #return render_error_template(**locals())
    mp3url = ''

    # Final page, stream mp3 media
    return render_template('play.html', styles=styles, style=style,
                           bgcolor=rand_color(), thumb = music['thumb'],
                           artist = music['artist'],
                           album_name = music['album_name'],
                           album_style = music['style'], year = music['year'],
                           country = music['country'], yid = video['id'],
                           ytitle = video['title'], mp3 = mp3url)





# Handle Image requests     
@app.route('/image')
def get_image():
    if not request.args.get('src'):
        return 'Error getting image file'
    
    files = ['favicon.ico','git.png','reload.png', 'logo.png']
    src = request.args.get('src')
    
    if not src in files:
        return 'Error: file not found :('

    return send_file('images/'+src)





# Find random track according to selected style
def get_random_music(style):
    # Pagination Request
    url = 'https://api.discogs.com/database/search?style='+style
    headers = {'Authorization':'Discogs token=' <YOUR_DISCOGS_API_TOKEN>}
    r = requests.get(url, headers=headers)
    try:
        data = json.loads(r.text)
    except:
        print 'Could not load discogs API json (1 req)'
        return None
    
    items = data['pagination']['items']
    pages = data['pagination']['pages']
    
    if items == 0:
        return None

    # Select Item
    url += '&page=%d' % random.randint(1,pages)
    r = requests.get(url, headers=headers)
    try:
        data = json.loads(r.text)
    except:
        print 'Could not load discogs API json (2 req)'
        return None
    
    result = random.choice(data['results'])

    # Grab Thumb
    try:
        thumb_url = str(result['thumb'])
        thumb_r = requests.get(thumb_url)
        thumb = ("data:" + thumb_r.headers['Content-Type'] + ";" +
                 "base64," + base64.b64encode(thumb_r.content))
    except:
        print 'Error getting thumb uri base64'
        thumb = '' 

    # Grab Album Info
    title = '%s' % result['title'] # artistname - albumname
    artist = re.sub('\(.+\)', '', title.split(' - ')[0].replace('*',''))
    album_name = title.split(' - ')[1]
    style = ', '.join(result['style'][:3])
    try:
        year = result['year']
        country = result['country']
    except:
        year= '?'    
        country = '?'

    # Grab Album Tracks
    album_src = requests.get(result['resource_url'])
    try:
        data = json.loads(album_src.text)
        tracks = data['tracklist']
        track = random.choice(tracks)['title']
    except:
        print 'Error getting album resource data tracks'
        return None

    
    keys = ['thumb','artist','album_name',
            'style','year','country',
            'track']  
    vals = [thumb, artist, album_name, style,
            year, country, track]
    
    return dict(zip(keys, vals))



# Get Youtube Video ID and Title
def get_youtube_id(query):
    token = ''<YOUR_GOOGLE_YOUTUBE_API_TOKEN>
    url = ('''https://www.googleapis.com/youtube/v3/search?
           maxResults=50&part=snippet&key='''
           +token+'&q='
           +query)
    
    r = requests.get(url)
    
    try:
        data = json.loads(r.text)
        results = data['items']
        if data['pageInfo']['totalResults'] == 0:
            print 'Error on youtube id results zero'
            return None
    except:
        print 'Error getting youtube id results items'
        return None

    i=0
    video = results[i]
    while video['id']['kind'] != "youtube#video":
        i+=1
        if i<len(results):
            video = results[i]
        else:
            print 'Error iterating youtube results out of bound'
            return None
        
    yid = video['id']['videoId']
    title = video['snippet']['title']

    keys = ['id','title']
    vals = [yid, title]
    
    return dict(zip(keys, vals))




# Get MP3 Link from API
def get_youtube_mp3(yid):
    url = 'https://youtube2mp3api.com/@grab?format=mp3&streams=mp3&api=button&vidID=%s'%yid
    h = {'X-Requested-With':'XMLHttpRequest', 
         'Referer':('https://youtube2mp3api.com/@api/button/mp3/%s'%yid)}
    
    r = requests.get(url,headers=h)
    data = r.text 
    # txt2re
    rg = re.compile('.*?".*?".*?".*?".*?(".*?")',re.IGNORECASE|re.DOTALL)
    m = rg.search(data)
    
    if not m:
        print 'Error extracting mp3 api link'
        return None
    
    mp3url = m.group(1)
    return mp3url[1:-1]

 


# Gradient background
def rand_color():
    return ''.join(random.choice('0123456789abcdef') for i in range(6))
    

# Error page
def render_error_template(**vars):
    return render_template('error.html', bgcolor=rand_color(), styles=styles,
                           style=vars['style'], thumb = vars['music']['thumb'],
                           artist = vars['music']['artist'],
                           album_name = vars['music']['album_name'],
                           album_style = vars['music']['style'],
                           year = vars['music']['year'],
                           country = vars['music']['country'])
