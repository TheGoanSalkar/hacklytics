import os
from openai import OpenAI

OPENAI_KEY = os.environ.get('OPENAI_KEY')
client = OpenAI(api_key=OPENAI_KEY)