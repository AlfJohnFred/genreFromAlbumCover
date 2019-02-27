import errno
import requests
import os
import spotipy
import spotipy.util as util
from Config import CLIENT_ID, CLIENT_SECRET
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

token = util.oauth2.SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
cache_token = token.get_access_token()


def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return -1


def save_album_art(id, folder_name):
    albums = []
    results = sp.artist_albums(artist['id'], album_type='album')
    albums.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    print('Total albums:', len(albums))
    for album in albums:
        for images in album['images']:
            if images['height'] == 640:
                url = (images['url'])
                print(url)
                filename = "D:\\CodePlayPen\\Python\\genreFromAlbumCover\\" + folder_name + "\\" + url.split('/')[
                    4] + ".jpeg"

                s = requests.Session()
                retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
                s.mount('http://', HTTPAdapter(max_retries=retries))
                album_art = s.get(url, allow_redirects=True)

                os.makedirs(os.path.dirname(filename), exist_ok=True)
                open(filename, 'wb').write(album_art.content)


def create_destination_folder(artist, genre):
    print('====', artist['name'], '====')
    print('Popularity: ', artist['popularity'])
    if len(artist['genres']) > 0:
        print('Genres: ', ','.join(artist['genres']))
    folder = "D:\\CodePlayPen\\Python\\genreFromAlbumCover\\" + genre
    try:
        os.makedirs(folder)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


if __name__ == '__main__':
    sp = spotipy.Spotify(cache_token)
    sp.trace = False

    with open("metal.txt", 'r') as f:
        names = [line.strip() for line in f]
        genre = "Metal"
    for name in names:
        artist = get_artist(name)
        if artist != -1:
            folder_name = create_destination_folder(artist, genre)
            save_album_art(artist, genre)
        else:
            print("No data for"+name)
