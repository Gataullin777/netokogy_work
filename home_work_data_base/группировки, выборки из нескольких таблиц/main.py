import sqlalchemy
from pprint import pprint


db = ''
engine = sqlalchemy.create_engine(db)
con = engine.connect()



# ### ЗАДАЧА 1
# data = con.execute('''SELECT * FROM genre;''')
# data = list(data)
#
# for i in data:
#     count = con.execute(f'''SELECT COUNT(id_genre) FROM genre_and_performers
#                     WHERE id_genre = {i[0]}''')
#     count = list(count)[0]
#     count = count[0]
#
#     #print(count)
#     print(f'исполнители в жанре {i[1]} = {count}')


### ЗАДАЧА 2
# data = con.execute('''SELECT * FROM album
#                         WHERE year_of_issue BETWEEN 2019 AND 2020;''')
# data = list(data)
# #pprint(data)
#
#
# # data = con.execute('''SELECT * FROM track;''')
# # data = list(data)
# # pprint(data)
# count_track = 0
# for i in data:
#     track =  con.execute(f'''SELECT * FROM track
#                             WHERE id_album = {i[0]} ''')
#     count_track += len(list(track))
#
#
# print(count_track)


##### ЗАДАЧА 3

# data = con.execute('''SELECT * FROM album;''')
#
# data = list(data)
#
# for i in data:
#
#     average_duration = con.execute(f'''SELECT AVG(duration) FROM track
#                                         WHERE id_album = {i[0]};''')
#     average_duration = list(average_duration)[0][0]
#
#     print(f'в альбоме {i[1]} продолжительность все треков составляет : {average_duration}')
#
#

###### ЗАДАЧА 4

# id_data_album = con.execute('''SELECT id FROM album
#                              WHERE NOT year_of_issue = 2020;''')
#
# id_data_album = list(id_data_album)
# #pprint(id_data_album)
#
# for i in id_data_album:
#     #print(i[0])
#     id_performers = con.execute(f'''SELECT id_performers FROM album_and_performers
#                                         WHERE id_album = {i[0]} ;''')
#     id_performers = list(id_performers)
#     # print(id_performers[0][0])
#     for i in id_performers:
#         #print(i[0])
#         performers = con.execute(f'''SELECT name_or_pseudonym FROM performers
#                                     WHERE id = {i[0]};''')
#         performers = list(performers)
#         print(f'Исполнитель песен {performers[0][0]} не выпустил альбом в 2020 году')


#### ЗАДАЧА 5
### ИСПОЛНИТЕЛЬ  Eminem


#
# id_track_Eminem =  con.execute('''SELECT id FROM track
#                             WHERE id_album = (SELECT id_album FROM album_and_performers
#                                     WHERE id_performers = (SELECT id FROM performers
#                                                             WHERE name_or_pseudonym ILIKE '%%eminem%%'))''')
# id_track_Eminem = list(id_track_Eminem)
# # print('номера треков Эминема')
# # print(id_track_Eminem)
# # print()
#
# list_id_collection_Eminem = []
# for i in id_track_Eminem:
#     id_collection = con.execute(f'''SELECT id_collection FROM collection_track
#                                     WHERE id_track = {i[0]}  ;''')
#
#     id_collection = list(id_collection)[0][0]
#     list_id_collection_Eminem.append(id_collection)
#     #print(id_collection)
#
#
# #print(list_id_collection_Eminem)
# list_temp = []
# for i in list_id_collection_Eminem:
#     name_collection_Eminem = con.execute(f'''SELECT name FROM collection
#                                                 WHERE id = {i}''')
#     name_collection_Eminem = list(name_collection_Eminem)[0][0]
#
#
#     if name_collection_Eminem in list_temp:
#         continue
#
#     else:
#         print(f'Eminem исполняет в сборнике {name_collection_Eminem}')
#         list_temp.append(name_collection_Eminem)
#
#


###### ЗАДАЧА 6

