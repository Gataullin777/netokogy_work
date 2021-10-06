from random import randint
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from pprint import pprint

import access
import database as db_vk

class Bot:
    '''
    Main class for methods bot
    '''

    id_group = access.id_group
    token_user = access.token_user
    token_group = access.token_group
    def __init__(self):
        self.vk_group = vk_api.VkApi(token=self.token_group)
        self.vk_user = vk_api.VkApi(token=self.token_user)

    def longpooling(self):
        # self.vk = vk_api.VkApi(token=self.token_group)  # авторизация
        longpoll = VkBotLongPoll(self.vk_group, self.id_group)  # подключение longpoll
        print("Бот запущен")  # Пишем в консоль чтобы понять запущен ли бот.

        for event in longpoll.listen():  # прослушиваем все сообщения

            # Если пришло новое сообщение
            if event.type == VkBotEventType.MESSAGE_NEW:
                mess = event.obj['message']['text']  # преобразуем текст сообщения в переменную
                peer_id = event.obj['message']['peer_id']

                return event.obj

class vk_user(Bot):
    '''
    This class uses methods with a user token
    '''

    def user_search(self, data_user_dict):

        vk = vk_api.VkApi(token=self.token_user)

        if data_user_dict['sex'] == 1:
            sex = 2
        elif data_user_dict['sex'] == 2:
            sex = 1
        else:
            sex = 0

        users = vk.method(
            'users.search',
            {
                'q': None,
                'count': 1000,
                'fields': 'id, is_closed',
                'sex': sex,
                'age_from': data_user_dict['age'] - 4,
                'age_to': data_user_dict['age'] + 4,
                'city': data_user_dict['city'],
                'status': 6,
                'v': 5.131,
                'is_closed': False
            }
        )

        # checking searced user in the database
        list_id_from_database = db_vk.pull_id()

        for i in users['items']:
            if i['id'] in list_id_from_database or i['is_closed'] is True:
                continue

            else:
                return i

    def get_links_photo(self, user_id):
        '''
        counting likes and comments photo profile vk.com
        :param user_id: id user from vk.com
        :return: links on top 3 popular photo from profile user vk.com, type list
        '''

        vk = vk_api.VkApi(token=self.token_user)
        photos_dict = vk.method(
            'photos.get',
            {
                'owner_id': user_id,
                'album_id': 'profile',
                'rev': 0,
                'extended': 1,
                'count': 200,
                'photo_sizes': 0

            }
        )

        photos_list = photos_dict['items']

        data_dict = {}
        count_likes_comments_list = []

        for i in photos_list:
            number = i["comments"]["count"] + i["likes"]["count"]
            data_dict[f'{number}'] = i['sizes'][-1]
            count_likes_comments_list.append(number)

        count_likes_comments_list = list(set(count_likes_comments_list))
        count_likes_comments_list_sorted = sorted(count_likes_comments_list)

        links_top_3_photo_list = []
        for i in count_likes_comments_list_sorted[-3:]:
            link_photo = data_dict[f'{i}']['url']
            links_top_3_photo_list.append(link_photo)

        return links_top_3_photo_list

    def get_id_city(self, city_name):

        vk = vk_api.VkApi(token=self.token_user)

        countries_id = vk.method('database.getCountries',
                                 {
                                     'code': 'RU'
                                 })

        countries_id = countries_id['items'][0]['id']

        id_city = vk.method('database.getCities',
                            {
                                'q': f'{city_name}',
                                'country_id': countries_id,
                                'count': 1
                            })
        id_city = id_city['items'][0]['id']

        return id_city

