# Telegram verification-bot

This is a telegram group member verification bot written in python using python-telegram-bot wrapper library.

## Description
It's still a work in progress. It verifies new users when they get added to a group and asks them some questions which they need to answer within certain time in order to get verified and have read wrtie permissions within the group.
Failure to do so will result in user getting kicked or banned from the group. It's basic purpose is to prevent bot users from getting added.

## Features
It provides following features at the moment:
1. Restrict a new user, and redirects them to a new chat where they will have to verify themself
2. Provides basic commands to admin using which he can change certain settings of the bot:
    set_timer: to change the verification time limit

## How to configure the bot

Create a new Bot using 'Bot Father' on telegram and generate api token and replace it with 'TOKEN' in main.py.
Set questions, answers, timer and timeup_action (kick or ban) in global_config.py

## Future enhancements

1. Provide more control to admin over bot ( allow to change questions and answers etc.)
2. Currently it is limited to one group, it needs some changes to make it more scalable
