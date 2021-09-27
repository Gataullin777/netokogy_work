import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType



def main():
    """ Пример использования bots longpoll
        https://vk.com/dev/bots_longpoll
    """
    tok = '1b5021e6d18ac8993a692749443ef83e1371f849b652fe5cab0dd5a3298cd649bf41ef3ce1f296559615b'
    vk_session = vk_api.VkApi(token=f'{tok}')
    vk_session._auth_token()

    longpoll = VkBotLongPoll(vk_session, 206818303)

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            print('Новое сообщение:')

            print('Для меня от: ', end='')

            print(event.obj.from_id)

            print('Текст:', event.obj.text)
            print()

        elif event.type == VkBotEventType.MESSAGE_REPLY:
            print('Новое сообщение:')

            print('От меня для: ', end='')

            print(event.obj.peer_id)

            print('Текст:', event.obj.text)
            print()

        elif event.type == VkBotEventType.MESSAGE_TYPING_STATE:
            print('Печатает ', end='')

            print(event.obj.from_id, end=' ')

            print('для ', end='')

            print(event.obj.to_id)
            print()

        elif event.type == VkBotEventType.GROUP_JOIN:
            print(event.obj.user_id, end=' ')

            print('Вступил в группу!')
            print()

        elif event.type == VkBotEventType.GROUP_LEAVE:
            print(event.obj.user_id, end=' ')

            print('Покинул группу!')
            print()

        else:
            print(event.type)
            print()


if __name__ == '__main__':
    main()