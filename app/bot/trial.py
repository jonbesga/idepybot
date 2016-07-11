class Trial:
    def __init__(self, chat_id, guilty, guilty_id):
        self.chat_id = chat_id
        self.guilty = guilty
        self.guilty_id = guilty_id
        self.punishment = 0
        self.forgiveness = 0
        self.status_text = '''
<b>¡¡phyton...PHYTON...PHYTON!!</b>
@{0} vas a ser juzgado por este sacrilegio ortografico.

Votad ahora el destino de @{0}:
* {1} votaron castigo
* {2} votaron perdon
        '''.format(self.guilty, self.punishment, self.forgiveness)
        self.inline_keyboard = [
            [
                {'text': 'Castigo', 'callback_data': 'punishment'},
                {'text': 'Perdon','callback_data': 'forgiveness' }
            ]
        ]
        self.who_has_voted = []

    def update_status_text(self):
        self.status_text = '''
<b>¡¡phyton...PHYTON...PHYTON!!</b>
@{0} vas a ser juzgado por este sacrilegio ortografico.

Votad ahora el destino de {0}:
* {1} votaron castigo
* {2} votaron perdon
        '''.format(self.guilty, self.punishment, self.forgiveness)

    def has_voted(self, username):
        if username in self.who_has_voted:
            return True
        else:
            return False
