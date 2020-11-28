import json
from pathlib import Path

import keyring
from jira import JIRA

JIRA_SERVICE = 'bjira'

DEFENSE_TEXT = 'Я проверил портфель на безопасность по "Чеклисту", портфель не несет рисков или согласован с ' \
               'командой Defense.'

_config_json = None


def get_config():
    global _config_json
    if not _config_json:
        with open(Path.joinpath(Path.home(), '.bjira_config'), 'r') as config:
            _config_json = json.loads(config.read())

    return _config_json


def get_jira_api(**kwargs):
    user = get_user()
    return JIRA(server=get_config()['host'], basic_auth=(user, keyring.get_password(JIRA_SERVICE, user)), **kwargs)


def get_user():
    return get_config()['user']


def get_team():
    return get_config()['team']


def get_task_url(task_name):
    host = get_config()['host']
    return f'{host}/browse/{task_name}'
