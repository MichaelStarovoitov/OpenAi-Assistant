import telebot
from data.config import TOKEN, pattern, propt, nameBot, resultFile
from components.db import Data
from components.agent import Agent
from components.textTools import get_simple_markdown
from components.tools import get_product_info, tell_about_contacts, tell_about_delivAndPayment
import Levenshtein



agent = Agent(
    name=nameBot,
    personality=propt,
    tools={
        get_product_info.__name__: get_product_info,
        tell_about_contacts.__name__:tell_about_contacts,
        tell_about_delivAndPayment.__name__:tell_about_delivAndPayment
    },
    allData=Data(path=resultFile)
)
print("agent Start")
bot = telebot.TeleBot(TOKEN)
agent.create_thread()
@bot.message_handler(content_types=['text'])

def test(message):
    print("=========== start =======================")
    print(message.text)
    agent.add_message(message.text)
    bot.send_message(message.chat.id, get_simple_markdown(pattern, agent.run_agent()), parse_mode='Markdown')

    print("=========== done  =======================")

bot.polling(non_stop=True)
print("agent Stop")