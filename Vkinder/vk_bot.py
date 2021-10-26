from random import randint
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from Vkinder import settings
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
        '''
        poolling server vk.com on new message
        :return: dictionary with data
        '''
        # self.vk = vk_api.VkApi(token=self.token_group)  # авторизация
        longpoll = VkBotLongPoll(self.vk_group, self.id_group)  # подключение longpoll
        print("Бот запущен")  # Пишем в консоль чтобы понять запущен ли бот.

        for event in longpoll.listen():  # прослушиваем все сообщения

            # Если пришло новое сообщение
            if event.type == VkBotEventType.MESSAGE_NEW:
                message_chat = event.obj['message']
                return message_chat

class vk_user(Bot):
    '''
    This class uses methods with a user token
    '''

    def user_search(self, data_user_dict):
        '''
        search the information about user on preparing data the format dictionary
        :param data_user_dict: dictionary with preparing data
        :return: target user id
        '''

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

        for user_id in users['items']:
            if user_id['id'] in list_id_from_database or user_id['is_closed'] is True:
                continue

            else:
                return user_id

    def get_top_photo(self, user_id):
        '''
        counting likes and comments photo profile vk.com
        :param user_id: id user from vk.com
        :return:  top 3 popular photo from profile user vk.com, type list in list, contains owner_id photo and id photo
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

        photos_info_list = photos_dict['items']

        data_dict = {}
        count_likes_comments_list = []

        for info in photos_info_list:
            number = info["comments"]["count"] + info["likes"]["count"]
            data_dict[f'{number}'] = [info['owner_id'], info['id']]
            count_likes_comments_list.append(number)

        count_likes_comments_list = list(set(count_likes_comments_list))
        count_likes_comments_list_sorted = sorted(count_likes_comments_list)

        top_3_photo_list = []
        for rating in count_likes_comments_list_sorted[-3:]:
            id_and_owner_id_photo = data_dict[f'{rating}']
            top_3_photo_list.append(id_and_owner_id_photo)

        return top_3_photo_list

    def get_id_city(self, city_name):
        '''
        function on name city return id city with vk.com
        :param city_name:
        :return: city id with vk.com
        '''

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

    def send_message(self, user_id, message='', media=None):
        '''
        sends message user vk.com , can sends media for example : photo, video, doc  etc
        :param user_id: type int, this is id user to whom send message
        :param message: type str, text
        :param media: optional argument, if want send media given user . Example argument: '<type media><owner_id>_<id>'
        :return: None
        '''
        self.vk_group.method('messages.send',
                       {'user_id': user_id, 'message': message, 'random_id': randint(1, 2147483647), 'attachment': media})

    def get_info_users(self, user_id):
        '''
        Get information about user vk.com
        :param user_id: int
        :return: dictionary with information
        '''

        response = self.vk_group.method('users.get',
                   {'user_ids': user_id, 'fields': 'sex, relation, contacts, bdate, city, photo_max_orig '})

        return response

    def setting_data(self, id_target_user, current_user_id):
        '''
        preparing data for search

        :param id_target_user:  id target user to whom want finding a half
        :param current_user_id: id current user
        :return: dictionary on the data second half  Словарь с данными пользователя кому хотим найти пару
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
        '''
        function finding a half user on data which the return function setting_data()
        :param current_user_id: id of the current user who writes to the bot group
        :return: do not return, send a message to the current user at the end
        '''

        try:
            if settings.TEMPLATE_DATA.get('search_user_id') is None:
                self.send_message(current_user_id, 'Введите id пользователя кому хотите найти половинку')
                message_text = self.longpooling()['text']
                search_user_id = int(message_text)  # if user enter string or float type data , will error

                settings.TEMPLATE_DATA['search_user_id'] = search_user_id

            else:
                search_user_id = settings.TEMPLATE_DATA['search_user_id']


            self.send_message(current_user_id, 'Начинаю сбор данных')
            data_target_user_dict = self.setting_data(search_user_id, current_user_id)
            data_searched_user = vk_user().user_search(data_target_user_dict)
            id_searched_user = data_searched_user['id']
            top_3_photo_list = vk_user().get_top_photo(id_searched_user)
            self.send_message(current_user_id, f'Для пользователя {data_target_user_dict["name"]}\n'
                                f'я нашел пару: {data_searched_user["first_name"]} {data_searched_user["last_name"]}\n'
                                f' id страницы vk.com/id{id_searched_user}')

            # send message link photos, maximum 3
            for photo in top_3_photo_list:
                media = f'photo{photo[0]}_{photo[1]}'
                self.send_message(current_user_id, media=media)

            # add searced user id of the database
            db_vk.add_data_of_the_table(id_searched_user)

            #
            vk_group().send_message(current_user_id, "Продолжить? [да / нет]")
            message_chat = self.longpooling()

            mess = message_chat['text']  # преобразуем текст сообщения в переменную
            current_user_id = message_chat['peer_id']
            if mess.lower() == 'да':
                self.finding_a_half(current_user_id)

            elif mess.lower() == 'нет':
                settings.TEMPLATE_DATA['search_user_id'] = None
                Vkinder().start()
            else:
                vk_group().send_message(current_user_id, "Увы я не зна такую команду!\n"
                                                         "Можете попросить меня найти половинку\n"
                                                         "для этого напишите мне [найти половинку]")


        except Exception as e:
            print(e)
            self.send_message(current_user_id, 'ошибка, что то пошло не так!!! начните заново')

class Vkinder(Bot):
    '''
    main class for work vk_bot
    '''

    def start(self):
        '''
        function launches loop handle message
        :return: not return
        '''
        while True:

            message_chat = self.longpooling()

            message_text = message_chat['text']  # преобразуем текст сообщения в переменную
            current_user_id = message_chat['peer_id']

            if message_text.lower() == "привет":
                vk_group().send_message(current_user_id, "Приветствую вас в приложении для поиска второй половинки,\n"
                           "я могу найти вторую половинку человеку по его id вконтакте,\n"
                           "для этого напишите мне команду : 'Найти половинку'" )


            elif message_text.lower() == 'найти половинку':
                vk_group().finding_a_half(current_user_id)

            else:
                vk_group().send_message(current_user_id, "Увы я не зна такую команду!\n"
                                                        "Можете попросить меня найти половинку\n"
                                                         "для этого напишите мне [найти половинку]")

