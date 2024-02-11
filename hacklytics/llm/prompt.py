import openai
from ..settings import client
from .prompt_response import PromptResponse
from string import Template
from .prompt_constants import FIRE_ANSWER, FIRE_TEXT, PROMPT_MESSAGE, TORNADO_TEXT, TORNADO_ANSWER, FLOOD_ANSWER, FLOOD_TEXT, TREE_ANSWER, TREE_TEXT
import re


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
    response = client.chat.completions.create(
        model='gpt-4',
        messages=[{'role':'user', 'content':prompt}]
    )
    return response.choices[0].message.content.strip()

def create_prompt_response_helper(response_part):
    index = response_part.find(':')
    return response_part[index+1:]

def create_prompt_response(text, response):
    response_list = response.split('\n\n')
    summary = get_completion_overall_health(text)
    immediate_issues = create_prompt_response_helper(response_list[0])
    immediate_fixes = create_prompt_response_helper(response_list[1])
    longterm_issues = create_prompt_response_helper(response_list[2])
    longterm_fixes = create_prompt_response_helper(response_list[3])
    top_three_recommendations = get_completion_top_three_insights(summary, immediate_issues, immediate_fixes, longterm_issues, longterm_fixes)
    return PromptResponse(summary, immediate_issues, immediate_fixes, longterm_issues, longterm_fixes, top_three_recommendations)

def get_issues_and_fixes(text):
    prompt = construct_prompt(text)
    response = make_api_call(prompt)
    return create_prompt_response(text, response)

def get_completion_standalone(text):

    customer_query = ""

    for line in text:
        print(line)
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

def get_completion_overall_health(text):
    messages = [
        {
            "role": "system",
            "content": """You are an assistant for a home insurance company. You are tasked with assisting your boss in summarizing the overall health of the house. You will be provided with
            a description of all the damages that has happened to the house, and you have to summarize the overall health of the house.
            
            """
        },
        {
            "role": "user",
            "content": f"""Here is the damage description: {text}"""
        }
    ]

    response = client.chat.completions.create(
        model='gpt-4',
        messages=messages,
        temperature=0
    )

    return response.choices[0].message.content.strip()

def get_completion_top_three_insights(summary, immediate_issues, immediate_fixes, longterm_issues, longterm_fixes):
    messages = [
        {
            "role": "system",
            "content": f"""You are an assistant for a home insurance company. You are tasked with assisting your boss in generating the top three insights as tailored maintenance and protection recommendations for the homeowners, based
            on the individual condition of their house. You will be provided with the following information about the house condition:

            1. A summary of the overall health of the house extracted from photography and text data. {summary}
            
            2. Few issues that needs to be addressed immediately. {immediate_issues}
            
            3. Fixes for the immediate issues. {immediate_fixes}
            4. Few issues that are likely to arise in long term within a 3-6 month time frame.  {longterm_issues}

            5. Fixes for the long term issues. {longterm_fixes}
            
            """
        },
        {
            "role": "user",
            "content": f"""Generate the top three insights as tailored maintenance and protection recommendations for my house. GENERATE THE OUTPUT AS 3 PARAGRAPHS"""
        }
    ]

    response = client.chat.completions.create(
        model='gpt-4',
        messages=messages,
        temperature=0
    )

    
    # pattern = r'\d\.\s\*\*(.*?)\*\*:\s'

    # # Splitting the text into bullet points
    # bullet_points = re.split(pattern, response.choices[0].message.content.strip())[1:]  # Discard the first element if it's empty

    # # Grouping titles with their respective content
    # bullet_points_list = ['-**' + bullet_points[i] + '**: ' + bullet_points[i + 1].strip() for i in range(0, len(bullet_points), 2)]

    
    
    # # pattern = r'\d\.\s\*\*(.*?)\*\*:'

    # # # Replace matched patterns with bullet points and a newline for readability
    # # bullet_points = re.sub(pattern, r'\n- \1:', )

    # print(bullet_points_list)

    return response.choices[0].message.content.strip()