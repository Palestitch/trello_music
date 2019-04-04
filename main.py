"""
Author: Fabio von Schelling Goldman
TODO:
- Figure out how to make more adaptable and versatile
--> Read in different types of files (txt)
- Probably best to make the whole thing with classes and hide the internals
"""

from trello import TrelloClient, os
import spotipy
import spotipy.util as util
from dotenv import load_dotenv


def setup_spotify(username):
    scope = "playlist-modify-public"
    token = util.prompt_for_user_token(username, scope, client_id=os.getenv("SPOTIFYID"),
                                       client_secret=os.getenv("SPOTIFYSECRET"),
                                       redirect_uri="http://localhost:8888/callback/")
    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        return sp
    else:
        print("Can't get token for", username)
        exit(-1)


def new_list(username, sp, new_name):
    existing_lists = sp.user_playlists(username)['items']
    for name in existing_lists:
        if new_name == name['name']:
            print("Playlist with this name exists already, please choose a new name.")
            return False
    return True


def add_all_cards(username, sp, new_playlist, category):
    for card in category.list_cards():
        result = sp.search(card.name, type="artist")
        if len(result['artists']['items']) == 0:
            continue
        tops = sp.artist_top_tracks(result['artists']['items'][0]['id'])
        for track in tops['tracks']:
            sp.user_playlist_add_tracks(username, new_playlist['id'], [track['uri']])
            print(track['name'])


def spotify(category):
    username = os.getenv("SPOTIFYUSERNAME")
    sp = setup_spotify(username)
    if not new_list(username, sp, category.name):
        return
    new_playlist = sp.user_playlist_create(username, category.name)
    add_all_cards(username, sp, new_playlist, category)
    print("Finished processing a list")


def setup_trello_client():
    client_trello = TrelloClient(
        api_key=os.getenv("TRELLOKEY"),
        api_secret=os.getenv("TRELLOSECRET"),
        token=os.getenv("TRELLOTOKEN")
    )
    return client_trello


def trello():
    client_trello = setup_trello_client()
    music_board = client_trello.search("Music to listen to")[0]
    categories = music_board.list_lists()
    for category in categories:
        spotify(category)


def main():
    load_dotenv()
    trello()


if __name__ == "__main__":
    main()
