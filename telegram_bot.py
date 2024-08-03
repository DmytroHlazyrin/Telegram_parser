from decouple import config
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from sqlalchemy.orm import Session
from database import get_db
from models import Message
import logging


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

PAGE_SIZE = 10

class TelegramBot:
    def __init__(self, token: str) -> None:
        self.token = token
        self.application = Application.builder().token(token).build()
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text)
        )
        self.application.add_handler(
            CallbackQueryHandler(self.show_more)
        )

    async def start(
            self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        keyboard = [[KeyboardButton("Show latest 10 messages")]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "Welcome! Use the button below to get the latest messages.",
            reply_markup=reply_markup,
        )

    async def handle_text(
            self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        if update.message.text == "Show latest 10 messages":
            await self.latest(update, context)

    async def latest(
            self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        db = next(get_db())
        context.user_data["offset"] = 0
        messages = self._get_messages_page(db, 0, PAGE_SIZE)

        if messages:
            response = self._format_messages(messages)
            keyboard = [
                [InlineKeyboardButton("Show more", callback_data="show_more")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                response,
                reply_markup=reply_markup,
            )
        else:
            await update.message.reply_text("No messages found.")

    async def show_more(
            self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        query = update.callback_query
        db = next(get_db())
        offset = context.user_data.get("offset", 0) + PAGE_SIZE
        messages = self._get_messages_page(db, offset, PAGE_SIZE)

        if messages:
            response = self._format_messages(messages)
            context.user_data["offset"] = offset
            keyboard = [
                [InlineKeyboardButton("Show more", callback_data="show_more")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                response,
                reply_markup=reply_markup,
            )
        else:
            await query.edit_message_text("No more messages.")

        await query.answer()

    def _get_messages_page(self, db: Session, offset: int, limit: int) -> list:
        return db.query(Message).order_by(Message.date.desc()).offset(
            offset
        ).limit(limit).all()

    def _format_messages(self, messages: list) -> str:
        response = ""
        for message in messages:
            response += (
                f"Message ID: {message.message_id}\n"
                f"Date: {message.date}\n"
                f"Sender ID: {message.sender_id}\n"
                f"First Name: {message.first_name}\n"
                f"Last Name: {message.last_name}\n"
                f"Username: {message.username}\n"
                f"Text: {message.text}\n\n"
            )
        return response

    def run(self) -> None:
        self.application.run_polling()


if __name__ == "__main__":
    bot_token = config("TELEGRAM_BOT_TOKEN")
    bot = TelegramBot(token=bot_token)
    bot.run()
