# IQ  testni aniqlash uchun

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import asyncio
import random

API_TOKEN = '7227515766:AAFIfZ2fSbSLVgZX3NbmkYkoTE773Iw1odg'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# 30 ta IQ savollari va javoblari
questions = [
    {"savol": "2 + 2 = ?", "javoblar": ["3", "4", "5"], "to'g'ri": 1},
    {"savol": "5 x 3 = ?", "javoblar": ["15", "20", "10"], "to'g'ri": 0},
    {"savol": "Qaysi biri hayvon?", "javoblar": ["Olma", "Fil", "Stol"], "to'g'ri": 1},
    {"savol": "12 - 4 = ?", "javoblar": ["6", "8", "9"], "to'g'ri": 1},
    {"savol": "3 + 5 = ?", "javoblar": ["7", "8", "9"], "to'g'ri": 1},
    {"savol": "Qaysi biri poytaxt?", "javoblar": ["Nyu York", "London", "Parij"], "to'g'ri": 2},
    {"savol": "Qaysi biri dasturlash tili?", "javoblar": ["Python", "HTML", "CSS"], "to'g'ri": 0},
    {"savol": "6 x 7 = ?", "javoblar": ["42", "36", "49"], "to'g'ri": 0},
    {"savol": "1 + 1 = ?", "javoblar": ["2", "3", "4"], "to'g'ri": 0},
    {"savol": "7 + 6 = ?", "javoblar": ["13", "12", "14"], "to'g'ri": 0},
    # Qo'shimcha 20 ta savol qo'shilgan
    {"savol": "9 + 1 = ?", "javoblar": ["10", "11", "9"], "to'g'ri": 0},
    {"savol": "3 + 9 = ?", "javoblar": ["11", "12", "13"], "to'g'ri": 1},
    {"savol": "4 + 7 = ?", "javoblar": ["10", "11", "12"], "to'g'ri": 1},
    {"savol": "5 x 2 = ?", "javoblar": ["10", "15", "20"], "to'g'ri": 0},
    {"savol": "20 / 5 = ?", "javoblar": ["4", "3", "5"], "to'g'ri": 0},
    {"savol": "8 x 2 = ?", "javoblar": ["16", "18", "20"], "to'g'ri": 0},
    {"savol": "100 - 50 = ?", "javoblar": ["60", "50", "40"], "to'g'ri": 1},
    {"savol": "6 x 8 = ?", "javoblar": ["48", "42", "56"], "to'g'ri": 0},
    {"savol": "3 + 7 = ?", "javoblar": ["9", "10", "11"], "to'g'ri": 1},
    {"savol": "1 + 0 = ?", "javoblar": ["1", "2", "0"], "to'g'ri": 0},
    {"savol": "Qaysi biri dasturlash tili?", "javoblar": ["CSS", "Java", "Photoshop"], "to'g'ri": 1},
    {"savol": "4 + 4 = ?", "javoblar": ["7", "8", "9"], "to'g'ri": 1},
    {"savol": "2 x 10 = ?", "javoblar": ["20", "15", "30"], "to'g'ri": 0},
    {"savol": "20 - 5 = ?", "javoblar": ["15", "16", "14"], "to'g'ri": 0},
    {"savol": "3 x 5 = ?", "javoblar": ["15", "18", "12"], "to'g'ri": 0},
    {"savol": "50 / 10 = ?", "javoblar": ["4", "5", "6"], "to'g'ri": 1},
    {"savol": "3 + 2 = ?", "javoblar": ["5", "4", "6"], "to'g'ri": 0},
    {"savol": "6 x 6 = ?", "javoblar": ["36", "30", "42"], "to'g'ri": 0},
    {"savol": "7 x 5 = ?", "javoblar": ["35", "30", "25"], "to'g'ri": 0},
]
user_scores = {}

@dp.message(Command('start'))
async def start(message: Message):
    user_scores[message.from_user.id] = {"current_question": 0, "score": 0, "shuffled_questions": []}
    await message.answer("Assalomu alaykum! IQ test boshlash uchun /test buyrug'ini yozing.")

@dp.message(Command('test'))
async def start_test(message: Message):
    random.shuffle(questions)
    user_scores[message.from_user.id]["shuffled_questions"] = questions[:]
    user_scores[message.from_user.id]["current_question"] = 0
    user_scores[message.from_user.id]["score"] = 0
    await send_question(message)

async def send_question(message: Message):
    user_data = user_scores[message.from_user.id]
    current_question = user_data["current_question"]
    total_questions = len(user_data["shuffled_questions"])

    if current_question < total_questions:
        question = user_data["shuffled_questions"][current_question]
        
        await message.answer(f"Savol {current_question + 1}/{total_questions}:")
        
        builder = ReplyKeyboardBuilder()
        for idx, javob in enumerate(question["javoblar"]):
            builder.button(text=javob)
        
        markup = builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
        question_msg = await message.answer(f"Savol: {question['savol']}\n5 soniya ichida javob bering!", reply_markup=markup)
        
        # Orqaga sanashni bitta xabar ichida ko'rsatish
        for i in range(5, 0, -1):
            await asyncio.sleep(1)  # Har bir soniyani kutish
            try:
                await bot.edit_message_text(f"Qolgan vaqt: {i} soniya", chat_id=message.chat.id, message_id=question_msg.message_id)
            except Exception as e:
                print(e)

        # Agar foydalanuvchi javob bermagan bo'lsa, keyingi savolga o'tish
        if user_scores[message.from_user.id]["current_question"] == current_question:
            await message.answer("Vaqt tugadi! Keyingi savolga o'tamiz.")
            user_scores[message.from_user.id]["current_question"] += 1
            await send_question(message)
    else:
        await end_test(message)

@dp.message()
async def check_answer(message: Message):
    user_data = user_scores.get(message.from_user.id, None)
    if not user_data:
        await message.answer("Testni boshlash uchun /test buyrug'ini yozing.")
        return

    current_question = user_data["current_question"]
    question = user_data["shuffled_questions"][current_question]

    if message.text == question["javoblar"][question["to'g'ri"]]:
        user_scores[message.from_user.id]["score"] += 1
        await message.answer("To'g'ri javob!")
    else:
        await message.answer("Notog'ri javob.")

    user_scores[message.from_user.id]["current_question"] += 1
    await send_question(message)

async def end_test(message: Message):
    score = user_scores[message.from_user.id]["score"]
    total_questions = len(user_scores[message.from_user.id]["shuffled_questions"])
    percentage = (score / total_questions) * 100
    await message.answer(f"Test yakunlandi! Sizning natijangiz: {score}/{total_questions} ({percentage:.2f}%)")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())