from telegram import Update, ChatMemberUpdated, ChatMember, ParseMode, ChatPermissions, InlineKeyboardButton, \
    InlineKeyboardMarkup, Chat
from telegram.ext import CallbackContext
import global_config
import logging
from timer_scheduler import set_timer

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

bot_user_messages = global_config.bot_user_messages

def track_chats(update: Update, context: CallbackContext) -> None:
    """Tracks the chats the bot is in."""
    result = extract_status_change(update.my_chat_member)
    if result is None:
        return
    was_member, is_member = result

    # Let's check who is responsible for the change
    cause_name = update.effective_user.full_name

    # Handle chat types differently:
    chat = update.effective_chat
    if chat.type == Chat.PRIVATE:
        if not was_member and is_member:
            logger.info("%s started the bot", cause_name)
            context.bot_data.setdefault("user_ids", set()).add(chat.id)
        elif was_member and not is_member:
            logger.info("%s blocked the bot", cause_name)
            context.bot_data.setdefault("user_ids", set()).discard(chat.id)
    elif chat.type in [Chat.GROUP, Chat.SUPERGROUP]:
        if not was_member and is_member:
            logger.info("%s added the bot to the group %s", cause_name, chat.title)
            context.bot_data.setdefault("group_ids", set()).add(chat.id)
        elif was_member and not is_member:
            logger.info("%s removed the bot from the group %s", cause_name, chat.title)
            context.bot_data.setdefault("group_ids", set()).discard(chat.id)
    else:
        if not was_member and is_member:
            logger.info("%s added the bot to the channel %s", cause_name, chat.title)
            context.bot_data.setdefault("channel_ids", set()).add(chat.id)
        elif was_member and not is_member:
            logger.info("%s removed the bot from the channel %s", cause_name, chat.title)
            context.bot_data.setdefault("channel_ids", set()).discard(chat.id)


def extract_status_change(chat_member_update: ChatMemberUpdated):
    status_change = chat_member_update.difference().get("status")

    old_is_member, new_is_member = chat_member_update.difference().get("is_member", (None, None))

    if status_change is None:
        return None

    old_status, new_status = status_change

    was_member = (
            old_status in [
        ChatMember.MEMBER, ChatMember.CREATOR, ChatMember.ADMINISTRATOR
    ]
            or (old_status == ChatMember.RESTRICTED and old_is_member is True)
    )

    is_member = (
            new_status in [
        ChatMember.MEMBER, ChatMember.CREATOR, ChatMember.ADMINISTRATOR
    ]
            or (new_status == ChatMember.RESTRICTED and new_is_member is True)
    )

    return was_member, is_member


def chat_member_update(update: Update, context: CallbackContext):

    global user_updates_dict

    result = extract_status_change(update.chat_member)

    if result is None:
        return

    was_member, is_member = result
    cause_name = update.chat_member.from_user.mention_html()
    member_name = update.chat_member.new_chat_member.user.mention_html()

    if not was_member and is_member:
        greet_message = update.effective_chat.send_message(
            f"{member_name} was added by {cause_name}. Welcome!.", parse_mode=ParseMode.HTML
        )
        new_user_id = update.chat_member.new_chat_member.user.id
        update.effective_chat.restrict_member(user_id=new_user_id, permissions=ChatPermissions())
        keyboard = [[InlineKeyboardButton("Start Test",callback_data=1,url=f"https://t.me/H_captcha_bot")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        restrict_message = update.effective_chat.send_message(text="You have been restricted from posting anything in "
                                                                   "this group. Press the button below and answer the"
                                                                   " questions.",reply_markup=reply_markup)
        user_updates_dict[new_user_id]=update
        if new_user_id not in bot_user_messages:
            bot_user_messages[new_user_id] = list()
            bot_user_messages[new_user_id].extend([greet_message, restrict_message])
        set_timer(update,context, new_user_id)

    elif was_member and not is_member:
        update.effective_chat.send_message(
            f"{member_name} is no longer with us. Thanks a lot, {cause_name} ...", parse_mode=ParseMode.HTML
        )