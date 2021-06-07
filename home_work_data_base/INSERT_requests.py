import sqlalchemy
import random

#db =

engine = sqlalchemy.create_engine(db)

connection = engine.connect()


# create data table performers
list_name_performers = ['Enrique Iglesias','Linkin Park','Arash','Eminem','50 cent','Ava Max','K-Maro','Pink']

# create data table genre
list_genre = ['Jazz',' Rock', 'Pop', 'Folk', 'Rap']

# create data table album
list_name_album = ['Meteora','Greatest Hits','Greatest Hits','Planet Jarre','The Dark Side of the Moon','Power Up','Everyday Life','McMxc A.D']
list_years_of_issue_album = [2018, 2019, 2020, 2021, 2017, 2018, 2020, 2019 ]

album_zip = zip(list_name_album,list_years_of_issue_album)
list_album = list(album_zip)

# create data table track
tracks = ['Lets Go Home Together', 'Whats Next', '6 For 6', 'Anxious', 'Rasputin', 'Peaches', 'Summer 91 (Looking Back)',
          'Summer 91 (Looking Back)', 'my love', 'Last Time', 'Black Hole', 'Addicted', 'Patience',
          'Leave The Door Open', 'Hold On', 'How Does It Feel']

duration = [2.15, 3.61, 3.15, 4.55, 3.99, 2.66, 3.56, 5.66, 4.23, 3.22, 3.86, 3.57, 3.93, 3.45, 3.57, 2.89  ]
list_id_album =[1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8]

track_zip = zip(tracks, duration, list_id_album)
list_track = list(track_zip)

#create data table collection
list_name_collection = ['COVERS', 'E', 'New j-pop', 'Forza Horizon 4', 'Mi amor', 'Love me', 'The best 100 ', 'Hits']
list_years_of_issue_collection = [2018, 2019, 2020, 2021, 2017, 2018, 2020, 2019 ]


# functions:
def add_performers(list_name_performers):
    id_performer = 1
    for performer in list_name_performers:

        connection.execute(f''' INSERT INTO performers
        VALUES ('{id_performer}', '{performer}'); ''')
        id_performer += 1

    #connection.execute(''' DELETE FROM performers''')

def add_genre(list_genre):
    id_genre = 1
    for genre in list_genre:
        connection.execute(F''' INSERT INTO genre
        VALUES ('{id_genre}', '{genre}'); ''')
        id_genre += 1

def add_album(list_album):
    id_album = 1
    for album in list_album:
        connection.execute(f'''INSERT INTO album
        VALUES ('{id_album}', '{album[0]}', '{album[1]}')''')
        id_album += 1

def add_track(list_track):

    id_track = 1

    for track in list_track:
        connection.execute(f''' INSERT INTO track
        VALUES ('{id_track}', '{track[2]}', '{track[0]}', '{track[1]}')''')
        id_track += 1

def add_data_genre_and_performers():
        connection.execute(''' INSERT INTO genre_and_performers
            VALUES ('1', '1', '1');''')

        connection.execute(f''' INSERT INTO genre_and_performers
                    VALUES ('2', '2', '2');''')

        connection.execute(f''' INSERT INTO genre_and_performers
                    VALUES ('3', '3', '3');''')

        connection.execute(f''' INSERT INTO genre_and_performers
                    VALUES ('4', '4', '4');''')

        connection.execute(f''' INSERT INTO genre_and_performers
                    VALUES ('5', '5', '5');''')

        connection.execute(f''' INSERT INTO genre_and_performers
                    VALUES ('6', '1', '6');''')

        connection.execute(f''' INSERT INTO genre_and_performers
                    VALUES ('7', '2', '7');''')

        connection.execute(f''' INSERT INTO genre_and_performers
                    VALUES ('8', '3', '8');''')

        connection.execute(f''' INSERT INTO genre_and_performers
                    VALUES ('9', '4', '1');''')

        connection.execute(f''' INSERT INTO genre_and_performers
                    VALUES ('10', '5', '2');''')

        connection.execute(f''' INSERT INTO genre_and_performers
                    VALUES ('11', '1', '3');''')

        connection.execute(f''' INSERT INTO genre_and_performers
                    VALUES ('12', '2', '4');''')

