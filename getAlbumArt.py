import requests
import os
import spotipy
import spotipy.util as util
from Config import CLIENT_ID, CLIENT_SECRET

token = util.oauth2.SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

cache_token = token.get_access_token()


def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None


def save_album_art(id,folder_name):
    albums = []
    results = sp.artist_albums(artist['id'], album_type='album')
    albums.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    print('Total albums:', len(albums))
    unique = set()  # skip duplicate albums
    for album in albums:
        name = album['name'].lower()
        for images in album['images']:
            if images['height'] == 640:
                url = (images['url'])
                filename = "D:\\CodePlayPen\\Python\\genreFromAlbumCover\\" + folder_name+"\\" + url.split('/')[4]+".jpeg"
                album_art = requests.get(url, allow_redirects=True)
                print(filename)
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                open(filename, 'wb').write(album_art.content)


def show_artist(artist):
    print('====', artist['name'], '====')
    print('Popularity: ', artist['popularity'])
    if len(artist['genres']) > 0:
        print('Genres: ', ','.join(artist['genres']))
    filename = "/"+artist['name']
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    return artist['name']


if __name__ == '__main__':
    sp = spotipy.Spotify(cache_token)
    sp.trace = False

    name = 'metallica'
    artist = get_artist(name)
    folder_name = show_artist(artist)
    save_album_art(artist,folder_name)
