from vk_bot import Vkinder_bot
from access import token_group, id_group, token_user


if __name__=='__main__':
    Vkinder = Vkinder_bot(token_group, id_group, token_user)
    Vkinder.start()