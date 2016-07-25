import requests


class BaseBot:
    def __init__(self, token):
        self.token = token
        self.offset = 0

    def make_query(self, method, payload=None):
        url = 'https://api.telegram.org/bot{0}/{1}'.format(self.token, method)
        response = requests.post(url, payload, timeout=1)
        return response.json()

    # For reference, see: https://core.telegram.org/bots/api#available-methods
    def get_me(self):
        json_response = self.make_query('getMe')
        return json_response

    def get_updates(self, offset, limit=100, timeout=0):
        json_response = self.make_query(
            'getUpdates', {'offset': offset, 'limit': limit,
                           'timeout': timeout})
        return json_response

    def set_webhook(self, url):
        json_response = self.make_query('setWebhook', {'url': url})
        return json_response

    def delete_webhook(self):
        json_response = self.make_query('setWebhook')
        return json_response

    def send_message(self, chat_id, text=None, parse_mode=None,
                     disable_web_page_preview=None, disable_notification=None,
                     reply_to_message_id=None, reply_markup=None):

        json_response = self.make_query(
            'sendMessage',
            {'chat_id': chat_id, 'text': text,
             'disable_web_page_preview': disable_web_page_preview,
             'parse_mode': parse_mode,
             'disable_notification': disable_notification,
             'reply_to_message_id': reply_to_message_id,
             'reply_markup': reply_markup})
        return json_response

    def forward_message(self, chat_id, from_chat_id, message_id,
                        disable_notification=False):
        json_response = self.make_query(
            'forwardMessage',
            {'chat_id': chat_id, 'from_chat_id': from_chat_id,
             'disable_notification': disable_notification,
             'message_id': message_id})
        return json_response

    def edit_message_text(self, chat_id, message_id, text, parse_mode=None,
                          reply_markup=None):
        json_response = self.make_query(
            'editMessageText',
            {'chat_id': chat_id, 'message_id': message_id,
             'parse_mode': parse_mode, 'text': text,
             'reply_markup': reply_markup})
        return json_response

    def answer_callback_query(self, callback_query_id, text):
        json_response = self.make_query(
            'answerCallbackQuery',
            {'callback_query_id': callback_query_id, 'text': text})
        return json_response

    def kick_chat_member(self, chat_id, user_id):
        json_response = self.make_query(
            'kickChatMember', {'chat_id': chat_id, 'user_id': user_id})
        return json_response

    def unban_chat_member(self, chat_id, user_id):
        json_response = self.make_query(
            'unbanChatMember', {'chat_id': chat_id, 'user_id': user_id})
        return json_response

    def process_updates(self):
        json_response = self.get_updates(self.offset)
        if 'result' in json_response:
            if json_response['result']:
                self.offset = json_response['result'][0]['update_id'] + 1
                return json_response['result'][0]
