# KGB_Bot-telegram
The one and only KGB bot for telegram!
## This bot has the following features:
1. The `uptime` command to determine the continuous operation time of the bot.  
2. The `quote` command sends a random quote from the quotes.txt file.  
3. The `add_user` command adds a user for monitoring to the users.txt file.  
4. The `add_swear` command adds a swear word to the swearing.txt file.  
5. The `remove_user` command removes a user from the monitoring list in the users.txt file.
6. The `remove_swear` command removes swear words from the list of swear words in the swearing.txt file.
7. The main loop checks if the message belongs to a user who is on the monitoring list.  
If the user is on the monitoring list, the bot checks each word in their message.  
If the word looks like a swear word from the swearing list, the bot checks if the word is on the exception list.  
If the word is on the exception list, the bot does nothing, and if the word is a swear word, user's message is deleted.
## Important note!
The quotes.txt, swearing.txt, users.txt and exceptions.txt files must be created manually in advance!
