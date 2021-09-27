from random import randint
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from pprint import pprint
import database as db_vk


token_group = '1b5021e6d18ac8993a692749443ef83e1371f849b652fe5cab0dd5a3298cd649bf41ef3ce1f296559615b'
id_group = 206818303
token_user = '8a8d4d2e656257c1c60467984487ee444e58c1ad7f561578ef64e0ab271f65b7d00990cca85e8e07971a5'

class Vkinder_bot():

    def __init__(self, token_group, id_group, token_user):
        self.token_user = token_user
        self.token_group = token_group
        self.id_group = id_group

    def send_message(self, user_id, message):
         self.vk.method('messages.send',
                  {'user_id': user_id, 'message': message, 'random_id': randint(1, 2147483647)})

    def get_info_users(self, user_id):
        '''
        :param user_id: int
        :return: dictionary with information
        '''
        #user_id = randint(4, 1000000)
        response = self.vk.method('users.get',
                   {'user_ids': user_id, 'fields': 'sex, relation, contacts, bdate, city, photo_max_orig '})
        print(response)
        return response

    def setting_data(self, id_first_user, user_id):
        '''
        :param id_first_user:  id пользователя, кому хотим найти пару
        :param user_id: id текущего пользователя
        :return: Словарь с данными пользователя кому хотим найти пару
        '''
        data_user_dict = {}
        info_first_user = self.get_info_users(id_first_user)[0]  # dictionary

        data_user_dict['name'] = info_first_user['first_name']

        if info_first_user.get('sex') == None:
            self.send_message(user_id, '''Какого пола вы ищете человека? \n '
                                            'если это мужщина введите - 2 \n '
                                            'если это женщина введите - 1''')
            message_text = self.longpooling()['message']['text']
            try:
                sex = int(message_text)
                data_user_dict['sex'] = sex
            except:
                self.send_message(user_id, 'Ошибка при определении пола, начните заново!!!')
        else:
            data_user_dict['sex'] = info_first_user.get('sex')

        if info_first_user.get('relation') == None or info_first_user.get('relation') == 0:
            self.send_message(user_id, '''Укажите семейное положение. Возможные значения:\n 
                                            1 — не женат (не замужем);\n
                                            2 — встречается;\n
                                            3 — помолвлен(-а);\n
                                            4 — женат (замужем);\n
                                            5 — всё сложно;\n
                                            6 — в активном поиске;\n
                                            7 — влюблен(-а);\n
                                            8 — в гражданском браке.''')
            message_text = self.longpooling()['message']['text']
            try:
                relation = int(message_text)
                data_user_dict['relation'] = relation
            except:
                self.send_message(user_id, 'Ошибка при определении семейного положения, начните заново!!!')
        else:
            data_user_dict['relation'] = info_first_user.get('relation')

        if info_first_user.get('city') == None or info_first_user['city']['title'] == None:
            self.send_message(user_id, '''Я не смог определить в каком городе живет пользователь, введите название города.''')
            message_text = self.longpooling()['message']['text']
            try:
                city_name = message_text
                id_city = self.id_city(city_name)
                data_user_dict['city'] = id_city
            except:
                self.send_message(user_id, 'Ошибка при определении города, начните заново!!!')
        else:
            data_user_dict['city'] = info_first_user['city']['id']

        if info_first_user.get('bdate') == None or len(info_first_user.get('bdate')) < 6:
            self.send_message(user_id,
                              '''Я не смог определить в возраст пользователя, введите пожалуйста его возраст.''')
            message_text = self.longpooling()['message']['text']
            try:
                age = message_text
                data_user_dict['age'] = int(age)
            except:
                self.send_message(user_id, 'Ошибка при определении возраста пользователя, начните заново!!!')
        else:
            year_brith_user = info_first_user['bdate'].split('.')[-1]
            year_brith_user = int(year_brith_user)
            age_user = 2021 - year_brith_user
            data_user_dict['age'] = age_user

        print(data_user_dict) # словарь наполняется правильно, можно приступать к след. шагу

        return data_user_dict

    def finding_a_half(self, user_id):
        self.send_message(user_id, 'Введите id пользователя')
        message_text = self.longpooling()['message']['text']

        try:
            id_first_user = int(message_text)  # если пользователь введет слово или дробное число, отправиться сообщение
            # об ошибке
            if id_first_user:
                self.send_message(user_id, 'Запускаю программу сбора данных')
                data_user_dict = self.setting_data(id_first_user, user_id)
                data_searched_user = self.user_search(data_user_dict)
                id_searched_user = data_searched_user['id']
                links_photo_list = self.get_links_photo(id_searched_user)
                self.send_message(user_id, f'Для пользователя {data_user_dict["name"]}\n'
                                f'я нашел пару: {data_searched_user["first_name"]} {data_searched_user["last_name"]}\n'
                                           f'Вот ссылки на полулярные фото:\n'
                                           f'{links_photo_list[0]}\n'
                                           f'{links_photo_list[1]}\n'
                                           f'{links_photo_list[2]}\n'
                                  f' id страницы vk.com/id{id_searched_user}')
            else:
                self.send_message(user_id, 'что то пошло не так!!! начните заново')
        except Exception as e:
            print(e)
            self.send_message(user_id, 'ошибка, что то пошло не так!!! начните заново')

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
                'count': 1,
                'fields': 'id',
                'sex': sex,
                'age_from': data_user_dict['age'] - 4,
                'age_to': data_user_dict['age'] + 4,
                'city': data_user_dict['city'],
                'status': 6,
                'v': 5.131
            }
        )

        pprint(users)
        print(users['items'][0]['id'])
        return users['items'][0]

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

        # pprint(photos_list)

        data_dict = {}
        count_likes_comments_list = []

        for i in photos_list:
            print('++++++++++++++++++++')
            print(f'count comments - {i["comments"]["count"]}, count likes - {i["likes"]["count"]}')
            number = i["comments"]["count"] + i["likes"]["count"]
            data_dict[f'{number}'] = i['sizes'][-1]
            count_likes_comments_list.append(number)

        pprint(data_dict)
        print(len(count_likes_comments_list))
        count_likes_comments_list = list(set(count_likes_comments_list))
        print(len(count_likes_comments_list))
        count_likes_comments_list_sorted = sorted(count_likes_comments_list)
        print(count_likes_comments_list_sorted)
        print(count_likes_comments_list_sorted[-3:])

        links_top_3_photo_list = []
        for i in count_likes_comments_list_sorted[-3:]:
            link_photo = data_dict[f'{i}']['url']
            links_top_3_photo_list.append(link_photo)

        print(links_top_3_photo_list)
        return links_top_3_photo_list

    def id_city(self, city_name):
        vk = vk_api.VkApi(token=self.token_user)

        countries_id = vk.method('database.getCountries',
                                 {
                                     'code': 'RU'
                                 })
        countries_id = countries_id['items'][0]['id']
        #print(countries_id)

        id_city = vk.method('database.getCities',
                            {
                                'q': f'{city_name}',
                                'country_id': countries_id,
                                'count': 1
                            })
        id_city = id_city['items'][0]['id']
        #print(id_city)
        return id_city

    def longpooling(self):
        self.vk = vk_api.VkApi(token=self.token_group)  # авторизация
        longpoll = VkBotLongPoll(self.vk, self.id_group)  # подключение longpoll
        print("Бот запущен")  # Пишем в консоль чтобы понять запущен ли бот.

        for event in longpoll.listen():  # прослушиваем все сообщения

            # Если пришло новое сообщение
            if event.type == VkBotEventType.MESSAGE_NEW:
                mess = event.obj['message']['text']  # преобразуем текст сообщения в переменную
                peer_id = event.obj['message']['peer_id']

                return event.obj

    def start(self):
        while True:
            event_obj = self.longpooling()

            mess = event_obj['message']['text']  # преобразуем текст сообщения в переменную
            current_user_id = event_obj['message']['peer_id']

            if mess.lower() == "привет":  # если текст сообщения = Привет!, отправляем сообщение.
                self.send_message(current_user_id, "Приветствую вас, меня зовут Сэм, я ваш личный помощник,\n"
                           "я могу найти вторую половику человеку по его id,\n"
                           "для этого напишите мне команду : 'Найти половину'" )


            elif mess.lower() == 'найти половину':
                self.finding_a_half(current_user_id)


            elif mess.lower() == 'расскажи про меня':
                user_info_list = self.get_info_users(current_user_id)
                message = f' Вас зовут {user_info_list[0]["first_name"]}\n' \
                          f'Ваша фамиия {user_info_list[0]["last_name"]}'

                self.send_message(current_user_id, message)

            else:
                self.send_message(current_user_id, 'Я не могу понять что вы хотите!')

