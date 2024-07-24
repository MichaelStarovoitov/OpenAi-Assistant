import telebot
from data.config import TOKEN, pattern
from components.db import Data
from components.agent import Agent
from components.textTools import get_simple_markdown
from components.tools import get_product_info, tell_about_contacts, tell_about_delivAndPayment
import Levenshtein

print("agent")

agent = Agent(
    name="Помічник у кондитерській",
    personality="Ти помічник кондитерського магазину LaTorta.  Дані для відповіді на запит користувача брати тільки з instructions: Metadata related to this conversation. Відповідати завжди українською мовою.",
    tools={
        get_product_info.__name__: get_product_info,
        tell_about_contacts.__name__:tell_about_contacts,
        tell_about_delivAndPayment.__name__:tell_about_delivAndPayment
    },
    allData=Data(path='./data/Result/ResultFile.json')
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