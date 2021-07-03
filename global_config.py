from collections import OrderedDict
# global variables

FIRST, SECOND, THIRD, FINAL = range(4)

# verification attempts for each question
no_of_verification_attempts = 3

# dict storing user_id:Updates mapping
user_updates_dict = {}

# dict storing user_id: list(Message) mapping
bot_user_messages = {}

# time after which the welcome messages are deleted
greet_message_delete_timer = 1

# list containing verification questions
verification_questions = ["Ques1","Ques2","Ques3"]

# list containing verification answers
verification_answers = ["Ans1","Ans2","Ans3"]

# action to take after time's up and user is unverified, Kick or Ban
timeup_action = 'kick'