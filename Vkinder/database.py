import sqlalchemy


db = "sefe"
engine = sqlalchemy.create_engine(db)
con = engine.connect()

##create table vk_user_info
# data = con.execute('''create table if not exists vk_user_info (
#                     id integer primary key);
#                     ''')


def pull_id(self):
        ser_id_list = con.execute(f'''SELECT id FROM vk_user_info''')
        # print(list(user_id_list)[0][0])
        user_id_list = list(user_id_list)  # list of corteges


def add_data_of_the_table(user_id):
    con.execute(f'''INSERT INTO vk_user_info(id)
                    VALUES({user_id});''')

def check_user(user_id):
    user_id_list = con.execute(f'''SELECT id FROM vk_user_info''')
    # print(list(user_id_list)[0][0])
    user_id_list = list(user_id_list)  # list of corteges


    # for i in elements:
    #     print(i[0])




# add_data_of_the_table(182527980)

check_user(353481)