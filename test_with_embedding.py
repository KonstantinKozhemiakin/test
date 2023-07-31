from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from lgs import lead_generation_skills
import numpy as np
import json

import openai

file = open('config.json', 'r')
config = json.load(file)

openai.api_key = config['openai']
bot = Bot(config['token'])
dp = Dispatcher(bot)

user_states = {}


def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']


def similarity(v1, v2):
    return np.dot(v1, v2)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    user_states[user_id] = {'messages': []}
    await message.reply("Welcome! Please describe your experience as a lead generator.")


@dp.message_handler()
async def send(message: types.Message):
    user_id = message.from_user.id

    # Check if the user_id exists in user_states dictionary, if not initialize it
    if user_id not in user_states:
        user_states[user_id] = {'messages': []}

    user_data = user_states[user_id]

    user_data['messages'].append(message.text.strip())
    print(len(user_data['messages']))

    if len(user_data['messages']) >= 2:
        if len(user_data['messages']) > 2:
            user_data['messages'] = user_data['messages'][-2:]  # Keep only the last two messages

        lead_generation_skills_embedding = get_embedding(lead_generation_skills)

        candidate_skills_embedding = get_embedding(user_data['messages'][1])
        sim = str(similarity(lead_generation_skills_embedding, candidate_skills_embedding))
        await message.answer("Similarity with lead generation skills: " + sim)
    else:
        await message.answer("Please provide more information about your experience as a lead generator.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
