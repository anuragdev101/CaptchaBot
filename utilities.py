from telegram import ChatPermissions

import global_config

user_updates_dict = global_config.user_updates_dict
bot_user_messages = global_config.bot_user_messages

def perform_action_and_cleanup_helper(func):

    def inner(*args, **kwargs):
        func(*args, **kwargs)
        global bot_user_messages
        global user_updates_dict

        del user_updates_dict[args[0]]
        for message in bot_user_messages[args[0]]:
            message.delete()
        del bot_user_messages[args[0]]

    return inner

@perform_action_and_cleanup_helper
def kick_user(id):
    global user_updates_dict
    if user_updates_dict[id] is not None:
        update = user_updates_dict[id]
        update.effective_chat.unban_member(user_id=id)

@perform_action_and_cleanup_helper
def ban_user(id):
    global user_updates_dict
    if user_updates_dict[id] is not None:
        update = user_updates_dict[id]
        update.effective_chat.ban_member(user_id=id)

@perform_action_and_cleanup_helper
def unrestrict_user(id):
    global user_updates_dict
    if user_updates_dict[id] is not None:
        update = user_updates_dict[id]
        update.effective_chat.restrict_member(user_id=id,
                                              permissions=ChatPermissions(can_send_messages=True,
                                                                          can_send_media_messages=True,
                                                                          can_send_polls=True,
                                                                          can_send_other_messages=True,
                                                                          can_add_web_page_previews=True,
                                                                          can_change_info=True,
                                                                          can_invite_users=True,
                                                                          can_pin_messages=True))