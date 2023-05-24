# -*- coding: utf-8 -*-
from padatious import IntentContainer
from glob import glob
from os.path import basename
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

container = IntentContainer('intent_cache')
for file_name in glob(f'vocab/*.intent'):
    name = basename(file_name).replace('.intent', '')
    container.load_intent(name, file_name)

for file_name in glob(f'vocab/*.entity'):
    name = basename(file_name).replace('.entity', '')
    container.load_entity(name, file_name)
container.train()


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


app = ApplicationBuilder().token("YOUR TOKEN HERE").build()

app.add_handler(CommandHandler("hello", hello))

app.run_polling()