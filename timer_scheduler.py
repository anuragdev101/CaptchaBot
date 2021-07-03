from telegram import Update
from telegram.ext import CallbackContext
import global_config

time_in_seconds = global_config.greet_message_delete_timer * 60
user_updates_dict = global_config.user_updates_dict
bot_user_messages = global_config.bot_user_messages
timeup_action = global_config.timeup_action

from utilities import *

# Enable logging
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def alarm(context: CallbackContext) -> None:
    """Send the alarm message."""
    chat_id, user_id = context.job.context
    if(timeup_action == 'kick'):
        kick_user(user_id)
    else:
        ban_user(user_id)

def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def set_timer(update: Update, context: CallbackContext, new_user_id) -> None:
    """Add a job to the queue."""
    global time_in_seconds
    chat_id = update.effective_chat.id
    try:
        if time_in_seconds < 0:
            update.effective_chat.send_message(text='Sorry we can not go back to future!')
            return
        job_removed = remove_job_if_exists(str(new_user_id), context)
        context.job_queue.run_once(alarm, time_in_seconds, context=(chat_id, new_user_id), name=str(new_user_id))
        if job_removed:
            logger.info("Old job was removed")
        timer_message = update.effective_chat.send_message(text='You have ' + str( (int) (time_in_seconds/60)) + ' minutes to complete the test')
        if new_user_id not in bot_user_messages:
            bot_user_messages[new_user_id] = list()
        bot_user_messages[new_user_id].extend([timer_message])

    except (IndexError, ValueError):
        update.message.reply_text('Error in scheduling timer')