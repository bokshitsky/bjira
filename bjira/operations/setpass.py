from getpass import getpass

import keyring

from bjira.operations import BJiraOperation
from bjira.utils import JIRA_SERVICE


class Operation(BJiraOperation):

    def configure_arg_parser(self, subparsers):
        parser_setpass = subparsers.add_parser('setpass', help='set jira token')
        parser_setpass.set_defaults(func=self._set_password)

    def _set_password(self, args):
        config = self.get_config()
        user = config['user']
        print(
            f'Получить токен можно тут: '
            f'{config["host"]}/secure/ViewProfile.jspa?selectedTab=com.atlassian.pats.pats-plugin:jira-user-personal-access-tokens'
        )
        keyring.set_password(JIRA_SERVICE, user, getpass(f'set token for user {user}'))
        try:
            self.get_jira_api(max_retries=0)
            print('token set')
        except:
            print('bad token')
