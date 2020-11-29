import json
from pathlib import Path

import keyring
from jira import JIRA

from bjira.utils import JIRA_SERVICE


class BJiraOperation:

    def __init__(self):
        self._config_json = None

    def configure_arg_parser(self, subparsers):
        raise NotImplementedError()

    def get_config(self):
        if not self._config_json:
            with open(Path.joinpath(Path.home(), '.bjira_config'), 'r') as config:
                _config_json = json.loads(config.read())

        return _config_json

    def get_jira_api(self, **kwargs):
        user = self.get_user()
        return JIRA(server=self.get_config()['host'],
                    basic_auth=(user, keyring.get_password(JIRA_SERVICE, user)), **kwargs)

    def get_user(self):
        return self.get_config()['user']

    def get_team(self):
        return self.get_config()['team']

    def get_task_url(self, task_name):
        host = self.get_config()['host']
        return f'{host}/browse/{task_name}'
