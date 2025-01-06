import asyncio
import logging
import signal

from telegram.ext import (Application, ApplicationBuilder, CommandHandler,
                          MessageHandler, filters)

from config import settings
from database import create_all
from handlers import (answer_trip_handler, calendar, start_handler,
                      trip_handler, welcome_new_member)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

application = ApplicationBuilder().token(settings.TG_TOKEN).build()
application.add_handler(CommandHandler('start', start_handler))
application.add_handler(CommandHandler('trip', trip_handler))
application.add_handler(CommandHandler('calendar', calendar))
application.add_handler(MessageHandler(filters.TEXT, answer_trip_handler))
application.add_handler(MessageHandler(
        filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member
    )
)
stop_event = asyncio.Event()


async def run_polling(application: Application):
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(
            sig, lambda: asyncio.create_task(shutdown(application))
        )
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    logging.info("Bot started. Press Ctrl+C to stop.")
    await stop_event.wait()
    await application.stop()
    await application.shutdown()


async def shutdown(application: Application):
    """Gracefully shut down the application."""
    logging.info("Received stop signal, shutting down...")
    stop_event.set()

async def main():
    await create_all()
    await run_polling(application)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())

