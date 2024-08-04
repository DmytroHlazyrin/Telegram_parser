from telethon import TelegramClient

from database import get_db, init_db
from models import Message
from decouple import config

API_ID = config("API_ID")
API_HASH = config("API_HASH")
PHONE_NUMBER = config("PHONE_NUMBER")

init_db()

client = TelegramClient("session", API_ID, API_HASH)


async def main():
    await client.start(PHONE_NUMBER)

    # Get dialogs
    dialogs = await client.get_dialogs()

    for dialog in dialogs:
        # Check if dialog is a user and has unread messages
        if dialog.is_user and dialog.unread_count > 0:
            # Get unread messages from the dialog and save them to the database
            messages = await client.get_messages(dialog.id, limit=dialog.unread_count)

            for message in reversed(messages):
                print(f'From: {dialog.name}, Message: {message.text}')
                db = next(get_db())
                db_message = Message(
                    message_id=message.id,
                    sender_id=message.sender_id if message.sender else None,
                    first_name=message.sender.first_name if message.sender else None,
                    last_name=message.sender.last_name if message.sender else None,
                    username=message.sender.username if message.sender else None,
                    phone_number=message.sender.phone if message.sender else None,
                    text=message.text,
                    date=message.date
                )
                db.add(db_message)
                db.commit()
                db.refresh(db_message)
            # Mark dialog as read
            await client.send_read_acknowledge(dialog.id)


if __name__ == "__main__":
    import traceback

    try:
        with client:
            client.loop.run_until_complete(main())
        with open("/var/log/cron.log", "a") as log_file:
            log_file.write("Script executed successfully\n")
    except Exception as e:
        with open("/var/log/cron.log", "a") as log_file:
            log_file.write(f"Error: {str(e)}\n")
            log_file.write("".join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)))
