import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile
from aiohttp import web  # Добавляем для открытия порта на Render

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = "8959804118:AAHWlw4mBRWBErt1WmMykhlqRIKf-Mzs4Io"
dp = Dispatcher()

@dp.update()
async def handle_everything(update: types.Update):
    chat_id = None
    is_clown = False

    if update.message_reaction:
        chat_id = update.message_reaction.chat.id
        new_reactions = update.message_reaction.new_reaction
        if new_reactions:
            last_reaction = new_reactions[-1]
            if isinstance(last_reaction, types.ReactionTypeEmoji) and last_reaction.emoji == "🤡":
                is_clown = True
            elif isinstance(last_reaction, types.ReactionTypeCustomEmoji):
                is_clown = True

    elif update.message_reaction_count:
        chat_id = update.message_reaction_count.chat.id
        reactions = update.message_reaction_count.reactions
        for r in reactions:
            if isinstance(r.type, types.ReactionTypeEmoji) and r.type.emoji == "🤡":
                is_clown = True
            elif isinstance(r.type, types.ReactionTypeCustomEmoji):
                is_clown = True

    if is_clown and chat_id:
        try:
            photo_file = FSInputFile("image.jpg")
            await update.bot.send_photo(
                chat_id=chat_id,
                photo=photo_file,
                caption="ВНИМАНИЕ!я нейродолбаеб и заметил что кто то из ботов,созданные @atumixs,отслеживает данный канал и ставит реакцию клоуна!Просьба закрыть код и не нагружать компьютер и интернет трафик!"
            )
            print("УСПЕШНО ОТПРАВЛЕНО!")
            return
        except Exception as e:
            print(f"ОШИБКА: {e}")

# Простейший веб-сервер, чтобы Render думал, что это сайт
async def handle_web(request):
    return web.Response(text="Bot is running!")

async def main():
    bot = Bot(token=BOT_TOKEN)
    
    # Запускаем бота в фоновом режиме
    asyncio.create_task(dp.start_polling(bot, allowed_updates=["message", "edited_message", "message_reaction", "message_reaction_count", "channel_post", "edited_channel_post"], skip_updates=True))
    
    # Открываем порт, который требует Render (по умолчанию 10000)
    app = web.Application()
    app.router.add_get("/", handle_web)
    
    port = int(os.environ.get("PORT", 10000))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    
    print(f"Веб-сервер запущен на порту {port}. Бот слушает реакции...")
    await site.start()
    
    # Держим программу запущенной бесконечно
    await asyncio.Event().wait()

if name == "main":
    asyncio.run(main())