from .basebot import BaseBot
from .trial import Trial
import requests
import time
import re
import logging
import json

class Bot(BaseBot):

    def __init__(self, token):
        super().__init__(token)
        self.last_time_someone_said_keyword = 0
        self.time_interval_between_keyword_detection = 30

        self.active_trial = None

    def check_if_user_joined(self, response):
        if 'new_chat_participant' in response['message']:
            if 'first_name' in response['message']['new_chat_participant']:
                gender_response = requests.get('https://api.genderize.io/?name={0}'.format(response['message']['new_chat_participant']['first_name']))
                if gender_response.json()['gender'] == 'female':
                    welcome_message = '<b>¡Bienvenida '
                else:
                    welcome_message = '<b>¡Bienvenido '
                welcome_message += '{0}!</b>'.format(response['message']['new_chat_participant']['first_name'])
                json_response = self.send_message(response['message']['chat']['id'], parse_mode='HTML', text=welcome_message)
                self.logger.debug(json_response)

    def check_if_someone_said_keyword(self, response):
        if time.time() > self.last_time_someone_said_keyword + self.time_interval_between_keyword_detection:
            keywords = {
                'ide':'No dudes. El mejor #IDE es <a href="https://www.jetbrains.com/pycharm/">Pycharm</a>.',
                'empresa':'Hablando de empresas, no olvides visitar nuestro <a href="https://github.com/python-spain/empresas/blob/master/.github/CONTRIBUTING.md">repositorio de empresas españolas</a> que usan Python.',
            }

            for word in re.sub('[!@#$?]', '', response['message']['text'].lower()).split():
                if word in keywords:
                    json_response = self.send_message(response['message']['chat']['id'], parse_mode='HTML', text=keywords[word])
                    self.logger.debug(json_response)
                    self.last_time_someone_said_keyword = time.time()
                    return True
        return False

    # TODO: Reorganize code
    def check_if_someone_said_phyton(self, response):
        for word in re.sub('[!@#$?]', '', response['message']['text'].lower()).split():
            if word == 'phyton':
                if not self.active_trial:
                    if 'username' in response['message']['from']:
                        new_trial = Trial(
                            response['message']['chat']['id'],
                            response['message']['from']['username'],
                            response['message']['from']['id']
                        )
                        self.active_trial = new_trial

                        json_response = self.send_message(
                            self.active_trial.chat_id,
                            parse_mode='HTML',
                            text=self.active_trial.status_text,
                            reply_markup=json.dumps({'inline_keyboard': self.active_trial.inline_keyboard})
                        )
                        self.logger.debug(json_response)
                        self.active_trial.status_message_id = json_response['result']['message_id']
                    else:
                        self.kick_chat_member(response['message']['chat']['id'], response['message']['from']['id'])
                        self.unban_chat_member(response['message']['chat']['id'], response['message']['from']['id'])
                        json_response = self.send_message(response['message']['chat']['id'], parse_mode='HTML', text='Sin nombre de usuario no hay juicio.')
                        self.logger.debug(json_response)

                else:
                    if response['message']['from']['id'] == self.active_trial.guilty_id:
                        you_are_lucky_text = '<b>No aprendes @{0}. Ni un juicio mereces.</b>'.format(self.active_trial.guilty)
                        self.kick_chat_member(self.active_trial.chat_id, self.active_trial.guilty_id)
                        self.unban_chat_member(response['message']['chat']['id'], response['message']['from']['id'])
                        self.active_trial.update_status_text()
                        json_response = self.edit_message_text(
                            self.active_trial.chat_id,
                            self.active_trial.status_message_id,
                            text=self.active_trial.status_text,
                            parse_mode='HTML',
                        )
                        self.logger.debug(json_response)
                        self.active_trial = None
                    else:
                        you_are_lucky_text = '<b>Tienes suerte. Ya estoy castigando a otro pecador</b>'
                    json_response = self.send_message(response['message']['chat']['id'], parse_mode='HTML', text=you_are_lucky_text)
                    self.logger.debug(json_response)
                return True

    def process_hook(self, response):
        self.logger.debug(response)
        # TODO: Reorganize code
        if self.active_trial:
            # TODO: Timestamp of trial start and kick if punishment is greater than forgiveness
            if 'callback_query' in response:
                if 'username' in response['callback_query']['from']:
                    if not self.active_trial.has_voted(response['callback_query']['from']['username']):
                        if response['callback_query']['data'] == 'punishment':
                            self.active_trial.punishment += 1
                        elif response['callback_query']['data'] == 'forgiveness':
                            self.active_trial.forgiveness += 1

                        self.active_trial.who_has_voted.append(response['callback_query']['from']['username'])
                        self.active_trial.update_status_text()
                        json_response = self.edit_message_text(
                            self.active_trial.chat_id,
                            self.active_trial.status_message_id,
                            text=self.active_trial.status_text,
                            parse_mode='HTML',
                            reply_markup=json.dumps({'inline_keyboard': self.active_trial.inline_keyboard})
                        )
                        self.logger.debug(json_response)
                        json_response = self.answer_callback_query(response['callback_query']['id'], text='Recibido!')
                        self.logger.debug(json_response)
                    else:
                        json_response = self.answer_callback_query(response['callback_query']['id'], text='Ya has votado!')
                        self.logger.debug(json_response)
                else:
                    json_response = self.answer_callback_query(response['callback_query']['id'], text='Necesitas nombre de usuario para votar!')
                    self.logger.debug(json_response)

        if 'message' in response:
            self.check_if_user_joined(response)

            if 'text' in response['message']:
                self.check_if_someone_said_keyword(response)
                self.check_if_someone_said_phyton(response)
