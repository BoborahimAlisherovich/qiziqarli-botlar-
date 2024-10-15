# Botga /start kamandasini yozib qidirmoqchi bulgan narsangizni yozasiz u sizga topib beradi 
# lekn kanal likni uzingiz quyasiz

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage

API_TOKEN = '7227515766:AAFIfZ2fSbSLVgZX3NbmkYkoTE773Iw1odg'
CHANNEL_ID = 'https://t.me/Inglizcha_kinolar_multfilm'  # Telegram kanal nomi yoki ID'si


bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Holatlarni saqlash uchun FSM (Finite State Machine)
class MovieState(StatesGroup):
    waiting_for_movie_name = State()

# Botdan foydalanish uchun start buyrug'i
@dp.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    await message.answer("Salom! Menga biror kino nomini yozing, men sizga kinoni yuboraman.")
    await state.set_state(MovieState.waiting_for_movie_name)

# Foydalanuvchi kino nomini kiritganda
@dp.message(MovieState.waiting_for_movie_name)
async def movie_name_handler(message: types.Message, state: FSMContext):
    movie_name = message.text.lower()
    await message.answer(f"'{movie_name}' kino qidirilmoqda...")

    try:
        async for msg in bot.get_chat_member(CHANNEL_ID, limit=100):
            if movie_name in msg.text.lower():
                await message.answer(f"Kino topildi: {msg.text}")
                if msg.video:
                    await bot.send_video(message.chat.id, msg.video.file_id)
                elif msg.document:
                        await bot.send_document(message.chat.id, msg.document.file_id)
                await state.clear()
                return

        await message.answer("Afsus, kino topilmadi.")
    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {str(e)}")

    await state.clear()

if __name__ == "__main__":
    dp.run_polling(bot)
