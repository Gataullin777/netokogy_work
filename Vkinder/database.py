import sqlalchemy
from access import db_access

db = db_access
engine = sqlalchemy.create_engine(db)
con = engine.connect()

# #create table vk_user_info
# data = con.execute('''create table if not exists vk_user_info (
#                     id integer primary key);
#                     ''')
#

def pull_id():
    '''
    take all id from the database and create a list
    :return: sorted list id
    '''

    users_id_list = con.execute(f'''SELECT id FROM vk_user_info''')
    users_id_list = list(users_id_list)  # list of corteges
    list_id = []
    for i in users_id_list:
        # print(i)
        list_id.append(i[0])

    list_id.sort()
    # print(list_ids)
    return list_id

def add_data_of_the_table(user_id):
    '''
    add user id of the table vk_user_info in the database
    :param user_id: int
    :return: None
    '''
    con.execute(f'''INSERT INTO vk_user_info(id)
                    VALUES({user_id});''')


