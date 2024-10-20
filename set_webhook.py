import requests

TOKEN = '7809347377:AAGBdPUSRcNsBgQcMWsvHGxrm-EMBtL3fso'
WEBHOOK_URL = 'https://ba70-95-24-220-215.ngrok-free.app/telegram-webhook/'

response = requests.get(f'https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}')
print(response.json())
