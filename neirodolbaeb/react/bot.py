import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile

# 1. МЕНЯЕМ НА WARNING, чтобы убрать технический спам "is not handled"
logging.basicConfig(level=logging.WARNING)

# Токен вашего бота
BOT_TOKEN = "8959804118:AAECwkXspx5oKjheHglytzp9tCdfEBRBVsw"

# Создаем диспетчер событий
dp = Dispatcher()

# Этот перехватчик сработает при ЛЮБОМ чихе со стороны Telegram
@dp.update()
async def handle_everything(update: types.Update):
    # Эта строка ОБЯЗАНА напечататься в консоли, если Telegram вообще достучался до компьютера!
    print("\n[СИГНАЛ] Telegram прислал обновление на компьютер! Разбираем... [СИГНАЛ]")
    
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
        print(f"[!!!] КЛОУН НАЙДЕН В ЧАТЕ {chat_id}! Отправляем фото...")
        try:
            # Картинка обязательно должна быть в папке с ботом и называться image.jpg
            photo_file = FSInputFile("image.jpg")
            
            await update.bot.send_photo(
                chat_id=chat_id,
                photo=photo_file,
                caption="ВНИМАНИЕ!я нейродолбаеб и заметил что кто то из ботов,созданные @atumixs,отслеживает данный канал и ставит реакцию клоуна!Просьба закрыть код и нагружать компьютер и интернет трафик!"
            )
            print(">>> УСПЕШНО ОТПРАВЛЕНО В КАНАЛ! <<<\n")
            return
            
        except Exception as e:
            print(f"Ошибка при отправке файла: {e}\n")
    else:
        print("Это действие не связано с клоуном 🤡, игнорируем.\n")

# Главная функция запуска
async def main():
    bot = Bot(token=BOT_TOKEN)
    print("Бот успешно запущен и проверяет абсолютно все реакции...")
    
    # Запускаем опрос сервера Telegram
    await dp.start_polling(bot, allowed_updates=["message", "edited_message", "message_reaction", "message_reaction_count", "channel_post", "edited_channel_post"], skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())