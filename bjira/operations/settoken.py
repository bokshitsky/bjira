from getpass import getpass

import keyring

from bjira.operations import BJiraOperation
from bjira.utils import JIRA_TOKEN, JIRA_SERVICE


class Operation(BJiraOperation):

    def configure_arg_parser(self, subparsers):
        parser_setpass = subparsers.add_parser('settoken', help='set jira token, remove password if present')
        parser_setpass.set_defaults(func=self._set_token)

    def _set_token(self, args):
        user = self.get_user()
        keyring.set_password(JIRA_TOKEN, user, getpass(f'set jira token for {user}: '))
        if keyring.get_password(JIRA_SERVICE, user):
            keyring.delete_password(JIRA_SERVICE, user)
        try:
            self.get_jira_api(max_retries=0)
            print('token set')
        except:
            print('bad token')
