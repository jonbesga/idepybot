from flask import Flask, request
from .bot import Bot
import configparser
import os
import logging
import datetime

app = Flask(__name__)
app.debug = True

# os.makedirs and logging to a filename SEEMS THAT DOESN'T WORK ON HEROKU
# logs_directory = os.path.join(os.path.dirname(__file__), 'logs')
# print(logs_directory)
# if not os.path.exists(logs_directory):
#     os.makedirs(logs_directory)
# log_file = os.path.join(logs_directory, '{0}.log'.format(str(datetime.datetime.now()).split(' ')[0]))
#
# logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s;%(name)s;%(levelname)s;%(message)s', datefmt="%Y-%m-%d %H:%M:%S")

logging.basicConfig(level=logging.INFO, format='%(asctime)s [X] [%(levelname)s] %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'settings.ini'))

TOKEN = config.get("Bot", "token")
HEROKU_APP = config.get("Heroku", "app_url")

bot = Bot(TOKEN)
json_response = bot.set_webhook(HEROKU_APP + '/{0}'.format(TOKEN))
logger.info(json_response['description'])

@app.route("/{0}".format(TOKEN), methods=['POST'])
def hook():
    result = bot.process_hook(request.get_json())
    return '', 200
