from dotenv import load_dotenv
import os
from tenacity import retry, wait_random_exponential, stop_after_attempt
import utils.functions as func

load_dotenv()
import json
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
def get_completion_from_messages(messages, model="gpt-3.5-turbo-0613", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        functions=func.function_descriptions,
        function_call="auto",
    )
    #     print(str(response.choices[0].message))
    return (
        response.choices[0].message,
        response.usage.prompt_tokens,
        response.usage.completion_tokens,
    )


def execute_function_call(message):
    if message["function_call"]["name"] == "get_delivery_areas":
        if json.loads(message["function_call"]["arguments"]) != {}:
            branch_name = json.loads(message["function_call"]["arguments"])[
                "branch_name"
            ]
            results = func.get_delivery_areas(branch_name)
        else:
            results = func.get_delivery_areas()
    elif message["function_call"]["name"] == "extract_menu":
        if json.loads(message["function_call"]["arguments"]) != {}:
            branch_name = json.loads(message["function_call"]["arguments"])[
                "branch_name"
            ]
            results = func.extract_menu(branch_name)
    elif message["function_call"]["name"] == "get_branch_names":
        results = func.get_branch_names()
    else:
        results = f"Error: function {message['function_call']['name']} does not exist"
    return results
