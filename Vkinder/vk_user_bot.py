import vk_api
from pprint import pprint


token_user = '8a8d4d2e656257c1c60467984487ee444e58c1ad7f561578ef64e0ab271f65b7d00990cca85e8e07971a5'

city_name = 'уфа'

def search_user():
    vk = vk_api.VkApi(token=token_user)
    users = vk.method(
                        'users.search',
                      {
                       'q': None,
                       'count': 1,
                       'birth_day': 18,
                       'birth_month': 11,
                       'birth_year': 1992,
                       'fields': 'photo, screen_name, city',
                       'sex': 1,
                       'v': 5.131
                      }
                      )
    pprint(users)


def id_city(city_name):
    vk = vk_api.VkApi(token=token_user)

    countries_id = vk.method('database.getCountries',
                             {
                                 'code': 'RU'
                             })
    countries_id = countries_id['items'][0]['id']
    print(countries_id)

    id_city = vk.method('database.getCities',
                        {
                            'q': f'{city_name}',
                            'country_id': countries_id,
                            'count': 1
                        })
    id_city = id_city['items'][0]['id']
    print(id_city)
    return id_city

def get_all_photos_user(user_id):
    vk = vk_api.VkApi(token=token_user)
    photos = vk.method(
        'photos.getAll',
        {
            'owner_id': user_id,
            'extended': 1,
            'count': 200,
            'no_service_albums': 0,
            'photo_sizes': 1

        }
    )
    pprint(photos)

# get_photos_user(25518283)

def counting_likes_and_comments_photo(user_id):
    '''
    counting likes and comments photo profile vk.com
    :param user_id: id user from vk.com
    :return: links on top 3 popular photo from profile user vk.com
    '''

    vk = vk_api.VkApi(token=token_user)
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





counting_likes_and_comments_photo(191048524)