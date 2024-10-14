import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage

API_TOKEN = '7227515766:AAFIfZ2fSbSLVgZX3NbmkYkoTE773Iw1odg'
TMDB_API_KEY = 'd04fb5df42595348550c3830e92b84c9'  # Replace with your TMDB API key
SEARCH_URL = 'https://api.themoviedb.org/3/search/movie'  # TMDb search endpoint
MEDIA_URL = 'https://api.themoviedb.org/3/movie/{movie_id}/videos'  # TMDb video endpoint

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# FSM for storing movie search states
class MovieState(StatesGroup):
    waiting_for_movie_name = State()

# Function to search for movies using TMDb API
def search_movie(movie_name):
    params = {
        'api_key': TMDB_API_KEY,
        'query': movie_name,
        'language': 'en-US',
        'page': 1
    }
    response = requests.get(SEARCH_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            return [(movie['title'], movie['id']) for movie in data['results']]
    
    return []

# Function to fetch movie media using TMDb API
def fetch_movie_media(movie_id):
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'en-US'
    }
    response = requests.get(MEDIA_URL.format(movie_id=movie_id), params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            # Assuming we want the first video for simplicity
            video = data['results'][0]
            return f"https://www.youtube.com/watch?v={video['key']}"  # You can adjust this based on the video source
    
    return "Media not found."

# /start command handler
@dp.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    await message.answer("Salom! Menga biror kino nomini yozing, men sizga kinoning ma'lumotini yuboraman.")
    await state.set_state(MovieState.waiting_for_movie_name)

# Handling the movie name input and sending movie titles as buttons
@dp.message(MovieState.waiting_for_movie_name)
async def movie_name_handler(message: Message, state: FSMContext):
    movie_name = message.text
    await message.answer("Kino qidirilmoqda...")

    # Fetch movie titles and IDs
    movies = search_movie(movie_name)
    
    if movies:
        # Har bir tugmachani alohida ro'yxat sifatida qo'shamiz
        buttons = [[InlineKeyboardButton(text=title, callback_data=str(movie_id))] for title, movie_id in movies]
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)  # InlineKeyboardMarkupni to'g'ri yaratish
        await message.answer("Tanlang:", reply_markup=keyboard)
    else:
        await message.answer("Kino topilmadi.")

    await state.clear()

# Handling button clicks for movie media
@dp.callback_query(lambda c: c.data.isdigit())
async def process_movie_selection(callback_query: types.CallbackQuery):
    movie_id = int(callback_query.data)
    media_info = fetch_movie_media(movie_id)
    
    await callback_query.answer()  # Acknowledge the callback
    await callback_query.message.answer(media_info)

if __name__ == "__main__":
    dp.run_polling(bot)
