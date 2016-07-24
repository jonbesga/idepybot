from flask import Flask, request
from .bot import Bot
import configparser
import os

app = Flask(__name__)
app.debug = True

# Read sensible data from settings.ini file
#config = configparser.ConfigParser()
#config.read(os.path.join(os.path.dirname(__file__), 'settings.ini'))
#TOKEN = config.get("Bot", "token")
#HEROKU_APP = config.get("Heroku", "app_url")

TOKEN = S3Client(os.environ['token'], os.environ['token'])
HEROKU_APP = S3Client(os.environ['app_url'], os.environ['app_url'])

# Create bot object and set webhook
bot = Bot(TOKEN)
json_response = bot.set_webhook(HEROKU_APP + '/{0}'.format(TOKEN))

@app.route("/{0}".format(TOKEN), methods=['POST'])
def hook():
    result = bot.process_hook(request.get_json())
    return '', 200
