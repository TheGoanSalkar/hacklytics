import openai
from ..settings import OPENAI_KEY
from .prompt_response import PromptResponse
from string import Template
from .prompt_constants import FIRE_ANSWER, FIRE_TEXT, PROMPT_MESSAGE, TORNADO_TEXT, TORNADO_ANSWER, FLOOD_ANSWER, FLOOD_TEXT, TREE_ANSWER, TREE_TEXT

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
    tornado_prompt = prompt_template.substitute(question=TORNADO_TEXT, answer=TORNADO_ANSWER)
    flood_prompt = prompt_template.substitute(question=FLOOD_TEXT, answer=FLOOD_ANSWER)
    tree_prompt = prompt_template.substitute(question=TREE_TEXT, answer=TREE_ANSWER)
    text_prompt = prompt_template.substitute(question=text, answer=PROMPT_MESSAGE)
    prompt = fire_prompt + '\n\n' + tornado_prompt +  '\n\n' + flood_prompt + '\n\n' + tree_prompt + '\n\n' + text_prompt
    return prompt

def make_api_call(prompt):
    openai.api_key = OPENAI_KEY
    response = openai.chat.completions.create(
        model='gpt-3.5-turbo',
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
