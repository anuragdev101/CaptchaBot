from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext, ConversationHandler
import global_config
import logging
from utilities import kick_user, ban_user, unrestrict_user

verification_questions = global_config.verification_questions
verification_answers = global_config.verification_answers
user_updates_dict = global_config.user_updates_dict
bot_user_messages = global_config.bot_user_messages

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> int:

    global user_updates_dict

    if update.message.from_user['id'] not in user_updates_dict:
        update.message.reply_text("Don't do personal chats with me, find a bf/gf. Bye!"),
        return ConversationHandler.END

    reply_keyboard = [['Yes', 'No']]
    update.message.reply_text(
        'Hi! I am Captcha Bot for HYT Union Group. I will ask you some questions which you need to answer to get verified in the group \n\n'
        'You have 2 attempts to answer each question correctly, If your answers are wrong, you will get banned from entering the group. Do you Understand?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )
    return global_config.FIRST


def first(update: Update, context: CallbackContext) -> int:

    global verification_questions
    user = update.message.from_user
    if update.message.text == 'Yes':
        logger.info("Good! Here is your first question", user.first_name, update.message.text)
        update.message.reply_text(verification_questions[0],reply_markup=ReplyKeyboardRemove(),
        )
        return global_config.SECOND
    else:
        kick_user(user['id'])
        return ConversationHandler.END


def second(update: Update, context: CallbackContext) -> int:

    global verification_questions
    user = update.message.from_user
    if update.message.text == verification_answers[0]:
        update.message.reply_text(verification_questions[1],reply_markup=ReplyKeyboardRemove(),
        )
        return global_config.THIRD
    else:
        ban_user(user['id'])
        return ConversationHandler.END


def third(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    if update.message.text == verification_answers[1]:
        update.message.reply_text(verification_questions[2],reply_markup=ReplyKeyboardRemove(),
        )
        return global_config.FINAL
    else:
        ban_user(user['id'])
        return ConversationHandler.END


def final(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    if update.message.text == verification_answers[2]:
        update.message.reply_text(
            'You are verified now',
            reply_markup=ReplyKeyboardRemove(),
        )
        unrestrict_user(user['id'])
        return ConversationHandler.END
    else:
        ban_user(user['id'])


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Verification got cancelled.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END