from getpass import getpass

import keyring

from bjira.operations import BJiraOperation
from bjira.utils import JIRA_SERVICE


class SetPasswordTask(BJiraOperation):

    def configure_arg_parser(self, subparsers):
        parser_setpass = subparsers.add_parser('setpass', help='set jira password')
        parser_setpass.set_defaults(func=self._set_password)

    def _set_password(self, args):
        config = self.get_config()
        user = config['user']
        keyring.set_password(JIRA_SERVICE, user, getpass(f'set password for user {user}'))
        try:
            self.get_jira_api(max_retries=0)
            print('password set')
        except:
            print('bad password')
