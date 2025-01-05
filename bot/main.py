import telebot
import asyncio
import re
from telebot.async_telebot import AsyncTeleBot
from difflib import SequenceMatcher

bot = AsyncTeleBot('TOKEN')

async def is_user_admin(chat_id, user_id):
    admin_statuses = ["creator", "administrator"]
    if user_id == "YOUR_ID":
        return 1
    result = await bot.get_chat_member(chat_id, user_id)
    if result.status in admin_statuses:
        return 1
    return 0

@bot.message_handler(commands=['add_user'])
async def add_user(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    result = await is_user_admin(chat_id, user_id)
    
    if result == 0:
        await bot.reply_to(message, "You do not have permission to run this command.")
        return

    args = message.text.split()
    if len(args) < 2:
        await bot.reply_to(message, "Please enter a user ID. \nExample: /add_user 123123123")
        return

    user_to_add = args[1]
    print(f"Attempting to add user: {user_to_add}")

    try:
        with open('users.txt', 'r') as file:
            existing_users = file.read().splitlines()

        if user_to_add in (user.lower() for user in existing_users):
            await bot.reply_to(message, f"The user ID '{user_to_add}' already exists in the list.")
            return

        with open('users.txt', 'a') as file:
            file.write(f'\n{user_to_add}')

        await bot.reply_to(message, f"User ID '{user_to_add}' added.")
    except Exception as e:
        await bot.reply_to(message, f"An error occurred: {str(e)}")

@bot.message_handler(commands=['add_swear'])
async def add_swear(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    result = await is_user_admin(chat_id, user_id)
    if result == 0:
        await bot.reply_to(message, "You do not have permission to run this command.")
        return

    args = message.text.split()
    if len(args) < 2:
        await bot.reply_to(message, "Please enter a swear word. \nExample: /add_swear FUCK")
        return

    swear_word_to_add = args[1].lower()
    print(f"Attempting to add a swear word: {swear_word_to_add}")

    try:
        with open('swearing.txt', 'r') as file:
            existing_swears = file.read().splitlines()

        if swear_word_to_add in (word.lower() for word in existing_swears):
            await bot.reply_to(message, f"The swear word '{swear_word_to_add}' already exists in the list.")
            return

        with open('swearing.txt', 'a') as file:
            file.write(f'\n{swear_word_to_add}')

        await bot.reply_to(message, f"Swear word '{swear_word_to_add}' added.")
    except Exception as e:
        await bot.reply_to(message, f"An error occurred: {str(e)}")

@bot.message_handler(commands=['remove_user'])
async def remove_user(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    result = await is_user_admin(chat_id, user_id)
    if result == 0:
        await bot.reply_to(message, "You do not have permission to run this command.")
        return

    args = message.text.split()
    if len(args) < 2:
        await bot.reply_to(message, "Please enter user ID. \nExample: /remove_user 123123123")
        return

    user_id_to_remove = args[1]
    print(f"Removing a user: ID = {user_id_to_remove}")

    try:
        with open('users.txt', 'r') as file:
            users = file.readlines()

        with open('users.txt', 'w') as file:
            for user in users:
                if user.strip() != user_id_to_remove:
                    file.write(user)

        await bot.reply_to(message, f"User ID: {user_id_to_remove} has been removed.")
    except FileNotFoundError:
        await bot.reply_to(message, "User list not found.")
    except Exception as e:
        await bot.reply_to(message, f"An error occurred: {str(e)}")

@bot.message_handler(commands=['remove_swear'])
async def remove_swear(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    result = await is_user_admin(chat_id, user_id)
    if result == 0:
        await bot.reply_to(message, "You do not have permission to run this command.")
        return
    
    args = message.text.split()
    if len(args) < 2:
        await bot.reply_to(message, "Please enter a swear word. \nExample: /remove_swear FUCK")
        return

    swear_word_to_remove = args[1]
    print(f"Removing a swear word: {swear_word_to_remove}")

    try:
        with open('swearing.txt', 'r') as file:
            swearing = file.readlines()

        with open('swearing.txt', 'w') as file:
            for swear in swearing:
                if swear.strip() != swear_word_to_remove:
                    file.write(swear)

        await bot.reply_to(message, f"Swear word '{swear_word_to_remove}' removed.")
    except FileNotFoundError:
        await bot.reply_to(message, "Swearing list not found.")
    except Exception as e:
        await bot.reply_to(message, f"An error occurred: {str(e)}")

@bot.message_handler(func=lambda message: True)
async def checking_messages(message):
    text = message.text
    user_id = str(message.from_user.id)
    text_cleaning = re.split(r'[,.\n? ]+', text)
    user_name = message.from_user.username

    try:
        with open("swearing.txt", "r") as swear_content:
            curses = swear_content.read().split()

        with open("users.txt", "r") as user_content:
            users_check = user_content.read().split()

        print(f"Message checking: ID = {user_id}, Username = @{user_name}")

        if user_id in users_check:
            for word in text_cleaning:
                for swear in curses:
                    similarity = SequenceMatcher(None, word.lower(), swear.lower()).ratio()
                    if similarity >= 0.6:
                        print(f"Message removed, swearing '{swear}' word '{word}' similarity {similarity}")
                        await bot.delete_message(message.chat.id, message.id)
                        return
    except FileNotFoundError as e:
        print(f"File not found: {str(e)}")
    except Exception as e:
        print(f"An error occurred while checking messages: {str(e)}")

if __name__ == '__main__':
    asyncio.run(bot.polling())
