from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
import requests

API_TOKEN = '7227515766:AAFIfZ2fSbSLVgZX3NbmkYkoTE773Iw1odg'  # Bu yerda botning API tokenini kiriting
TMDB_API_KEY = 'd04fb5df42595348550c3830e92b84c9'  # Agar TMDB'dan foydalanmoqchi bo'lsangiz

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())  # FSM uchun MemoryStorage ishlatish

# Holatlarni saqlash uchun FSM (Finite State Machine)
class MovieState(StatesGroup):
    waiting_for_movie_name = State()

# Kinoni topish funksiyasi (TMDB API'dan foydalanib)
def search_movie(movie_name):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_name}"
    response = requests.get(url)
    data = response.json()
    
    if data['results']:
        movie = data['results'][0]
        title = movie['title']
        overview = movie.get('overview', 'No description available.')
        release_date = movie.get('release_date', 'Unknown release date.')
        return f"Title: {title}\nOverview: {overview}\nRelease Date: {release_date}"
    return "Movie not found."

# Botdan foydalanish uchun start buyrug'i
@dp.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    await message.answer("Salom! Menga biror inglizcha kino nomini yozing, men sizga kinoning ma'lumotini yuboraman.")
    await state.set_state(MovieState.waiting_for_movie_name)  # Holatni o'zgartirish

# Foydalanuvchi kino nomini kiritganda
@dp.message(MovieState.waiting_for_movie_name)
async def movie_name_handler(message: Message, state: FSMContext):
    movie_name = message.text
    await message.answer("Kino qidirilmoqda...")

    # Kino nomi asosida ma'lumot olish
    movie_info = search_movie(movie_name)
    
    await message.answer(movie_info)
    await state.clear()

if __name__ == "__main__":
    dp.run_polling(bot)
