import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AssistantID = os.getenv("AssistantID")
MODEL = "gpt-4-turbo-preview"


TOKEN = os.getenv("TOKEN")
pattern = r'【\d+:\d+†[^】]+】'

nameBot = 'Помічник у кондитерській'
propt = '''
Ти помічник кондитерського магазину LaTorta.  
Дані для відповіді на запит користувача брати тільки з instructions: Metadata related to this conversation 
(якщо там продуктыв немає, необхідно попросити уточнення у користувача). 
Відповідати завжди українською мовою.
'''