class vk_group(Bot):
    '''
        This class uses methods with a group token
    '''

    def send_message(self, user_id, message):
        self.vk_group.method('messages.send',
                       {'user_id': user_id, 'message': message, 'random_id': randint(1, 2147483647)})

    def get_info_users(self, user_id):
        '''
        :param user_id: int
        :return: dictionary with information
        '''

        response = self.vk_group.method('users.get',
                   {'user_ids': user_id, 'fields': 'sex, relation, contacts, bdate, city, photo_max_orig '})

        return response

    def setting_data(self, id_target_user, current_user_id):
        '''
        :param id_target_user:  id пользователя, кому хотим найти пару
        :param current_user_id: id текущего пользователя
        :return: Словарь с данными пользователя кому хотим найти пару
        '''
        data_target_user_dict = {}  # create new empty dictionary
        info_search_user_dict = self.get_info_users(id_target_user)[0]

        data_target_user_dict['name'] = info_search_user_dict['first_name']

        if info_search_user_dict.get('sex') == None:
            self.send_message(current_user_id, '''Какого пола вы ищете человека? \n '
                                            'если это мужщина введите - 2 \n '
                                            'если это женщина введите - 1''')
            message_text = self.longpooling()['message']['text']
            try:
                sex = int(message_text)
                data_target_user_dict['sex'] = sex
            except:
                self.send_message(current_user_id, 'Ошибка при определении пола, начните заново!!!')
        else:
            data_target_user_dict['sex'] = info_search_user_dict.get('sex')



        if info_search_user_dict.get('city') == None or info_search_user_dict['city']['title'] == None:
            self.send_message(current_user_id, f'''Я не смог определить в каком городе живет {data_target_user_dict['name']}, введите название города.''')
            message_text = self.longpooling()['message']['text']
            try:
                city_name = message_text
                id_city = vk_user().get_id_city(city_name)
                data_target_user_dict['city'] = id_city
            except:
                self.send_message(current_user_id, 'Ошибка при определении города, начните заново!!!')
        else:
            data_target_user_dict['city'] = info_search_user_dict['city']['id']

        if info_search_user_dict.get('bdate') == None or len(info_search_user_dict.get('bdate')) < 6:
            self.send_message(current_user_id,
                              f'''Я не смог определить в возраст {data_target_user_dict['name']} введите пожалуйста  возраст.''')
            message_text = self.longpooling()['message']['text']
            try:
                age = message_text
                data_target_user_dict['age'] = int(age)
            except:
                self.send_message(current_user_id, 'Ошибка при определении возраста пользователя, начните заново!!!')
        else:
            year_brith_user = info_search_user_dict['bdate'].split('.')[-1]
            year_brith_user = int(year_brith_user)
            age_user = 2021 - year_brith_user
            data_target_user_dict['age'] = age_user

        data_target_user_dict['relation'] = 6

        return data_target_user_dict

    def finding_a_half(self, current_user_id):
        self.send_message(current_user_id, 'Введите id пользователя кому хотите найти половинку')
        message_text = self.longpooling()['message']['text']

        try:
            id_first_user = int(message_text)  # если пользователь введет слово или дробное число, отправиться сообщение
            # об ошибке

            self.send_message(current_user_id, 'Начинаю сбор данных')
            data_target_user_dict = self.setting_data(id_first_user, current_user_id)
            data_searched_user = vk_user().user_search(data_target_user_dict)
            id_searched_user = data_searched_user['id']
            links_photo_list = vk_user().get_links_photo(id_searched_user)
            self.send_message(current_user_id, f'Для пользователя {data_target_user_dict["name"]}\n'
                                f'я нашел пару: {data_searched_user["first_name"]} {data_searched_user["last_name"]}\n'
                                f' id страницы vk.com/id{id_searched_user}')

            # send message link photos, maximum 3
            for i in links_photo_list:
                self.send_message(current_user_id, i)

            # add searced user id of the database
            db_vk.add_data_of_the_table(id_searched_user)

        except Exception as e:
            print(e)
            self.send_message(current_user_id, 'ошибка, что то пошло не так!!! начните заново')

