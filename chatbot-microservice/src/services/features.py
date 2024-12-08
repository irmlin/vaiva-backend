import ollama
import os
import json

class FeaturesService:
    def __init__(self):
        self.__extr_prompt = f"{os.path.join('static')}/feature_extraction_prompt.json"
        self.__data_dir = os.path.join('src', 'data', 'features')

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
    
    # Overwrites specific users feature map file with new data
    async def write_features(self, username, data):
        data_file = f'{os.path.join(self.__data_dir, username)}.txt'

        print(f'Updating features for {username}')
        with open(data_file, 'w') as file:
            file.write(data)

        return 'done'
    
    # Generates feature map and a response using Ollama. Endpoint returns response
    # string to display to the user in frontend
    async def extreact_features(self, username, msg):
        existing_features = await self.get_features(username=username)
        messages = []

        with open(self.__extr_prompt, 'r') as file:
            extr_prompt = json.load(file)

        messages.append(extr_prompt)

        if existing_features['status'] == 'ok':
            messages.append({'role': 'user', 'content': existing_features['content']})

        msg_expand = [{'role': 'assistant', 'content': 'What else can you tell me about yourself?'},
                      {'role': 'user', 'content': msg}]
        messages.extend(msg_expand)

        print('Waiting for ollama response..')
        response = ollama.chat(
            model='llama3.2',
            format='json',
            messages=messages
        )

        response_data = response['message']['content']
        print(response_data)

        messages.append({'role': 'assistant', 'content': response_data})

        # response_data = json.dumps(response_data)
        response_data = json.loads(response_data)

        print(f'++++++++++++++++++++++++++++++\nFEATURES:\n{response_data['features']}')
        print(f'++++++++++++++++++++++++++++++\nRESPONSE:\n{response_data['response']}')
        
        features = json.dumps(response_data['features'])
        await self.write_features(username=username, data=features)

        return response_data['response']