import requests
import json
import openai
import pandas as pd

# Repositório da API: https://github.com/digitalinnovationone/santander-dev-week-2023-api

sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app'
# O arquivo SDW2023.csv serve apenas de exemplo

# Para gerar uma API Key:
# 1. Crie uma conta na OpenAI
# 2. Acesse a seção "API Keys"
# 3. Clique em "Create API Key"
# Link direto: https://platform.openai.com/account/api-keys

# Substitua o texto por sua API Key da OpenAI, ela será salva como uma variável de ambiente.
openai_api_key = "example"
openai.api_key = openai_api_key 

#EXTRACT
df = pd.read_csv('SDW2023.csv')
user_ids = df['UserID'].tolist()
print(user_ids)

def get_user(id):
    response = requests.get(f'{sdw2023_api_url}/users/{id}')
    return response.json() if response.status_code == 200 else None

users = [user for id in user_ids if (user := get_user(id)) is not None]
print(json.dumps(users, indent=2))

#TRANSFORM
def generate_ai_news(user):
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "Você é um especialista em minternet banking."
            },
            {
                "role": "user",
                "content": f"Crie uma mensagem para {user['name']} sobre as vantagens do PIX (máximo de 100 caracteres)"
            }
        ]
        )
    return completion.choices[0].message.content.strip('\"')

for user in users:
    news = generate_ai_news(user)
    print(news)
    user['news'].append({
        "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
        "description": news
    })

  #LOAD
def update_user(user):
    response = requests.put(f"{sdw2023_api_url}/users/{user['id']}", json=user)
    return True if response.status_code == 200 else False

for user in users:
    success = update_user(user)
    print(f"Usuário atualizado com sucesso!" if success else "Algo de errado aconteceu... Tente novamente.")

