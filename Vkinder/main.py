from vk_group_bot import Vkinder_bot, token_group, id_group, token_user

if __name__=='__main__':
    VKbot = Vkinder_bot(token_group, id_group, token_user)
    VKbot.start()