# TODO
# Scriptas, kuris is userio atsakymo i boto uzduota klausima
# istraukia features, kuris toliau naudojamas system promptuose

import ollama
import os

def read_file(user_id):
    data_path = os.path.abspath("..\\data\\features\\")
    filename = user_id

    data_file = f"{data_path}\\{filename}.txt"

    try:
        with open(data_file, 'r') as file:
            text_content = file.read()
    
    except FileNotFoundError:
        text_content = ''

    return text_content

def write_features(user_id, data):
    data_path = os.path.abspath("..\\data\\features\\")
    filename = user_id

    data_file = f"{data_path}\\{filename}.txt"

    with open(data_file, 'w') as file:
        file.write(data)

def extract_features(user_id, data):

    existing_features = read_file(user_id)

    response = ollama.chat(
        model='llama3.2',
        messages=[
            {
            'role': 'system',
            'content': '''you will be provided with data about a persons work field, 
            domain and other work information, personal traits, main functions, hobbies, 
            dislikes, tone of chatting and other similar features. by referencing this 
            information, you have to make a feature map of this user so it can be used for creating
            a digital clone for task automation and communication with clients. do not output any
            additive information and only display features divided into these three groups: 
            all main personal details such as name, contact information, location, etc.;
            professional expertise, soft and technical skills, field, domain and main functions;
            communication style, personality traits, tone, slang and general vibe; main tasks or
            goals that are wanted to be achieved by using this application.'''
            },
            {
            'role': 'user',
            'content': existing_features,
            },
            # {
            # 'role': 'agent',
            # 'content': 'Do you conscent to let me store your personal data to perform your wanted functions?',
            # },
            # {
            # 'role': 'user',
            # 'content': 'yes i do',
            # },
            {
            'role': 'agent',
            'content': 'What else can you tell me about yourself?',
            },
            {
            'role': 'user',
            'content': data,
            }
        ]
    )

    feature_map = f'\n{response['message']['content']}'

    write_features(user_id, feature_map)

    print(feature_map)

aboutme = 'i am working from vilnius on tuesdays. i do personal trainings and make meal and sport programs'
extract_features('joshua', aboutme)