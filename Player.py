import Model
from pygame import mixer
from tkinter import filedialog
import os
from mutagen.mp3 import MP3

class Player:
    def __init__(self):
        mixer.init()
        self.my_model = Model.Model()

    def get_database_status(self):
        return self.my_model.get_database_status()

    def close_player(self):
        mixer.music.stop()
        self.my_model.close_database_conn()

    def set_volume(self, volume_level):
        mixer.music.set_volume(volume_level)


    def add_song(self):
        song_path = filedialog.askopenfilenames(title="Select Your Song ....",filetypes=[("mp3 files", "*.mp3")])
        print(song_path)
        song_name_list = []
        if song_path == "":
            return
        if len(song_path) > 0:
            for i in range(0, len(song_path)):
                # print(i, len(song_path))
                song_name = os.path.basename(song_path[i])
                self.my_model.add_song(song_name, song_path[i])
                song_name_list.append(song_name)
            return song_name_list
        # song_name = os.path.basename(song_path)
        # self.my_model.add_song(song_name, song_path)
        # return song_name

    def remove_song(self, song_name):
        self.my_model.remove_song(song_name)

    def get_song_count(self):
        return self.my_model.get_song_count()

    def get_song_length(self, song_name):
        self.song_path = self.my_model.get_song_path(song_name)
        self.audio_tag = MP3(self.song_path)
        song_length = self.audio_tag.info.length
        return song_length

    def play_song(self):
        mixer.quit()
        mixer.init(frequency= self.audio_tag.info.sample_rate)
        mixer.music.load(self.song_path)
        mixer.music.play()

    def play_seek_song(self, seek_value):
        mixer.quit()
        mixer.init(frequency=self.audio_tag.info.sample_rate)
        mixer.music.load(self.song_path)
        mixer.music.play(loops=0, start=seek_value)

    def stop_song(self):
        mixer.music.stop()

    def pause_song(self):
        mixer.music.pause()

    def unpause_song(self):
        mixer.music.unpause()

    def add_song_to_favourite(self, song_name):
        song_path = self.my_model.get_song_path(song_name)
        result = self.my_model.add_song_to_favourite(song_name, song_path)
        return result

    def load_songs_from_favourites(self):
        result = self.my_model.load_songs_from_favourites()
        return result,self.my_model.song_dict

    def remove_song_from_favourites(self, song_name):
        result = self.my_model.remove_song_from_favourites(song_name)
        return result











































































# import mysql.connector
# import traceback
# connection = None
# try:
#     connection = mysql.connector.connect(host='localhost', user='Python_Project', password='adarsh', database='Python_Project', auth_plugin='mysql_native_password')
#     print(connection)
#     print("Connected Successfully to the Database")
# except mysql.connector.DatabaseError:
#     print("DatabaseError")
#     print(traceback.format_exc())
# finally:
#     if connection is not None:
#         connection.close()
#         print("Dissconnected from Database Successfully")