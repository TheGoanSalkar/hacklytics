import openai
from ..settings import OPENAI_KEY
from .prompt_response import PromptResponse
from string import Template
from .prompt_constants import FIRE_ANSWER, FIRE_TEXT, PROMPT_MESSAGE

prompt_template = Template('''
$question

Answer :

$answer
''')

response_template = '''
Immediate Issues : $immediateIssues

Immediate Fixes : $immediateFixes

Long-term Issues : $longtermIssues

Long-term Fixes : $longtermFixes
'''

def construct_prompt(text):
    fire_prompt = prompt_template.substitute(question=FIRE_TEXT, answer=FIRE_ANSWER)
    text_prompt = prompt_template.substitute(question=text, answer=PROMPT_MESSAGE)
    prompt = fire_prompt + '\n\n' + text_prompt
    return prompt

def make_api_call(prompt):
    response = client.chat.completions.create(
        model='gpt-4',
        messages=[{'role':'user', 'content':prompt}]
    )
    return response.choices[0].message.content.strip()

def create_prompt_response_helper(response_part):
    index = response_part.find(':')
    return response_part[index+1:]

def create_prompt_response(response):
    response_list = response.split('\n\n')
    immediate_issues = create_prompt_response_helper(response_list[0])
    immediate_fixes = create_prompt_response_helper(response_list[1])
    longterm_issues = create_prompt_response_helper(response_list[2])
    longterm_fixes = create_prompt_response_helper(response_list[3])
    return PromptResponse(immediate_issues, immediate_fixes, longterm_issues, longterm_fixes)

def get_issues_and_fixes(text):
    prompt = construct_prompt(text)
    response = make_api_call(prompt)
    return create_prompt_response(response)

def get_completion_standalone(text):

    customer_query = ""

    for line in text:
        customer_query += line + "\n"

    messages = [
        {
            "role": "system",
            "content": """You are an assistant for a home insurance company. You are tasked with assisting your boss in resonponding to a customer's query. The customer has recently experienced a disaster 
            and has provided you what all has happened in the form of few sentences. You should summarize the customer's query in detail and explain it to your boss.
            
            """
        },
        {
            "role": "user",
            "content": f"""Here is the customer query: {customer_query}"""
        }
    ]

    response = client.chat.completions.create(
        model='gpt-4',
        messages=messages,
        temperature=0
    )

    return response.choices[0].message.content.strip()
