import requests
import vk_api
import datetime


#
# access_token_vk = 'a02c3fa721a2d5b8119c45c9e03db0dbbc038b1645a20a6723a9f9654079a4900e431ce1312dc908b38d9'
#
# params = {
#     'group_id': '206818303',
#     'token': f'{access_token_vk}'
#         }
# url = 'https://api.vk.com/method/groups.getLongPollSettings?group_id=206818303&access_token=a02c3fa721a2d5b8119c45c9e03db0dbbc038b1645a20a6723a9f9654079a4900e431ce1312dc908b38d9&v=5.131'
#
# response = requests.get(url, params=params )
#
# print(response.status_code)
# print(response.json())


# session = vk_api.VkApi(token=access_token_vk)
# vk = session.get_api()
#
# vk.groups.getLongPollSettings(group_id='206818303')

# work whaatsapp
# #Login
# login_page = LoginPage(driver)
# login_page.load()
# time.sleep(7)

# dict_ = {'time': 11, 'wer': {'time_2': 22}}
#
# print(dict_.get('wer').get('time_2'))
#


dict_ = {'bdate': '18.11.1992'}

age = dict_['bdate'].split('.')[-1]
print(age)
age = int(age)
print(type(age))