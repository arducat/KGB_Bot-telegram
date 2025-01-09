import re
import telebot
import asyncio
import fortune

from os import getenv
from datetime import datetime, timezone
from difflib import SequenceMatcher
from telebot.async_telebot import AsyncTeleBot



kgb = AsyncTeleBot(getenv('TOKEN', ''))


# Saving time at the moment of bot start
start_time = datetime.now(timezone.utc)



# User verification function for administrator rights
async def is_user_admin(chat_id, user_id):
    admin_statuses = ["creator", "administrator"]
    if user_id == "YOUR_ID": # God mode hehe:3
        return 1
    result = await kgb.get_chat_member(chat_id, user_id)
    if result.status in admin_statuses:
        return 1
    return 0



# Sending a quote
@kgb.message_handler(commands=['quote'])
async def quote(message):
    fortun = fortune.get_random_fortune('quotes.txt')
    
    await kgb.reply_to(message,f'`{fortun}`')


# Adding a user to the users monitoring list
@kgb.message_handler(commands=['add_user'])
async def add_user(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    result = await is_user_admin(chat_id, user_id)

    # Checking a user for administrator rights
    if result == 0:
        await kgb.reply_to(message, "You do not have permission to run this command.")
        return
    # Checking a command for an argument
    args = message.text.split()
    if len(args) < 2:
        await kgb.reply_to(message, "Please enter a user ID. \nExample: /add_user 123123123")
        return

    user_to_add = args[1]
    print(f"Attempting to add user: {user_to_add}") # Debugging to the console

    # Handling errors and adding a user to the list
    try:
        with open('users.txt', 'r') as file:
            existing_users = file.read().splitlines()

        # Sending an error message that the user is already on the list
        if user_to_add in (user.lower() for user in existing_users):
            await kgb.reply_to(message, f"The user ID '{user_to_add}' already exists in the list.")
            return

        # Adding a user to the list
        with open('users.txt', 'a') as file:
            file.write(f'\n{user_to_add}')

        # Sending a message that the user has been successfully added to the list
        await kgb.reply_to(message, f"User ID '{user_to_add}' added.")
    # Sending an error message
    except Exception as e:
        await kgb.reply_to(message, f"An error occurred: {str(e)}")


# Adding a swear word to the list of swear words
@kgb.message_handler(commands=['add_swear'])
async def add_swear(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    result = await is_user_admin(chat_id, user_id)

    # Checking a user for administrator rights
    if result == 0:
        await kgb.reply_to(message, "You do not have permission to run this command.")
        return
    # Checking a command for an argument
    args = message.text.split()
    if len(args) < 2:
        await kgb.reply_to(message, "Please enter a swear word. \nExample: /add_swear FUCK")
        return

    swear_word_to_add = args[1].lower()
    print(f"Attempting to add a swear word: {swear_word_to_add}") # Debugging to the console

    # Handling errors and adding swear word to the list
    try:
        with open('swearing.txt', 'r') as file:
            existing_swears = file.read().splitlines()

        # Sending an error message that the swear word is already on the list
        if swear_word_to_add in (word.lower() for word in existing_swears):
            await kgb.reply_to(message, f"The swear word '{swear_word_to_add}' already exists in the list.")
            return

        # Adding a swear word to the list
        with open('swearing.txt', 'a') as file:
            file.write(f'\n{swear_word_to_add}')

        # Sending a message that the swear word has been successfully added to the list
        await kgb.reply_to(message, f"Swear word '{swear_word_to_add}' added.")
    # Sending an error message
    except Exception as e:
        await kgb.reply_to(message, f"An error occurred: {str(e)}")


# Removing a user from the users monitoring list
@kgb.message_handler(commands=['remove_user'])
async def remove_user(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    result = await is_user_admin(chat_id, user_id)

    # Checking a user for administrator rights
    if result == 0:
        await kgb.reply_to(message, "You do not have permission to run this command.")
        return
    # Checking a command for an argument
    args = message.text.split()
    if len(args) < 2:
        await kgb.reply_to(message, "Please enter user ID. \nExample: /remove_user 123123123")
        return

    user_id_to_remove = args[1]
    print(f"Removing a user: ID = {user_id_to_remove}")  # Debugging to the console

    # Handling errors and removing a user from the list
    try:
        with open('users.txt', 'r') as file:
            users = file.readlines()
            
        # Removing a user from the list
        with open('users.txt', 'w') as file:
            for user in users:
                if user.strip() != user_id_to_remove:
                    file.write(user)

        # Sending a message that the user has been successfully removed from the list
        await kgb.reply_to(message, f"User ID: {user_id_to_remove} has been removed.")
    # Sending an error message that the file with the list of users was not found
    except FileNotFoundError:
        await kgb.reply_to(message, "User list not found.")
    # Sending an error message
    except Exception as e:
        await kgb.reply_to(message, f"An error occurred: {str(e)}")


# Removing a swear word from the list of swear words
@kgb.message_handler(commands=['remove_swear'])
async def remove_swear(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    result = await is_user_admin(chat_id, user_id)

    # Checking a user for administrator rights
    if result == 0:
        await kgb.reply_to(message, "You do not have permission to run this command.")
        return
    # Checking a command for an argument
    args = message.text.split()
    if len(args) < 2:
        await kgb.reply_to(message, "Please enter a swear word. \nExample: /remove_swear FUCK")
        return

    swear_word_to_remove = args[1]
    print(f"Removing a swear word: {swear_word_to_remove}")  # Debugging to the console

    # Handling errors and removing swear word from the list
    try:
        with open('swearing.txt', 'r') as file:
            swearing = file.readlines()

        # Removing a swear word from the list
        with open('swearing.txt', 'w') as file:
            for swear in swearing:
                if swear.strip() != swear_word_to_remove:
                    file.write(swear)

        # Sending a message that the swear word has been successfully removed from the list
        await kgb.reply_to(message, f"Swear word '{swear_word_to_remove}' removed.")
    # Sending an error message that the swear words list file was not found
    except FileNotFoundError:
        await kgb.reply_to(message, "Swearing list not found.")
    # Sending an error message
    except Exception as e:
        await kgb.reply_to(message, f"An error occurred: {str(e)}")


# Command to find out how long the bot has been running
@kgb.message_handler(commands=['uptime'])
async def send_uptime(message):
    current_time = datetime.now(timezone.utc)
    uptime_duration = current_time - start_time

    # Getting days hours and minutes from bot running time
    days = uptime_duration.days
    hours, remainder = divmod(uptime_duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Formatting and sending a message to a user
    uptime_str = f"{days} days, {hours} hours, {minutes} minutes."
    await kgb.send_message(message.chat.id, f'The bot has been running for: \n{uptime_str}')


# Function for searching and removing swear words from users in the monitoring list
@kgb.message_handler(func=lambda message: True)
async def checking_messages(message):
    text = message.text
    user_id = str(message.from_user.id)
    text_cleaning = re.split(r'[,.\n? ]+', text)
    user_name = message.from_user.username

    # Handling errors and searching/removing swear words from users from the monitoring list
    try:
        # Reading files with a list of users, curses and exceptions
        with open("swearing.txt", "r") as swear_content:
            curses = swear_content.read().split()
        with open("users.txt", "r") as user_content:
            users_check = user_content.read().split()
        with open("exceptions.txt", "r") as exceptions_content:
            exceptions = exceptions_content.read().split()

        print(f"Message checking: ID = {user_id}, Username = @{user_name}")  # Debugging to the console

        # Searching for a user in the list of users to monitoring
        if user_id in users_check:
            # Searching for swear words in user's text
            for word in text_cleaning:
                for swear in curses:
                    # Comparison of a user's word from the text with a swear word from the list
                    similarity = SequenceMatcher(None, word.lower(), swear.lower()).ratio()
                    # If the match is greater than or equal to 60%, then we delete the user’s message
                    if similarity >= 0.6:
                        # If the word is in the exceptions, then ignore it.
                        if word.lower() in exceptions:
                            continue
                        print(f"Message removed, swearing '{swear}' word '{word}' similarity {similarity}")   # Debugging to the console
                        await kgb.delete_message(message.chat.id, message.id)
                        return
    # Sending an error message that files were not found
    except FileNotFoundError as e:
        print(f"File not found: {str(e)}")
    # Sending an error message
    except Exception as e:
        print(f"An error occurred while checking messages: {str(e)}")


# Running a bot
if __name__ == '__main__':
    print("KGB bot is turned on!")
    asyncio.run(kgb.polling())
