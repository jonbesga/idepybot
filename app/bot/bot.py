from .basebot import BaseBot
import requests
import time
import re
import json

class Caesar():

    alphabet = "abcdefghijklmnopqrstuvwxyz"

    def __init__(self, key):
        self.key = key
        self.shifted_alphabet = self.alphabet[key:] + self.alphabet[0:key]
        self.encrypt_dict = str.maketrans(self.alphabet, self.shifted_alphabet)
        self.decrypt_dict = str.maketrans(self.shifted_alphabet, self.alphabet)

    def encrypt_sentence(self, sentence):
        return sentence.translate(self.encrypt_dict)

    def decrypt_sentence(self, sentence):
        return sentence.translate(self.decrypt_dict)


class Bot(BaseBot):

    def __init__(self, token):
        super().__init__(token)
        self.last_time_someone_said_keyword = 0
        self.time_interval_between_keyword_detection = 60
        self.pinned_message = '''
@astrojuanlu: ¡Hola a todos! Bienvenidos al grupo de Telegram de la Asociación Python España. Este grupo está abierto a todo el mundo y en él se hablan temas que tienen que ver con la comunidad Python española, se preguntan dudas y se intercambia información. Algunos consejos y normas para empezar:

* Preséntate cuando llegues 😄
* Los principiantes son bienvenidos
* Si no conoces un grupo local en tu ciudad, dilo y te indicaremos
* Temas on-topic: dudas sobre Python, discusión general, #PyConES, eventos, reuniones (entre otros)
* Este es un grupo grande, se recomienda evitar el bombardeo de mensajes (_flood_) en la medida de lo posible
* Para asuntos profundos, se recomienda acudir a la lista de correo https://lists.es.python.org/listinfo/general
* Las discusiones en el grupo se rigen por el código de conducta de la asociación, que puedes leer en http://documentos-asociacion.es.python.org/c%C3%B3digo%20de%20conducta.html
* En concreto, las bromas de contenido sexual o inapropiado no están permitidas
* Este grupo está moderado, sé respetuoso y tolerante con los demás
* "We are all consenting adults here"
* La web de la asociación es http://es.python.org y te puedes hacer socio por 30 € al año para apoyar las actividades y eventos que desarrolla, si quieres

¡Disfruta del grupo!
        '''

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
                    welcome_message = '<b>¡Bienvenida a Python España '
                else:
                    welcome_message = '<b>¡Bienvenido a Python España '

                welcome_message += '{0}!</b>\n'.format(first_name)
                welcome_message += ('Durante tu estancia aquí es importante que '
                                    'conozcas las reglas del grupo. '
                                    '<a href="https://telegram.me/idepybot">Habla conmigo</a> '
                                    'para conocerlas.')

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

    # Todo Testing
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

    # Todo Testing
    def check_if_is_caesar(self, response):
        if response['inline_query']['query']:
            if response['inline_query']['query'].split(' ')[0] == 'caesar':
                sentence = response['inline_query']['query'].split(' ')[1]
                caesar = Caesar(13)
                encrypted_sentence = caesar.encrypt_sentence(sentence)

                document = json.dumps([{'type': 'article',
                                        'id': '0',
                                        'input_message_content': {'message_text': encrypted_sentence },
                                        'title': "Send your text encrypted",
                                        'description': encrypted_sentence
	            }])

                json_response = requests.post(
                    url='https://api.telegram.org/bot{0}/{1}'.format(self.token, 'answerInlineQuery'),
                    data={'inline_query_id': response['inline_query']['id'], 'results': document},
                    timeout=0.5
                ).json()


    def process_hook(self, response):
        if 'message' in response:
            self.check_if_user_joined(response)

            if 'text' in response['message']:
                if response['message']['text'] == '/start': # or response['message']['text'] == '/rules@IdePyBot':
                    json_response = self.send_message(response['message']['from']['id'],
                                      parse_mode='HTML', text=self.pinned_message)
                    print(json_response)
                # else:
                #     pass
                    # self.check_if_someone_said_keyword(response)

        if 'inline_query' in response:
            pass
            #self.check_if_is_unix_timestamp(response)
            #self.check_if_is_caesar(response)
