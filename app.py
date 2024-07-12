import telebot
from data.config import TOKEN, pattern
from data.db import Data
from components.agent import Agent
from components.textTools import get_simple_markdown
from components.tools import get_product_info, tell_about_contacts, tell_about_delivAndPayment
import Levenshtein

agent = Agent(
    name="Candy store Assistant",
    personality="Im a laTorta store consultant",
    tools={
        get_product_info.__name__: get_product_info,
        tell_about_contacts.__name__:tell_about_contacts,
        tell_about_delivAndPayment.__name__:tell_about_delivAndPayment
    },
    allData=Data(path='./data/ResultFile.json')
)
bot = telebot.TeleBot(TOKEN)
agent.create_thread()
@bot.message_handler(content_types=['text'])

def test(message):
    print("=========== start =======================")

    agent.add_message(message.text)
    bot.send_message(message.chat.id, get_simple_markdown(pattern, agent.run_agent()), parse_mode='Markdown')

    print("=========== done  =======================")

bot.polling(non_stop=True)