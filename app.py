import chainlit as cl
import openai
from utils.openai_utils import get_completion_from_messages, execute_function_call


@cl.on_chat_start
async def start():
    await cl.Avatar(
        name="afs-bot",
        url="https://i.ibb.co/xC7qST7/logo-1.png",
    ).send()

    await cl.Message(
        content="🤖 Ahoy ! Welcome to AFS Chat ! 💬\nHow can I assist?",
        author="afs-bot",
    ).send()


# setting up system message and context

system_message = f"""Your are a chatbot named AFS Chat and your objective is to give the user \
the information they asked based on the information you have.If you find that to give the answer \
you don't have sufficient information, you use the available functions. While using function calling, \
Don't make assumptions about what values to plug into functions.Ask follow up questions if you need \
to get the function parameter. Observe the conversation and find appropriate \
function and its parameter.Ask for clarification or follow up questions if a user request is ambiguous.\
If you still don't have specific functions or information,  then  just politely answer that you \
don't know the answer and you must not make anything up! Also, you are a chatbot for restaurant.So, you must crosscheck \
user's questions and only answer relevant questions associated with restaurants. Else, you ask the user \
to ask relevant questions only and don't respond to any irrelevant questions.Let's go step by step"""


global context
context = [{"role": "system", "content": system_message}]


# cost calculation

TOTAL_COST = 0


def calculate_cost(prompt_tokens, completion_tokens):
    CHARGE_PER_PROMPT_TOKEN = 0.0015 / 1000
    CHARGE_PER_COMPLETION_TOKEN = 0.002 / 1000
    global TOTAL_COST
    

    DOLLAR_TO_TAKA = 108

    prompt_charge = prompt_tokens * CHARGE_PER_PROMPT_TOKEN * DOLLAR_TO_TAKA
    completion_charge = completion_tokens * CHARGE_PER_COMPLETION_TOKEN * DOLLAR_TO_TAKA
    TOTAL_COST += prompt_charge + completion_charge


@cl.on_message
async def main(message: str):
    context.append({"role": "user", "content": message})
    response, prompt_tokens, completion_tokens = get_completion_from_messages(context)
    calculate_cost(prompt_tokens, completion_tokens)

    if response.get("function_call"):
        context.append(response)
        results = execute_function_call(response)
        context.append(
            {
                "role": "function",
                "content": results,
                "name": response["function_call"]["name"],
            }
        )

        second_response = openai.ChatCompletion.create(
            # model="gpt-4-0613",
            model="gpt-3.5-turbo-0613",
            messages=context,
            temperature=0,
        )
        context.append(
            {"role": "assistant", "content": second_response.choices[0].message.content}
        )
        calculate_cost(
            second_response.usage.prompt_tokens, second_response.usage.completion_tokens
        )

    else:
        context.append({"role": "assistant", "content": response.content})

    reply_content = (
        f"{context[-1]['content']}  Used Thus Far: **{TOTAL_COST:.2f} Taka** Prompt Token: {prompt_tokens} Completion Token:{completion_tokens}"
    )
    await cl.Message(content=reply_content, author="afs-bot").send()
