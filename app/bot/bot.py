from .basebot import BaseBot
import requests
import time
import re
import json

class Bot(BaseBot):

    def __init__(self, token):
        super().__init__(token)
        self.last_time_someone_said_keyword = 0
        self.time_interval_between_keyword_detection = 60

    def check_if_user_joined(self, response):
        # If the messsage has the 'new chat participant'
        # key (when a user enters a group)
        msg = response['message']
        if 'new_chat_participant' in msg:
            # Check if the new participant has a first name
            if 'first_name' in msg['new_chat_participant']:
                # Use the genderize API to know if the name is a
                # male one or a female one
                first_name = msg['new_chat_participant']['first_name']
                url = 'https://api.genderize.io/?name={0}'.format(first_name)
                gender_response = requests.get(url)
                # Change the welcome_message in concordance
                if gender_response.json()['gender'] == 'female':
                    welcome_message = '<b>¡Bienvenida '
                else:
                    welcome_message = '<b>¡Bienvenido '

                welcome_message += '{0}!</b>'.format(first_name)
                self.send_message(msg['chat']['id'], parse_mode='HTML',
                                  text=welcome_message)

    def check_if_someone_said_keyword(self, response):
        # If the needed time has passed since the last keyword was detected
        if (time.time() > self.last_time_someone_said_keyword +
                self.time_interval_between_keyword_detection):
            # msg = ('Boh. Todo el mundo sabe que el mejor IDE es '
            #       '<a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ">'
            # 'Eclipse</a>.')

            bot_msg = ('Si estas interesado en bots puedes mirar '
                       '<a href="https://github.com/jabesga/idepybot">'
                       'como estoy hecho</a>.')
            keywords = {
                'bot': bot_msg,
            }
            # Check if any keyword is being used in the message
            for word in re.sub('[!@#$?]', '',
                               response['message']['text'].lower()).split():
                if word in keywords:
                    self.send_message(response['message']['chat']['id'],
                                      parse_mode='HTML', text=keywords[word],
                                      disable_web_page_preview=True)
                    self.last_time_someone_said_keyword = time.time()
                    return True
        return False

    def check_if_is_unix_timestamp(self, response):
        if response['inline_query']['query']:
            if response['inline_query']['query'].split(' ')[0] == 'unix':
                unix_timestamp = response['inline_query']['query'].split(' ')[1]
                url = 'http://www.convert-unix-time.com/api?timestamp={}'.format(unix_timestamp)

                json_response = requests.get(url).json()

                if 'utcDate' in json_response:
                    utcDate = json_response['utcDate']
                else:
                    utcDate = 'Impossible Unix Timestamp'

                document = json.dumps([{'type': 'article',
                                        'id': '0',
                                        'input_message_content': {'message_text': utcDate },
                                        'title': unix_timestamp,
                                        'description': utcDate,
                                        'thumb_url': 'http://a1.mzstatic.com/us/r30/Purple3/v4/78/50/a3/7850a3cb-8c1b-c8e0-c9ca-201575b29f54/icon175x175.png',
                                        'thumb_width': 512,
                                        'thumb_height': 512}])

                json_response = requests.post(
                    url='https://api.telegram.org/bot{0}/{1}'.format(self.token, 'answerInlineQuery'),
                    data={'inline_query_id': response['inline_query']['id'], 'results': document}
                ).json()

    def process_hook(self, response):
        if 'message' in response:
            self.check_if_user_joined(response)

            if 'text' in response['message']:
                self.check_if_someone_said_keyword(response)

        if 'inline_query' in response:
            self.check_if_is_unix_timestamp(response)
