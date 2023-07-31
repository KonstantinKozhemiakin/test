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
     "content": '''As a recruiter, you should conduct multiple-choice tests to assess the knowledge and skills of a Lead Generation Manager candidate. 
Ask random questions on these topics:
		Lead Generation Manager / Researcher
        International sales of software services
        Outstaff and Outsource
        LinkedIn and Email outreach
        Software development stages (Web and Mobile)
        Written English (Intermediate)
        Attention to detail
        Automation and data management tools (Apollo, Instantly, Zaper, Linked-helper, etc.)
        Tech stack
        IT Outsourcing company
        LinkedIn Sales Navigator, Clutch, Upwork, PipeDrive
        English level B2+ or C1
        Lead-gen (outstaffing / outsourcing)
        Lead-gen tools
        Email outreach
        IT technologies
        B2B sales experience
        CRM systems
        Upwork, FB, AngelList, PPH
        Automation tools (Snovio, GrowthLead, Lemlist, etc.)
        Presales Mastery
        Google Workspace, Snov.io, Findthatlead, Crunchbase
        IT lead generator
        Black humor and sarcasm
        B2B CSM experience
        GigRadar, Upwork
        SDLC (Software Development Life Cycle)
        English (Upper-Intermediate or above)
        Result-driven
        ICP (Ideal Customer Profile)
        IT outsourcing services
        B2B lead generation
        CRM management
        Market research and trends
        Team management
        Analytical skills
        Goal-driven and results-oriented.
After 10 answers avaluate the candidate by the percentage of correct answers'''},
    {"role": "user",
     "content": "I am a candidate for the position of lead generator, I want you to determine my level of knowledge"},
    {"role": "assistant", "content": "Greetings! Are you ready to take the test?"}]


def update(message, role, content):
    messages.append({"role": role, "content": content})
    return messages


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Welcome! In this evaluation, we will assess your skills as a lead generation specialist.")


@dp.message_handler()
async def send(message: types.Message):
    update(messages, "user", message.text)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
        #temperature=0.9

    )
    await message.answer(response['choices'][0]['message']['content'])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
