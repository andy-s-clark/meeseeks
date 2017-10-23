import re
import yaml

from bottle import HTTPError


class Meeseeks:
    def __init__(self):
        self._load_config()

    def _load_config(self):
        with open('meeseeks.yaml') as config_file_handle:
            self.__config = yaml.load(config_file_handle)
            for route in self.__config['message_routes']:
                self.__config['message_routes'][route]['regex'] = re.compile(route)

    @staticmethod
    def get_descriptor(base_url, auth_token):
        query_string = ''
        if auth_token is not None:
            query_string = '?auth_token=%s' % auth_token
        return {
            'name': 'Meeseeks',
            'description': 'Slash command bot. Look at me!',
            'key': 'com.build.meeseeks',
            'links': {
                'self': '%s/descriptor/%s' % (base_url, query_string),
            },
            'capabilities': {
                'installable': {
                    'allowGlobal': False,
                    'allowRoom': True
                },
                'webhook': [
                    {
                        'event': 'room_message',
                        'pattern': '^\/',
                        'url': '%s/webhook/%s' % (base_url, query_string),
                        'name': 'meeseeks',
                        'authentication': 'none'
                    }
                ],
                'hipchatApiConsumer': {
                    'scopes': [
                        'send_notification'
                    ]
                }
            }
        }

    def handle_room_message_item(self, message_item):
        if 'message' not in message_item or \
              'message' not in message_item['message']:
            raise HTTPError(400, 'Missing item.message.message')
        for route_name, route_options in self.__config['message_routes'].items():
            match_result = route_options['regex'].search(message_item['message']['message'].rstrip())
            if match_result:
                method_to_run = getattr(self, route_options['callback'])
                return method_to_run(message_item=message_item, match_result=match_result)
        return {} # Don't do anything if there is no matching route

    @staticmethod
    def show_message(message, color='green', notify=False, message_format='html'):
        return {'color': color, 'message': message, 'notify': notify, 'message_format': message_format}

    def show_help(self, message_item, match_result):
        help_items = ''
        for route_name, route_options in self.__config['message_routes'].items():
            help_items += self.__config['help_item_template']\
                .replace('{description}', route_options['description'])\
                .replace('{example}', route_options['example'])
        return self.show_message(message=self.__config['help_template'].replace('{help_items}', help_items))

    @staticmethod
    def _get_phones():
        try:
            with open('phones.yaml') as phones_file_handle:
                phones = yaml.load(phones_file_handle)
        except FileNotFoundError:
            with open('example_phones.yaml') as phones_file_handle:
                phones = yaml.load(phones_file_handle)
        return phones

    def show_phones(self, message_item, match_result):
        phones = self._get_phones()
        try:
            name_to_match = match_result.group('name').lower()
            filtered_phones = {k: v for k, v in phones.items() if name_to_match in k.lower()}
            print(filtered_phones)
        except IndexError:
            filtered_phones = phones
        phones_items = ''
        for name, number in sorted(filtered_phones.items()):
            phones_items += self.__config['phones_item_template']\
                .replace('{name}', name)\
                .replace('{number}', number)
        return self.show_message(message=self.__config['phones_template']
                                 .replace('{phones_items}', phones_items))