class Vkinder(Bot):
    # def __init__(self):
    #     self.vk_group = vk_group()
    #     self.vk_user = vk_user()
    # # def send_message(self, user_id, message):
    # #      self.vk_group.method('messages.send',
    # #               {'user_id': user_id, 'message': message, 'random_id': randint(1, 2147483647)})
    #
    # # def get_info_users(self, user_id):
    # #     '''
    # #     :param user_id: int
    # #     :return: dictionary with information
    # #     '''
    # #
    # #     response = self.vk_group.method('users.get',
    # #                {'user_ids': user_id, 'fields': 'sex, relation, contacts, bdate, city, photo_max_orig '})
    # #     print(response)
    # #     return response
    #
    # # def setting_data(self, id_search_user, current_user_id):
    # #     '''
    # #     :param id_first_user:  id пользователя, кому хотим найти пару
    # #     :param current_user_id: id текущего пользователя
    # #     :return: Словарь с данными пользователя кому хотим найти пару
    # #     '''
    # #     data_user_dict = {}
    # #     info_search_user = self.get_info_users(id_search_user)[0]  # dictionary
    # #
    # #     data_user_dict['name'] = info_search_user['first_name']
    # #
    # #     if info_search_user.get('sex') == None:
    # #         self.send_message(current_user_id, '''Какого пола вы ищете человека? \n '
    # #                                         'если это мужщина введите - 2 \n '
    # #                                         'если это женщина введите - 1''')
    # #         message_text = self.longpooling()['message']['text']
    # #         try:
    # #             sex = int(message_text)
    # #             data_user_dict['sex'] = sex
    # #         except:
    # #             self.send_message(current_user_id, 'Ошибка при определении пола, начните заново!!!')
    # #     else:
    # #         data_user_dict['sex'] = info_search_user.get('sex')
    # #
    # #
    # #
    # #     if info_search_user.get('city') == None or info_search_user['city']['title'] == None:
    # #         self.send_message(current_user_id, '''Я не смог определить в каком городе живет пользователь, введите название города.''')
    # #         message_text = self.longpooling()['message']['text']
    # #         try:
    # #             city_name = message_text
    # #             id_city = self.get_id_city(city_name)
    # #             data_user_dict['city'] = id_city
    # #         except:
    # #             self.send_message(current_user_id, 'Ошибка при определении города, начните заново!!!')
    # #     else:
    # #         data_user_dict['city'] = info_search_user['city']['id']
    # #
    # #     if info_search_user.get('bdate') == None or len(info_search_user.get('bdate')) < 6:
    # #         self.send_message(current_user_id,
    # #                           '''Я не смог определить в возраст пользователя, введите пожалуйста его возраст.''')
    # #         message_text = self.longpooling()['message']['text']
    # #         try:
    # #             age = message_text
    # #             data_user_dict['age'] = int(age)
    # #         except:
    # #             self.send_message(current_user_id, 'Ошибка при определении возраста пользователя, начните заново!!!')
    # #     else:
    # #         year_brith_user = info_search_user['bdate'].split('.')[-1]
    # #         year_brith_user = int(year_brith_user)
    # #         age_user = 2021 - year_brith_user
    # #         data_user_dict['age'] = age_user
    # #
    # #     data_user_dict['relation'] = 6
    # #     print(data_user_dict) # словарь наполняется правильно, можно приступать к след. шагу
    # #
    # #     return data_user_dict
    #
    # # def finding_a_half(self, user_id):
    # #     self.send_message(user_id, 'Введите id пользователя')
    # #     message_text = self.longpooling()['message']['text']
    # #
    # #     try:
    # #         id_first_user = int(message_text)  # если пользователь введет слово или дробное число, отправиться сообщение
    # #         # об ошибке
    # #
    # #         self.send_message(user_id, 'Запускаю программу сбора данных')
    # #         data_user_dict = self.setting_data(id_first_user, user_id)
    # #         data_searched_user = self.user_search(data_user_dict)
    # #         id_searched_user = data_searched_user['id']
    # #         links_photo_list = self.get_links_photo(id_searched_user)
    # #         self.send_message(user_id, f'Для пользователя {data_user_dict["name"]}\n'
    # #                             f'я нашел пару: {data_searched_user["first_name"]} {data_searched_user["last_name"]}\n'
    # #                             f' id страницы vk.com/id{id_searched_user}')
    # #
    # #         # send message link photos, maximum 3
    # #         for i in links_photo_list:
    # #             self.send_message(user_id, i)
    # #
    # #         # add searced user id of the database
    # #         db_vk.add_data_of_the_table(id_searched_user)
    # #
    # #     except Exception as e:
    # #         print(e)
    # #         self.send_message(user_id, 'ошибка, что то пошло не так!!! начните заново')
    #
    # # def user_search(self, data_user_dict):
    # #
    # #     vk = vk_api.VkApi(token=self.token_user)
    # #
    # #     if data_user_dict['sex'] == 1:
    # #         sex = 2
    # #     elif data_user_dict['sex'] == 2:
    # #         sex = 1
    # #     else:
    # #         sex = 0
    # #
    # #     users = vk.method(
    # #         'users.search',
    # #         {
    # #             'q': None,
    # #             'count': 1000,
    # #             'fields': 'id, is_closed' ,
    # #             'sex': sex,
    # #             'age_from': data_user_dict['age'] - 4,
    # #             'age_to': data_user_dict['age'] + 4,
    # #             'city': data_user_dict['city'],
    # #             'status': 6,
    # #             'v': 5.131,
    # #             'is_closed': False
    # #         }
    # #     )
    # #
    # #     # checking searced user in the database
    # #     list_id_from_database = db_vk.pull_id()
    # #
    # #     for i in users['items']:
    # #         if i['id'] in list_id_from_database or i['is_closed'] is True:
    # #             continue
    # #
    # #         else:
    # #             return i
    # #
    # #
    # #     # pprint(users)
    # #     # print(users['items'][0]['id'])
    # #
    # #     # return users['items'][0]
    # #
    # # def get_links_photo(self, user_id):
    # #     '''
    # #     counting likes and comments photo profile vk.com
    # #     :param user_id: id user from vk.com
    # #     :return: links on top 3 popular photo from profile user vk.com, type list
    # #     '''
    # #
    # #     vk = vk_api.VkApi(token=self.token_user)
    # #     photos_dict = vk.method(
    # #         'photos.get',
    # #         {
    # #             'owner_id': user_id,
    # #             'album_id': 'profile',
    # #             'rev': 0,
    # #             'extended': 1,
    # #             'count': 200,
    # #             'photo_sizes': 0
    # #
    # #         }
    # #     )
    # #
    # #     photos_list = photos_dict['items']
    # #
    # #     # pprint(photos_list)
    # #
    # #     data_dict = {}
    # #     count_likes_comments_list = []
    # #
    # #     for i in photos_list:
    # #         print('++++++++++++++++++++')
    # #         print(f'count comments - {i["comments"]["count"]}, count likes - {i["likes"]["count"]}')
    # #         number = i["comments"]["count"] + i["likes"]["count"]
    # #         data_dict[f'{number}'] = i['sizes'][-1]
    # #         count_likes_comments_list.append(number)
    # #
    # #     pprint(data_dict)
    # #     print(len(count_likes_comments_list))
    # #     count_likes_comments_list = list(set(count_likes_comments_list))
    # #     print(len(count_likes_comments_list))
    # #     count_likes_comments_list_sorted = sorted(count_likes_comments_list)
    # #     print(count_likes_comments_list_sorted)
    # #     print(count_likes_comments_list_sorted[-3:])
    # #
    # #     links_top_3_photo_list = []
    # #     for i in count_likes_comments_list_sorted[-3:]:
    # #         link_photo = data_dict[f'{i}']['url']
    # #         links_top_3_photo_list.append(link_photo)
    # #
    # #     print(links_top_3_photo_list)
    # #     return links_top_3_photo_list
    # #
    # # def get_id_city(self, city_name):
    # #     vk = vk_api.VkApi(token=self.token_user)
    # #
    # #     countries_id = vk.method('database.getCountries',
    # #                              {
    # #                                  'code': 'RU'
    # #                              })
    # #     countries_id = countries_id['items'][0]['id']
    # #     #print(countries_id)
    # #
    # #     id_city = vk.method('database.getCities',
    # #                         {
    # #                             'q': f'{city_name}',
    # #                             'country_id': countries_id,
    # #                             'count': 1
    # #                         })
    # #     id_city = id_city['items'][0]['id']
    # #     #print(id_city)
    # #     return id_city
    #
    # # def longpooling(self):
    # #     self.vk = vk_api.VkApi(token=self.token_group)  # авторизация
    # #     longpoll = VkBotLongPoll(self.vk, self.id_group)  # подключение longpoll
    # #     print("Бот запущен")  # Пишем в консоль чтобы понять запущен ли бот.
    # #
    # #     for event in longpoll.listen():  # прослушиваем все сообщения
    # #
    # #         # Если пришло новое сообщение
    # #         if event.type == VkBotEventType.MESSAGE_NEW:
    # #             mess = event.obj['message']['text']  # преобразуем текст сообщения в переменную
    # #             peer_id = event.obj['message']['peer_id']
    # #
    # #             return event.obj
    def start(self):
        while True:
            # event_obj = self.longpooling()
            event_obj = self.longpooling()

            mess = event_obj['message']['text']  # преобразуем текст сообщения в переменную
            current_user_id = event_obj['message']['peer_id']

            if mess.lower() == "привет":
                vk_group().send_message(current_user_id, "Приветствую вас в приложении для поиска второй половинки,\n"
                           "я могу найти вторую половинку человеку по его id вконтакте,\n"
                           "для этого напишите мне команду : 'Найти половинку'" )


            elif mess.lower() == 'найти половинку':
                vk_group().finding_a_half(current_user_id)

            else:
                vk_group().send_message(current_user_id, 'Я не могу понять что вы хотите!')

