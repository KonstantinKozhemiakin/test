import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import pprint
import json

file = open('config.json', 'r')
config = json.load(file)

openai.api_key = config['openai']
bot = Bot(config['token'])
dp = Dispatcher(bot)

messages = [
    {"role": "system",
     "content": "You are a recruiter who is testing a candidate for the position of lead generator. Create a list of different questions on topics such as: Online marketing, Lead generation, Search engine optimization (SEO), Pay-per-click (PPC) advertising, Social media marketing, Website design and development, Customer relationship management (CRM). For each question, create a multiple-choice answer with one correct answer and two or three incorrect answers. Ask questions from the list in turn, accepting one answer at a time. After the candidate completes 10 tests, evaluate his performance by calculating the percentage of correct answers on the ten questions."},
    {"role": "user",
     "content": "I am a candidate for the position of lead generator, I want you to determine my level of knowledge"},
    {"role": "assistant", "content": "Greetings! Are you ready to take the test?"}]


def update(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Welcome! In this evaluation, we will assess your skills as a lead generation specialist.")


@dp.message_handler()
async def send(message: types.Message):
    global messages
    messages = update(messages, "user", message.text)
    print(messages)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
        # temperature=0.1
    )
    await message.answer(response['choices'][0]['message']['content'])
    messages = update(messages, "assistant", response['choices'][0]['message']['content'])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
