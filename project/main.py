import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
from project.models.IssueLurker import IssueLurker

load_dotenv()
client_token = os.environ['TELEGRAM_TOKEN']
logging.basicConfig(level=logging.INFO)
bot = Bot(token=client_token)
dp = Dispatcher(bot, storage=MemoryStorage())
searcher = IssueLurker()
token = os.getenv('GITHUB_TOKEN')
searcher.initialize_token(token)
storage = {'username': '', 'links': []}


class IssueSearcher(StatesGroup):
    waiting_for_links = State()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет, я бот который поможет тебе быстро и удобно искать issues для open-source contributing")
    await message.reply("Вот список команд которые я умею: "
                        "\n/setLinksToSearch - Добавить репозитории которые вы хотите"
                        "\n/startSearching - Начать поиск по списку ваших репозиторий")


@dp.message_handler(commands=['setLinksToSearch'])
async def set_links_to_search(message: types.Message):
    await message.reply("Введите ссылку на репозиторий, убедитесь что вводите свою ссылку в формате:\n"
                                "'https://www.github.com/repo_owner/repo")
    await IssueSearcher.waiting_for_links.set()


@dp.message_handler(commands=['startSearching'])
async def start(message: types.Message):
    if len(storage['links']) > 0:
        for link in storage['links']:
            if searcher.get_links_to_search(link):
                await message.reply("Ссылкa добавленa")
            else:
                await message.reply("Что то пошло не так, убедитесь что вводите свою ссылку в формате:\n"
                                    "'https://www.github.com/repo_owner/repo")
        await message.reply("Ссылки добавлены, начинаю поиск")
        tmp = ['Cсылки:']
        tmp.append(searcher.get_query())
        print(tmp)
        for i in tmp:
            await message.reply(i)
    else:
        await message.reply("К сожалению вы не вставили никаких ссылок,\n"
                      "Пожалуйста введите ссылку(и):")
        await IssueSearcher.waiting_for_links.set()


@dp.message_handler(state=IssueSearcher.waiting_for_links)
async def set_links(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['links'] = []
        if message.text != 'stop' and searcher.validate_link(message.text):
            data['links'].append(message.text)
            storage['links'].extend(data['links'])
            await message.reply('Ссылка успешно добавлена')
            await IssueSearcher.waiting_for_links.set()
        else:
            await message.reply('Чтобы начать поиск по репозиториям введите команду: /startSearching')
            await state.update_data(links=data['links'])
            await state.finish()

    print(storage['links'])


@dp.message_handler()
async def process_other_messages(message: types.Message):
    await message.answer("Введите команду /start для начала работы")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
