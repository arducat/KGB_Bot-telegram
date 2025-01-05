import telebot
import asyncio
import re
from telebot.async_telebot import AsyncTeleBot
from difflib import SequenceMatcher



bot = AsyncTeleBot('TOKEN')



# User verification function for administrator rights
async def is_user_admin(chat_id, user_id):
    admin_statuses = ["creator", "administrator"]
    if user_id == "YOUR_ID": # God mode hehe:3
        return 1
    result = await bot.get_chat_member(chat_id, user_id)
    if result.status in admin_statuses:
        return 1
    return 0



# Adding a user to the users monitoring list
@bot.message_handler(commands=['add_user'])
async def add_user(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    result = await is_user_admin(chat_id, user_id)

    # Checking a user for administrator rights
    if result == 0:
        await bot.reply_to(message, "You do not have permission to run this command.")
        return
    # Checking a command for an argument
    args = message.text.split()
    if len(args) < 2:
        await bot.reply_to(message, "Please enter a user ID. \nExample: /add_user 123123123")
        return

    user_to_add = args[1]
    print(f"Attempting to add user: {user_to_add}") # Debugging to the console

    # Handling errors and adding a user to the list
    try:
        with open('users.txt', 'r') as file:
            existing_users = file.read().splitlines()

        # Sending an error message that the user is already on the list
        if user_to_add in (user.lower() for user in existing_users):
            await bot.reply_to(message, f"The user ID '{user_to_add}' already exists in the list.")
            return

        # Adding a user to the list
        with open('users.txt', 'a') as file:
            file.write(f'\n{user_to_add}')

        # Sending a message that the user has been successfully added to the list
        await bot.reply_to(message, f"User ID '{user_to_add}' added.")
    # Sending an error message
    except Exception as e:
        await bot.reply_to(message, f"An error occurred: {str(e)}")


# Adding a swear word to the list of swear words
@bot.message_handler(commands=['add_swear'])
async def add_swear(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    result = await is_user_admin(chat_id, user_id)

    # Checking a user for administrator rights
    if result == 0:
        await bot.reply_to(message, "You do not have permission to run this command.")
        return
    # Checking a command for an argument
    args = message.text.split()
    if len(args) < 2:
        await bot.reply_to(message, "Please enter a swear word. \nExample: /add_swear FUCK")
        return

    swear_word_to_add = args[1].lower()
    print(f"Attempting to add a swear word: {swear_word_to_add}") # Debugging to the console

    # Handling errors and adding swear word to the list
    try:
        with open('swearing.txt', 'r') as file:
            existing_swears = file.read().splitlines()

        # Sending an error message that the swear word is already on the list
        if swear_word_to_add in (word.lower() for word in existing_swears):
            await bot.reply_to(message, f"The swear word '{swear_word_to_add}' already exists in the list.")
            return

        # Adding a swear word to the list
        with open('swearing.txt', 'a') as file:
            file.write(f'\n{swear_word_to_add}')

        # Sending a message that the swear word has been successfully added to the list
        await bot.reply_to(message, f"Swear word '{swear_word_to_add}' added.")
    # Sending an error message
    except Exception as e:
        await bot.reply_to(message, f"An error occurred: {str(e)}")


# Removing a user from the users monitoring list
@bot.message_handler(commands=['remove_user'])
async def remove_user(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    result = await is_user_admin(chat_id, user_id)

    # Checking a user for administrator rights
    if result == 0:
        await bot.reply_to(message, "You do not have permission to run this command.")
        return
    # Checking a command for an argument
    args = message.text.split()
    if len(args) < 2:
        await bot.reply_to(message, "Please enter user ID. \nExample: /remove_user 123123123")
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
        await bot.reply_to(message, f"User ID: {user_id_to_remove} has been removed.")
    # Sending an error message that the file with the list of users was not found
    except FileNotFoundError:
        await bot.reply_to(message, "User list not found.")
    # Sending an error message
    except Exception as e:
        await bot.reply_to(message, f"An error occurred: {str(e)}")


# Removing a swear word from the list of swear words
@bot.message_handler(commands=['remove_swear'])
async def remove_swear(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    result = await is_user_admin(chat_id, user_id)

    # Checking a user for administrator rights
    if result == 0:
        await bot.reply_to(message, "You do not have permission to run this command.")
        return
    # Checking a command for an argument
    args = message.text.split()
    if len(args) < 2:
        await bot.reply_to(message, "Please enter a swear word. \nExample: /remove_swear FUCK")
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
        await bot.reply_to(message, f"Swear word '{swear_word_to_remove}' removed.")
    # Sending an error message that the swear words list file was not found
    except FileNotFoundError:
        await bot.reply_to(message, "Swearing list not found.")
    # Sending an error message
    except Exception as e:
        await bot.reply_to(message, f"An error occurred: {str(e)}")


# Function for searching and removing swear words from users in the monitoring list
@bot.message_handler(func=lambda message: True)
async def checking_messages(message):
    text = message.text
    user_id = str(message.from_user.id)
    text_cleaning = re.split(r'[,.\n? ]+', text)
    user_name = message.from_user.username

    # Handling errors and searching/removing swear words from users from the monitoring list
    try:
        # Reading files with a list of users and swear words
        with open("swearing.txt", "r") as swear_content:
            curses = swear_content.read().split()
        with open("users.txt", "r") as user_content:
            users_check = user_content.read().split()

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
                        print(f"Message removed, swearing '{swear}' word '{word}' similarity {similarity}")   # Debugging to the console
                        await bot.delete_message(message.chat.id, message.id)
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
    asyncio.run(bot.polling())
