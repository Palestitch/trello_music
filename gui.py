import PySimpleGUI as sg


class Gui:

    def __init__(self):
        self.button_pressed = None
        self.values = None
        self.window = None

    @staticmethod
    def alert(arg):
        # This is awkward still, but works
        sg.Popup(arg, title="Alert")

    def handle_window(self, window_name, window_layout):
        self.window = sg.Window(window_name).Layout(window_layout)
        self.button_pressed, self.values = self.window.Read()
        self.window.Close()

    def validate_credentials(self):
        if self.button_pressed != "Submit":
            return
        username = self.values[1]
        pw = self.values[2]
        # validate with spotify
        return

    def login_window(self):
        login = [
            [sg.Image(r'/home/fabio/Downloads/icons8-music-26.png')],
            [sg.Text('Please enter your Spotify email and password')],
            [sg.Text('E-mail', size=(15, 1)), sg.InputText()],
            [sg.Text('Password', size=(15, 1)), sg.InputText(password_char="*")],
            [sg.Submit(), sg.Cancel()]
        ]
        self.handle_window("Login", login)
        return self.button_pressed, self.values

    def main_menu(self, username):
        main_menu = [
            [sg.Text("Currently logged in as " + username + ".")],
            [sg.Button("Create playlist")],
            [sg.Button("Change user"), sg.Quit()]
        ]
        self.handle_window("Main Menu", main_menu)
        return self.button_pressed, self.values

    def main(self):
        self.alert("This method is deprecated.")
        return


if __name__ == "__main__":
    g = Gui()
    Gui.main(g)
