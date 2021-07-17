import sqlalchemy
from pprint import pprint


db = ''
engine = sqlalchemy.create_engine(db)
con = engine.connect()

### ЗАДАЧА 1
# data = con.execute('''SELECT name, COUNT(genre_and_performers.id_performers) FROM genre
#                             LEFT JOIN genre_and_performers ON genre.id = genre_and_performers.id_genre
#                             GROUP BY name ;''')
# data = list(data)
# pprint(data)



### ЗАДАЧА 2

# data = con.execute('''SELECT COUNT(track.id) FROM track
#                         LEFT JOIN album ON track.id_album = album.id
#                          WHERE year_of_issue BETWEEN 2019 AND 2020 ;''')
#
# data = list(data)
# pprint(data)

##### ЗАДАЧА 3

# data = con.execute('''SELECT album.name, AVG(duration) FROM album
#                         LEFT JOIN track ON album.id = track.id_album
#                         GROUP BY album.name
#                         ORDER BY AVG(duration) ;''')
# data = list(data)
# pprint(data)

###### ЗАДАЧА 4

# data = con.execute('''SELECT p.name_or_pseudonym FROM performers p
#                         LEFT JOIN album_and_performers ap ON p.id = ap.id_performers
#                         LEFT JOIN album a ON ap.id_album = a.id
#                         WHERE NOT a.year_of_issue = 2020; ''')
# data = list(data)
# pprint(data)

#### ЗАДАЧА 5
### ИСПОЛНИТЕЛЬ  Eminem

#data = con.execute('''SELECT DISTINCT c.name FROM collection c
#                         LEFT JOIN collection_track ct ON c.id = ct.id_collection
#                         LEFT JOIN track t ON ct.id_track = t.id
#                         LEFT JOIN album a ON t.id_album = a.id
#                         LEFT JOIN album_and_performers ap ON a.id = ap.id_album
#                         LEFT JOIN performers p ON ap.id_performers = p.id
#                         WHERE p.name_or_pseudonym LIKE '%%Eminem%%'; ''')
# data = list(data)
# pprint(data)


###### ЗАДАЧА 6

# data = con.execute('''SELECT a.name FROM album a
#                         LEFT JOIN album_and_performers ap ON a.id = ap.id_album
#                         LEFT JOIN performers p ON ap.id_performers = p.id
#                         LEFT JOIN genre_and_performers gp ON p.id = gp.id_performers
#                         LEFT JOIN genre g ON gp.id_genre = g.id
#                         GROUP BY a.name
#                         HAVING COUNT(gp.id_genre) > 1;''')
#
# data = list(data)
# pprint(data)


####### ЗАДАНИЕ 7

# data = con.execute('''SELECT t.name FROM collection_track ct
#                     RIGHT JOIN track t ON ct.id_track = t.id
#                     WHERE ct IS NULL;''')
#
# data = list(data)
# pprint(data)

##### ЗАДАНИЕ 8

# data = con.execute('''SELECT p.name_or_pseudonym ,MIN(t.duration) FROM track t
#                         LEFT JOIN album a ON t.id_album = a.id
#                         LEFT JOIN album_and_performers ap ON a.id = ap.id_album
#                         LEFT JOIN performers p ON ap.id_performers = p.id
#                         WHERE duration IN (SELECT MIN(duration) FROM track)
#                                             GROUP BY p.name_or_pseudonym
#                                             ORDER BY MIN(t.duration);''')
# data = list(data)
# pprint(data)


###### ЗАДАНИЕ 9

# data = con.execute('''SELECT a.name, COUNT(*) FROM album a
#                     LEFT JOIN track t ON  a.id = t.id_album
#                     GROUP BY a.name
#                     HAVING COUNT(t.id) IN (SELECT COUNT(t.id) FROM track t
#                                             GROUP BY t.id_album
#                                             ORDER BY COUNT(t.id)
#                                             LIMIT 1)
#                     ;''')
#
#
# data = list(data)
# pprint(data)
#




















