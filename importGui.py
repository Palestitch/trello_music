import PySimpleGUI as sg


class ImportGui:

    def __init__(self):
        self.window = None
        self.button_pressed = None
        self.values = None

    def progress_bar(self, progress):
        if progress is None:
            layout = [[sg.Text('Importing artists')],
                      [sg.ProgressBar(100, orientation='h', size=(20, 20), key='progressbar')],
                      ]
            self.window = sg.Window('Artist import', layout)
            return
        progress_bar = self.window.FindElement('progressbar')
        event, values = self.window.Read(timeout=0)
        if event is None:
            exit(0)
        progress_bar.UpdateBar(progress)
        if progress == 100:
            self.window.Close()

    @staticmethod
    def trello_choose_playlist(categories):
        layout = [[sg.Text("Please choose a list to import from")]]
        for c in categories:
            layout.append([sg.Radio(c.name, key=c.name, group_id="category")])
        layout.append([sg.Submit(), sg.Cancel()])
        window = sg.Window('Choose board', layout)
        button, value = window.Read()
        window.Close()
        return button, value

    @staticmethod
    def duplicated_list(name):
        duplicate_interface = [
            [sg.Text("A playlist with the name '" + name + "' already exists please choose how to proceed.")],
            [sg.Button("Append to '" + name + "'", key="append",
                       tooltip="This might add duplicate songs to the playlist.")],
            [sg.Text("OR")],
            [sg.Button("Rename '" + name + "' to", key="rename"), sg.InputText("Enter new name here.")],
            [sg.Cancel()]
        ]
        tmp_window = sg.Window('Duplicated playlist').Layout(duplicate_interface)
        tmp_button_pressed, tmp_values = tmp_window.Read()
        tmp_window.Close()
        return tmp_button_pressed, tmp_values

    def choose_import_mode(self):
        file_path = sg.InputText(visible=False, key="path", enable_events=True)
        file_browse_button = sg.FileBrowse(visible=False, key="browser", target="path",
                                           file_types=(("Text Files", ".txt"),))
        playlist_name = sg.InputText("Type a name for the playlist or one will be generated.", visible=False, key="name")
        create_playlist_menu = [
            [sg.Text("Please choose how to import the playlist.")],
            [sg.Radio("Import from Trello", "rad1", key="trello"),
             sg.Radio("Import from txt file.", "rad1", enable_events=True, key="txt")],
            [file_browse_button, file_path, playlist_name],
            [sg.Submit(), sg.Cancel()]
        ]
        self.window = sg.Window('Create new playlist').Layout(create_playlist_menu)
        self.button_pressed, self.values = self.window.Read()
        if self.button_pressed == "txt":
            file_path.visible = True
            file_browse_button.visible = True
            self.window.Element('browser').Update(visible=True)
            self.window.Element('path').Update(visible=True)
            self.window.Element('name').Update(visible=True)
            self.button_pressed, self.values = self.window.Read()
            self.button_pressed, self.values = self.window.Read()
        self.window.Close()
        return self.button_pressed, self.values
