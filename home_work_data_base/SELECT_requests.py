import sqlalchemy
from pprint import pprint


db = 'postgresql://radif:1111@localhost:5432/test_db'

engine = sqlalchemy.create_engine(db)

connection = engine.connect()


#1)
# result = connection.execute(''' SELECT name, year_of_issue FROM album
#                                     WHERE year_of_issue = 2018;''').fetchall()
# print(result)

#2
# result = connection.execute(''' SELECT name, duration FROM track
# ORDER BY duration DESC
# LIMIT 1
# ;''').fetchall()

#pprint(result)

#3
# result = connection.execute(''' SELECT name, duration FROM track
# WHERE duration >= 3.5 ;''').fetchall()
#
# pprint(result)

#4
# result = connection.execute(''' SELECT name, year_of_issue FROM collection
# WHERE year_of_issue BETWEEN 2018 AND 2020 ;''').fetchall()
#
# pprint(result)

#5
# result = connection.execute(''' SELECT name_or_pseudonym FROM performers
# WHERE name_or_pseudonym NOT LIKE  '%% %%';''').fetchall()
#
# pprint(result)

#6
# result = connection.execute('''SELECT name FROM track
# WHERE name ILIKE '%%my%%' ;''').fetchall()
#
# print(result)


# Продолжение ДЗ

# table = connection.execute(''' SELECT * FROM track;''')
# pprint(list(table))


# table = connection.execute(''' SELECT duration FROM track;''')
# pprint(list(table))