# all_id_performers = con.execute('''SELECT id FROM performers;''')
# all_id_performers = list(all_id_performers)
# #print(all_id_performers)
#
# performers_two_genre = []
# for i in all_id_performers:
#
#     data = con.execute(f'''SELECT id_genre FROM genre_and_performers
#                             WHERE id_performers = {i[0]};''')
#     data = list(data)
#
#     if len(data) >= 2:
#         performers_two_genre.append(i[0])
#     else:
#         continue
#
# #print(performers_two_genre)
#
# for i in performers_two_genre:
#     name_album = con.execute(f'''SELECT name FROM album
#                                     WHERE id = (SELECT id_album FROM album_and_performers
#                                                     WHERE id_performers = {i}) ;''')
#
#     name_album = list(name_album)[0][0]
#     print(f'альбом, в котором присутствует исполнитель более 1 го жанра : {name_album}')

#
#### ДОБАВИЛ 17 ЫЙ ТРЕК, ,БЫЛО  16
##lenght_id = con.execute('''SELECT id FROM track;''')
##lenght_id = len(list(lenght_id))
##print(lenght_id)
#
##con.execute(f''' INSERT INTO track
##                VALUES ({lenght_id + 1}, 8, 'LA LA LA' , 3.19);''')
#



####### ЗАДАНИЕ 7
# tracks_list = []
# tracks = con.execute('''SELECT id FROM track;''')
# tracks = list(tracks)
# for i in tracks:
#     tracks_list.append(i[0])
#
# #pprint(tracks_list)
#
# id_track_of_the_collection_list = []
# id_track_of_the_collection = con.execute('''SELECT id_track FROM collection_track;''')
# id_track_of_the_collection = list(id_track_of_the_collection)
# for i in id_track_of_the_collection:
#     id_track_of_the_collection_list.append(i[0])
#
# #pprint(id_track_of_the_collection_list)
#
# id_track_list = []
# for i in tracks_list:
#     if i in id_track_of_the_collection_list:
#         continue
#
#     else:
#         id_track_list.append(i)
#
# #print(id_track_list)
#
# for i in id_track_list:
#     name_track = con.execute(f'''SELECT name FROM track
#                                 WHERE id = {i};''')
#     name_track = list(name_track)[0][0]
#     print(f'наименование трека, который не вошёл в сборники : {name_track}')
#
#

###### ЗАДАНИЕ 8
#
# min_lengt_track = con.execute(''' SELECT id FROM track
#                             WHERE duration = (SELECT MIN(duration) FROM track) ;''')
# min_lengt_track = list(min_lengt_track)
# pprint(f'список id самых коротких треков {min_lengt_track}')
#
# for i in min_lengt_track:
#     performer = con.execute(f''' SELECT name_or_pseudonym FROM performers
#                                 WHERE id = (SELECT id_performers FROM album_and_performers
#                                                 WHERE id_album = (SELECT id_album FROM track
#                                                                     WHERE id = {i[0]}));''')
#     performer = list(performer)[0][0]
#     pprint(f'самые короткие треки у испольнителей : {performer}')


###### ЗАДАНИЕ 9
#
# album = con.execute('''SELECT id_album, COUNT(id) FROM track
#                         GROUP BY id_album
#                         ORDER BY id_album ;''')
# album = list(album)
# #pprint(album)
#
# print(f'у нас в списке {len(album)} альбомов ')
#
# #test_album = [(1, 4), (2, 5), (3, 2), (4, 6), (5, 9), (6, 2), (7, 2), (8, 3)]
# id_min_lenght_album = []
# iter = album[0][1]
# #print(iter)
# for i in album:
#     if i[1] == iter:
#         id_min_lenght_album.append(i[0])
#
#     elif i[1] < iter:
#         iter = i[1]
#         id_min_lenght_album.clear()
#         id_min_lenght_album.append(i[0])
#
#     else:
#         continue
#
# if len(id_min_lenght_album) == 1:
#     album = con.execute(f'''SELECT name FROM album
#                                 WHERE id = {id_min_lenght_album[0]}''')
#     album = list(album)[0][0]
#     print(f' самый малый по количеству треков является альбом : {album}')
#
#
#
#
# else:
#     #print(id_min_lenght_album)
#     print(f'из всех {len(album)} альбомов, по количеству треков самые меньшие {len(id_min_lenght_album)} альбома :  ')
#
#     for i in id_min_lenght_album:
#         album = con.execute(f'''SELECT name FROM album
#                                     WHERE id = {i}''')
#         album = list(album)[0][0]
#         print(album)
#
#     print(f'у всех по {iter} трека ')
#
#
























