import ollama
import os
import time
import random

from fastapi import HTTPException, UploadFile
from fastapi.responses import FileResponse

class ConversationService:
    def __init__(self):
        self.__conv_prompt = f"{os.path.join('src', 'data')}/conversation_prompt.txt"
        self.__data_dir = os.path.join('src', 'data', 'features')
        self.__conv_dir = os.path.join('src', 'data', 'conversations')
        self.id = str(int(time.time()) + random.randint(1, 100))

    async def generate_id(self):
        self.id = str(int(time.time()) + random.randint(1, 100))

    # Returns specific users feature map (json: status;content.)
    async def get_features(self, username):
        file_path = f'{os.path.join(self.__data_dir, username)}.txt'

        try:
            with open(file_path, 'r') as file:
                features = {'status': 'ok', 'content': file.read()}

        except FileNotFoundError:
            features = {'status': 'error', 'content': 'No data for this user was not found.'}
            print(f"No feature map for {username} could be found.")

        return features
    
    async def save_conversation(self, messages, id):
        data_file = f'{os.path.join(self.__conv_dir, id)}.txt'
        with open(data_file, 'w') as file:
            file.write(messages)

        return 'Done'
    
    async def get_conversation(self, id):
        data_file = f'{os.path.join(self.__conv_dir, id)}.txt'
        try:
            with open(data_file, 'r') as file:
                messages = eval(file.read())
                return messages
        
        except FileNotFoundError:
            return -1
        
    
    async def call_openai_api(self, messages):
        print('Waiting for ollama response..')
        response = ollama.chat(
            model='llama3.2',
            messages=messages
            # temperature=0.2
        )
        return response

    async def send_message(self, username, message, id):

        messages = await self.get_conversation(id)

        if messages and messages != -1:
            print('--------------------------> calling messages')
            messages.append({'role': 'user', 'content': message})
            response = await self.call_openai_api(messages=messages)
        
        else:
            print('--------------------------> calling msg')
            with open(self.__conv_prompt, 'r') as file:
                initial_prompt = file.read()
            features = await self.get_features(username=username)
            feature_map = features['content'].replace('{', '').replace('}', '')
            if features['status'] == 'ok':
                system_prompt = {'role': 'system', 'content':f'{initial_prompt}\nFEATURE MAP:{feature_map}'}

            messages = []
            messages.append(system_prompt)

            messages.append({'role': 'user', 'content': message})

            response = await self.call_openai_api(messages=messages)
        
        response_message = response['message']['content']
        messages.append({'role':'assistant', 'content': response_message})

        print(response_message)

        await self.save_conversation(messages=str(messages), id=self.id)

        return(response_message)


# def read_file(user_id):
#     data_path = os.path.abspath("..\\data\\features\\")
#     filename = user_id

#     data_file = f"{data_path}\\{filename}.txt"
#     with open(data_file, 'r') as file:
#         text_content = file.read()

#     return text_content

# def send_message(user_id, messages, message):

#     if(message['content'] == '/q'):
#         return 0

#     messages.append(message)

#     print(messages)

#     response = ollama.chat(
#         model='llama3.2',
#         messages=messages
#     )

#     answer = response['message']

#     print(response['message']['content'])

#     # call text-to-speech, video and audio models

#     messages.append(answer)

#     message = {
#         'role': 'user',
#         'content': input('Enter your message: ')
#         }

#     send_message(user_id, messages, message)

# user_id = 'alex_morgan'
# user_features = read_file(user_id)

# messages=[
#     {
#     'role': 'system',
#     'content': '''you will be provided data about a certain user. act like him referencing
#     the given information. dont sound robotic or fake. answer questions
#     you only know about from the data provided. if you dont know something,
#     say that you dont know or that youll check and answer later.'''
#     },
#     {
#     'role': 'system',
#     'content': user_features
#     }
# ]

# user_input = input('Enter your message: ')

# message={
#     'role': 'user',
#     'content': user_input
#     }

# print(message)

# status = send_message('', messages, message)