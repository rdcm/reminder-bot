"""Telegram reminder bot."""

import os
from dataclasses import dataclass
import yaml
from apscheduler.triggers.cron import CronTrigger

from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CallbackContext,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)


@dataclass
class AppConfig:
    """Application config"""

    tasks: list


async def on_start(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def on_help(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def on_fallback(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


async def notify_job(context: CallbackContext, chat_id, text):
    """Sends a notification to a chat."""
    await context.bot.send_message(chat_id=chat_id, text=text)


def load_config(config_file):
    """Load application configuration."""
    with open(config_file, mode="r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    return map_config_to_model(config)


def map_config_to_model(config):
    """Map configuration to dataclass."""
    return AppConfig(tasks=config.get("tasks", []))


def main() -> None:
    """Start the bot."""

    config = load_config("config.yaml")

    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", on_start))
    application.add_handler(CommandHandler("help", on_help))

    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, on_fallback)
    )

    for task in config.tasks:
        application.job_queue.run_custom(
            lambda ctx, task=task: notify_job(ctx, chat_id, task.get("text")),
            job_kwargs={
                "trigger": CronTrigger.from_crontab(task.get("cron")),
            },
        )

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
