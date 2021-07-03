
from telegram.ext import Updater, ConversationHandler
import logging

from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters, CallbackContext
from telegram import Update
from telegram.ext import ChatMemberHandler

from chat_member_update import track_chats, chat_member_update
import global_config

from verification import start, first, second, third, final, cancel

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# global variables
no_of_verification_attempts = global_config.no_of_verification_attempts
user_updates_dict = global_config.user_updates_dict
bot_user_messages = global_config.bot_user_messages
greet_message_delete_timer = global_config.greet_message_delete_timer


def set_verification_time(update: Update, context: CallbackContext):
    global greet_message_delete_timer
    time_in_minutes = int(context.args[0])
    greet_message_delete_timer = time_in_minutes * 60
    update.effective_chat.send_message("Countdown timer set to "+ str(time_in_minutes)+ " minutes!")

updater = Updater(token='TOKEN', use_context=True)

dispatcher = updater.dispatcher

dispatcher.add_handler(ChatMemberHandler(track_chats, ChatMemberHandler.MY_CHAT_MEMBER))
dispatcher.add_handler(ChatMemberHandler(chat_member_update, ChatMemberHandler.CHAT_MEMBER))
dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            global_config.FIRST: [MessageHandler(Filters.regex('^(Yes|No)$'), first)],
            global_config.SECOND: [MessageHandler(Filters.text, second)],
            global_config.THIRD: [MessageHandler(Filters.text, third)],
            global_config.FINAL: [MessageHandler(Filters.text, final)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],run_async=True
    ))
dispatcher.add_handler(CommandHandler("set_timer", set_verification_time))
updater.start_polling(allowed_updates=Update.ALL_TYPES)
updater.idle()