def add_collections(list_name_collection,list_years_of_issue_collection):
    id_collection = 1
    for i in range(8):
        connection.execute(f'''INSERT INTO collection
            VALUES ('{id_collection}', '{list_name_collection[i]}', '{list_years_of_issue_collection[i]}' );''')
        id_collection += 1

def add_data_collection_track():

    connection.execute(''' INSERT INTO collection_track
                        VALUES ('1', '1', '1');
                        ''')                                                  # YEAR_OF_ISSUE = 2018    1, 9, 6, 14

    connection.execute(''' INSERT INTO collection_track
                            VALUES ('2', '1', '9');
                            ''')

    connection.execute(''' INSERT INTO collection_track
                            VALUES ('3', '1', '6');
                            ''')



    connection.execute(''' INSERT INTO collection_track
                            VALUES ('4', '2', '2');
                            ''')                                                # 2019     2, 10, 16, 8,

    connection.execute(''' INSERT INTO collection_track
                            VALUES ('5', '2', '10');
                            ''')

    connection.execute(''' INSERT INTO collection_track
                            VALUES ('6', '2', '16');
                            ''')




    connection.execute(''' INSERT INTO collection_track
                            VALUES ('7', '3', '11');
                            ''')                                        # 2020          3,    11, 7, 15,

    connection.execute(''' INSERT INTO collection_track
                            VALUES ('8', '3', '3');
                            ''')

    connection.execute(''' INSERT INTO collection_track
                            VALUES ('9', '3', '7');
                            ''')






    connection.execute(''' INSERT INTO collection_track
                            VALUES ('10', '4', '4');
                            ''')                                          #2021        4, 12

    connection.execute(''' INSERT INTO collection_track
                            VALUES ('11', '4', '12');
                            ''')

    connection.execute(''' INSERT INTO collection_track
                            VALUES ('12', '4', '15');
                            ''')




    connection.execute(''' INSERT INTO collection_track
                            VALUES ('13', '5', '5');
                            ''')                                          #2017             5, 13

    connection.execute(''' INSERT INTO collection_track
                            VALUES ('14', '5', '13');
                            ''')



    connection.execute(''' INSERT INTO collection_track
                            VALUES ('15', '6', '5');
                            ''')                                       # 2018

    connection.execute(''' INSERT INTO collection_track
                            VALUES ('16', '6', '14');
                            ''')

    connection.execute(''' INSERT INTO collection_track
                            VALUES ('17', '6', '6');
                            ''')





    connection.execute(''' INSERT INTO collection_track
                            VALUES ('18', '7', '11');
                            ''')                                      #2020

    connection.execute(''' INSERT INTO collection_track
                            VALUES ('19', '7', '7');
                            ''')

    connection.execute(''' INSERT INTO collection_track
                            VALUES ('20', '7', '14');
                            ''')


    connection.execute(''' INSERT INTO collection_track
                            VALUES ('21', '8', '16');
                            ''')                                      #2019

    connection.execute(''' INSERT INTO collection_track
                            VALUES ('22', '8', '13');
                            ''')

    connection.execute(''' INSERT INTO collection_track
                            VALUES ('23', '8', '9');
                            ''')

def add_data_album_and_performers():

    for i in range(1,9):
        connection.execute(f'''INSERT INTO album_and_performers
                        VALUES ('{i}', '{i}', '{i}');
                        ''')






add_performers(list_name_performers)
add_genre(list_genre)
add_album(list_album)
add_track(list_track)
add_data_genre_and_performers()
add_collections(list_name_collection,list_years_of_issue_collection)
add_data_collection_track()
add_data_album_and_performers()




