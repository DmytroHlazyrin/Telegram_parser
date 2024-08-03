from telethon import TelegramClient

from database import get_db, init_db
from models import Message
from decouple import config

# Вставьте ваши данные API ID и API Hash
API_ID = config("API_ID")
API_HASH = config("API_HASH")
PHONE_NUMBER = config("PHONE_NUMBER")

init_db()

client = TelegramClient(PHONE_NUMBER, API_ID, API_HASH)


async def main():
    await client.start(PHONE_NUMBER)

    # Получаем диалоги
    dialogs = await client.get_dialogs()

    for dialog in dialogs:
        # Проверяем, является ли диалог личным чатом и есть ли непрочитанные сообщения
        if dialog.is_user and dialog.unread_count > 0:
            # Получаем непрочитанные сообщения
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
            # Отмечаем сообщения как прочитанные
            await client.send_read_acknowledge(dialog.id)


if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
