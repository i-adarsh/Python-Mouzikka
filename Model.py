# from mysql.connector import *
import mysql.connector
from traceback import *
from mysql.connector import DatabaseError


class Model:
    def __init__(self):
        self.song_dict = {}
        self.db_status = True
        self.conn = None
        self.cur = None
        try:
            self.conn = mysql.connector.connect(host='localhost', user='Python_Project', password='adarsh',
                                                database='Python_Project', auth_plugin='mysql_native_password')
            print("Connected Successfully to the Database")
            self.cur = self.conn.cursor()
        except DatabaseError:
            self.db_status = False
            print("DatabaseError : ", format_exc())

    def get_database_status(self):
        return self.db_status

    def close_database_conn(self):
        if self.cur is not None:
            self.cur.close()
            print("Cursor Closed")
        if self.conn is not None:
            self.conn.close()
            print("Connction Closed")

    def add_song(self, song_name, song_path):
        self.song_dict[song_name] = song_path
        # print("Song Added ", self.song_dict[song_name])
        # print(self.song_dict)

    def get_song_path(self, song_name):
        return self.song_dict[song_name]

    def remove_song(self, song_name):
        self.song_dict.pop(song_name)
        print("After Deletion", self.song_dict)

    def search_song_in_favourite(self, song_name):
        query = f"select * from myfavourites where song_name='{song_name}'"
        self.cur.execute(query)
        song_tuple = self.cur.fetchone()
        if song_tuple is None:
            return False
        return True

    def get_song_count(self):
        return len(self.song_dict)

    def add_song_to_favourite(self, song_name, song_path):
        is_song_present = self.search_song_in_favourite(song_name)
        if is_song_present == True:
            return "Song already exists"
        self.cur.execute("select max(song_id) from myfavourites")
        last_song_id = self.cur.fetchone()[0]
        next_song_id = 1
        if last_song_id is not None:
            next_song_id = last_song_id + 1
        self.cur.execute("insert into myfavourites value (%s, %s, %s)", (next_song_id, song_name, song_path))
        self.conn.commit()
        return "Song added Successfully"

    def load_songs_from_favourites(self):
        self.cur.execute("select song_name, song_path from myfavourites")
        song_present = False
        for song_name, song_path in self.cur:
            self.song_dict[song_name] = song_path
            song_present = True
        if song_present:
            return "List Populated from Favourites"
        else:
            return "No Song Found in Favourites"

    def remove_song_from_favourites(self, song_name):
        query = f"Delete from myfavourites where song_name='{song_name}'"
        self.cur.execute(query)
        count = self.cur.rowcount
        if count == 0:
            return "Song not present in your favourites"
        else:
            #
            self.song_dict.pop(song_name)
            self.conn.commit()
            return "Song deleted from Your favourites"
