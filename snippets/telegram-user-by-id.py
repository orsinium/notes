"""
This script allow you to send in Telegram message with link on user.

If user has login, you can just send "@login" message, and telegram
transform it into link on user profile.
However you cannot do it if user has no login.
In this case you need to this snippet.

This snippet get `user_id`, transfor it to link on this user and send this link
in message to `send_to`.
"""

from telethon import TelegramClient, tl


# https://my.telegram.org
API_ID = 12345
API_HASH = '...'


user_id = 82752261      # ID of user that profile you want to get in message.
send_to = 'orsinium'    # login or ID of message receiver.
message = 'touch me'    # text of message with link


client = TelegramClient('session_name', API_ID, API_HASH)
client.start()

full_user = client(tl.functions.users.GetFullUserRequest(user_id))
input_user = tl.types.InputUser(
    user_id=full_user.user.id,
    access_hash=full_user.user.access_hash,
)

client(
    tl.functions.messages.SendMessageRequest(
        send_to, message, entities=[
            tl.types.InputMessageEntityMentionName(
                offset=0,
                length=len(message),
                user_id=input_user,
            ),
        ],
    ),
)
