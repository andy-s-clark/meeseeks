import re

class Meeseeks():

    def __init__(self):
        self.__message_matchers = {
            re.compile('^/phones$'): 'get_phones'
        }

    def handle_room_message_item(self, message_item):
        if 'message' not in message_item or \
              'message' not in message_item['message']:
            raise HTTPError(400, 'Missing item.message.message')
        for regex in self.__message_matchers:
            match_result = regex.match(message_item['message']['message'])
            if match_result:
                method_to_run = getattr(self, "get_phones")
                return method_to_run(match_result, message_item)
        return {}

    def get_phones(self, match_result, message_item):
        return {'result': 'phones!'}