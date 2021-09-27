from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

token = '1b5021e6d18ac8993a692749443ef83e1371f849b652fe5cab0dd5a3298cd649bf41ef3ce1f296559615b'

vk = vk_api.VkApi(token=token)
vk._auth_token()
longpoll = VkLongPoll(vk)

print(' ok ')
def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7)})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text

            if request == "привет":
                write_msg(event.user_id, f"Хай, {event.user_id}")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")
