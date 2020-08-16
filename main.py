"""
Author: Fabio von Schelling Goldman
TODO:
- Figure out how to make more adaptable and versatile
--> Read in different types of files than just txt
- Possibly make a spotify super class that handles adding playlists etc.
- Fix The new line thing with browser
- Custom Button for browsing
- Hide .* files when browsing
- ReadMe for github
- Check for first time usage for credentials
- validate credentials in gui.py
"""

import gui as gui_class
import importGui
import spotify as sp


class MainRunner:

    def __init__(self):
        self.gui = gui_class.Gui()
        self.import_gui = importGui.ImportGui()
        self.spotify_import = sp.SpotifyImportPlaylist()

    def progress_bar_handler(self):
        done = False
        # Creates the window
        self.import_gui.progress_bar(None)
        while not done:
            perc_cov = self.spotify_import.percentage_imported
            if perc_cov is None:
                continue
            elif perc_cov == 100:
                done = True
            else:
                self.import_gui.progress_bar(perc_cov)

    def artist_lookup_thread(self):
        self.spotify_import.main("trello")
        success = self.spotify_import.return_boolean
        error_cause = self.spotify_import.return_error
        if not success:
            mode, name = self.import_gui.duplicated_list(error_cause)
            if mode == "append":
                self.spotify_import.main("trello", duplicate_handling="append")
            elif mode == "rename":
                self.spotify_import.main("trello", new_playlist_name=name[0])
        return

    def check_credentials(self):
        self.spotify_import.load_credentials()
        credentials_accepted = self.spotify_import.setup_spotify()
        while not credentials_accepted:
            self.gui.alert("The provided credentials for Spotify were not valid. Please login again.")
            button_pressed, creds = self.gui.login_window()
            if button_pressed and button_pressed != "Cancel":
                # This won't work yet, but need to read how to do this
                self.spotify_import.save_credentials("SPOTIFYUSERNAME", creds[0])
                self.spotify_import.save_credentials("SPOTIFYPASSWORD", creds[1])
                credentials_accepted = self.spotify_import.setup_spotify()
            else:
                exit(0)
        # Creds for Spotify were valid and the user is now logged in
        return

    def import_playlist(self):
        last_button_pressed, current_values = self.import_gui.choose_import_mode()
        if not last_button_pressed:
            exit(0)
        elif last_button_pressed == "Submit":
            if current_values["trello"]:
                self.spotify_import.main("trello")
                success = self.spotify_import.return_boolean
                error_cause = self.spotify_import.return_error
                if not success:
                    mode, name = self.import_gui.duplicated_list(error_cause)
                    if mode == "append":
                        self.spotify_import.main("trello", duplicate_handling="append")
                    elif mode == "rename":
                        self.spotify_import.main("trello", new_playlist_name=name[0])
                    else:
                        return
            else:
                if current_values["name"] != "Type a name for the playlist or one will be generated.":
                    playlist_name = current_values["name"]
                else:
                    playlist_name = ""
                self.spotify_import.main("txt", current_values["path"], playlist_name)
                success = self.spotify_import.return_boolean
                error_cause = self.spotify_import.return_error
                if not success:
                    mode, name = self.import_gui.duplicated_list(error_cause)
                    if mode == "append":
                        self.spotify_import.main("txt", current_values["path"], duplicate_handling="append")
                    elif mode == "rename":
                        self.spotify_import.main("txt", current_values["path"], new_playlist_name=name[0])
                    else:
                        return
            self.gui.alert("Successfully created the playlist.")
        elif last_button_pressed == "Cancel":
            return
        else:
            self.gui.alert("When importing the playlist something went wrong that shouldn't go wrong. Sorry.")

    def main(self):
        self.check_credentials()
        last_button_pressed, current_values = self.gui.main_menu(self.spotify_import.spotify_username)
        if last_button_pressed and last_button_pressed != "Quit":
            if last_button_pressed == "Create playlist":
                self.import_playlist()
            elif last_button_pressed == "Change User":
                self.gui.alert("Not implemented yet.")
        else:
            exit(0)


if __name__ == "__main__":
    m = MainRunner()
    m.main()
