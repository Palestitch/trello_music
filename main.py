'''
TODO:
- Figure out how to make more adaptable and versatile
--> Don't double playlists
--> Read in different types of files
'''
from trello import TrelloClient, os
import spotipy
import spotipy.util as util
from dotenv import load_dotenv


def spotify(category):
    scope = "playlist-modify-public"
    username = os.getenv("SPOTIFYUSERNAME")
    token = util.prompt_for_user_token(username, scope, client_id=os.getenv("SPOTIFYID"),
                                       client_secret=os.getenv("SPOTIFYSECRET"),
                                       redirect_uri="http://localhost:8888/callback/")
    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
    else:
        print("Can't get token for", username)
        exit(-1)
    playlists = sp.user_playlist_create(username, category.name)
    for card in category.list_cards():
        result = sp.search(card.name, type="artist")
        if len(result['artists']['items']) == 0:
            continue
        tops = sp.artist_top_tracks(result['artists']['items'][0]['id'])
        for track in tops['tracks']:
            sp.user_playlist_add_tracks(username, playlists['id'], [track['uri']])
            print(track['name'])
    print("Finished processing a list")


def trello():
    client_trello = TrelloClient(
        api_key=os.getenv("TRELLOKEY"),
        api_secret=os.getenv("TRELLOSECRET"),
        token=os.getenv("TRELLOTOKEN")
    )
    music_board = client_trello.search("Music to listen to")[0]
    categories = music_board.list_lists()
    for category in categories:
        spotify(category)


def main():
    load_dotenv()
    trello()


if __name__ == "__main__":
    main()