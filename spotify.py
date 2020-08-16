import spotipy
import spotipy.util as util
import yaml
from trello.trelloclient import TrelloClient
import importGui
import gui


class SpotifyImportPlaylist:

    def __init__(self):
        self.spotify_username = ""
        self.duplicate_handling = ""
        self.user_info = None
        self.sp = None
        self.percentage_imported = None
        self.return_boolean = None
        self.return_error = None
        self.trello_selection = ""

    # Return False, if list is duplicate
    def main(self, option, file_name=None, duplicate_handling="", new_playlist_name=""):
        self.duplicate_handling = duplicate_handling
        if option == "trello":
            self.trello(new_playlist_name)
        elif option == "txt":
            self.txt(file_name, new_playlist_name)

    def find_right_category(self, categories):
        for c in categories:
            if c.name == self.trello_selection:
                return c

    def find_category_from_values(self, values, categories):
        for key, val in values.items():
            if val:
                for c in categories:
                    if c.name == key:
                        self.trello_selection = key
                        return c
        return None

    def trello(self, new_playlist_name):
        client_trello = self.setup_trello_client()
        music_board = client_trello.search("Music to listen to")[0]
        categories = music_board.list_lists()
        if self.trello_selection:
            category = self.find_right_category(categories)
            self.spotify_trello(category, new_playlist_name) if new_playlist_name else self.spotify_trello(category, self.trello_selection)
        else:
            button, values = importGui.ImportGui.trello_choose_playlist(categories)
            if button == "Submit":
                category = self.find_category_from_values(values, categories)
                if not category:
                    gui.Gui.alert("No Choice has been made. Remake this dialog.")
                    # This could be bad if done many many times
                    self.trello(new_playlist_name)
                else:
                    self.spotify_trello(category, new_playlist_name) if new_playlist_name else self.spotify_trello(category, self.trello_selection)
            elif button == "Cancel":
                return
            else:
                exit(0)

    def setup_trello_client(self):
        client_trello = TrelloClient(
            api_key=self.user_info["TRELLOKEY"],
            api_secret=self.user_info["TRELLOSECRET"],
            token=self.user_info["TRELLOTOKEN"]
        )
        return client_trello

    def spotify_trello(self, category, new_playlist_name):
        self.spotify_username = str(self.user_info["SPOTIFYUSERNAME"])
        self.setup_spotify()
        playlist_to_add_to = self.find_list(new_playlist_name)
        if playlist_to_add_to == "":
            self.return_boolean = False
            self.return_error = category.name
        else:
            self.add_all_artists(playlist_to_add_to, category.list_cards(), trello=True)
            self.return_boolean = True
            self.return_error = None

    def txt(self, file_name, playlistname=""):
        self.spotify_txt(file_name, playlistname)

    def spotify_txt(self, file_name, playlist_name=""):
        if not playlist_name:
            tmp_name = file_name.split("/")[-1]
            playlist_name = tmp_name.split(".")[0]
        playlist_to_add_to = self.find_list(playlist_name)
        if playlist_to_add_to == "":
            self.return_boolean = False
            self.return_error = playlist_name
        else:
            with open(file_name) as artists:
                self.add_all_artists(playlist_to_add_to, artists.readlines())
            self.return_boolean = True
            self.return_error = None

    def find_list(self, new_playlist_name):
        existing_lists = self.sp.user_playlists(self.spotify_username)['items']
        for name in existing_lists:
            if new_playlist_name == name['name']:
                if self.duplicate_handling == "":
                    return ""
                elif self.duplicate_handling == "append":
                    return name['id']
                elif self.duplicate_handling == "skip":
                    return ""
                else:
                    return ""
        playlist_to_add = self.sp.user_playlist_create(self.spotify_username, new_playlist_name)
        return playlist_to_add['id']

    def add_all_artists(self, new_playlist_name, list_to_iterate, trello=False):
        temp_gui_element = importGui.ImportGui()
        temp_gui_element.progress_bar(self.percentage_imported)
        self.percentage_imported = 0
        for item in list_to_iterate:
            if trello:
                result = self.sp.search(item.name, type="artist")
            else:
                if item.strip() == "":
                    continue
                result = self.sp.search(item, type="artist")
            if len(result['artists']) == 0 or len(result['artists']['items']) == 0:
                # We couldn't find the artist or any songs connected to the artist
                continue
            tops = self.sp.artist_top_tracks(result['artists']['items'][0]['id'])
            # We assume the first artist found is the one we are looking for
            for track in tops['tracks']:
                self.sp.user_playlist_add_tracks(self.spotify_username, new_playlist_name, [track['uri']])
            self.percentage_imported += 100 / len(list_to_iterate)
            print(self.percentage_imported)
            temp_gui_element.progress_bar(self.percentage_imported)
            if self.percentage_imported > 100:
                self.percentage_imported = 100
        self.percentage_imported = 100
        temp_gui_element.progress_bar(self.percentage_imported)

    def setup_spotify(self):
        self.spotify_username = str(self.user_info["SPOTIFYUSERNAME"])
        scope = "playlist-modify-public"
        token = util.prompt_for_user_token(self.spotify_username, scope, client_id=self.user_info["SPOTIFYID"],
                                           client_secret=self.user_info["SPOTIFYSECRET"],
                                           redirect_uri="http://localhost:8888/callback/")
        if token:
            self.sp = spotipy.Spotify(auth=token)
            self.sp.trace = False
            return True
        else:
            print("Can't get token for", self.spotify_username)
            return False

    def load_credentials(self):
        self.user_info = yaml.load(open("creds.yaml"), Loader=yaml.BaseLoader)

    @staticmethod
    def save_credentials(description, value):
        with open("creds.yaml") as file:
            yaml.dump({description: value}, file, Dumper=yaml.BaseDumper)
