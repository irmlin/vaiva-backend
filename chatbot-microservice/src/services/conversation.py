# TODO
# chatbot interfeisas, system prompte pateikiama vartotojo features santrauka
# ir yra atsakinejama i userio uzduodamus klausimus. galbut atsakymus taip pat 
# formuoti informacija gaunant function calling budu


# DATA GATHERING (append the following to msg[])

# agent: hello, please answer some question so i could make a clone out of you. let me know when you think
# you gave me all your information

# user: hello, my answer is this

# << iskvieciamas feature extraction sitam atsakymui >>

# agent: ...

# PABAIGA NUTRAUKUS USERIUI, T.Y. KAI JIS ISJUNGIA PROGRAMA
# NUSPRENDES, KAD DAUGIAU INFORMACIJOS PATEIKTI NEBENORI

# ==================================================================================================
# ==================================================================================================

import ollama
import os

from fastapi import HTTPException, UploadFile
from fastapi.responses import FileResponse

def read_file(user_id):
    data_path = os.path.abspath("..\\data\\features\\")
    filename = user_id

    data_file = f"{data_path}\\{filename}.txt"
    with open(data_file, 'r') as file:
        text_content = file.read()

    return text_content

def send_message(user_id, messages, message):

    if(message['content'] == '/q'):
        return 0

    messages.append(message)

    print(messages)

    response = ollama.chat(
        model='llama3.2',
        messages=messages
    )

    answer = response['message']

    print(response['message']['content'])

    # call text-to-speech, video and audio models

    messages.append(answer)

    message = {
        'role': 'user',
        'content': input('Enter your message: ')
        }

    send_message(user_id, messages, message)

user_id = 'alex_morgan'
user_features = read_file(user_id)

messages=[
    {
    'role': 'system',
    'content': '''you will be provided data about a certain user. act like him referencing
    the given information. dont sound robotic or fake. answer questions
    you only know about from the data provided. if you dont know something,
    say that you dont know or that youll check and answer later.'''
    },
    {
    'role': 'system',
    'content': user_features
    }
]

user_input = input('Enter your message: ')

message={
    'role': 'user',
    'content': user_input
    }

print(message)

status = send_message('', messages, message)