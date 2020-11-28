#!/usr/bin/env python3
import argparse
import re
from getpass import getpass

import keyring

from bjira.utils import get_jira_api, get_task_url, get_user, get_team, get_config, JIRA_SERVICE, DEFENSE_TEXT


def _get_issue_type(args):
    return {
        'bg': 'Production Bug',
        'bug': 'Production Bug',

        'at': 'Autotesting Task',

        'hh': 'Задача'
    }.get(args.task_type, 'Задача')


def _get_prefix(args):
    if not args.service and args.task_type == 'at':
        return '[at] '
    elif args.service:
        return f'[{args.service}] '
    return ''


def _get_task_message(args):
    return _get_prefix(args) + args.message


def _parse_portfolio_task(portfolio):
    return 'PORTFOLIO-' + re.sub('[^0-9]', '', portfolio)


def _create_new_task(args):
    task_message = _get_task_message(args)
    print(f'creating task "{task_message}"')

    jira_api = get_jira_api()
    task = jira_api.create_issue(
        prefetch=True,
        fields={
            'project': 'HH',
            'issuetype': {'name': _get_issue_type(args)},
            'assignee': {'name': get_user()},
            'summary': task_message,
            'customfield_10961': {'value': get_team()}  # Development team
        }
    )
    print(get_task_url(task.key))

    if args.portfolio:
        portfolio_key = _parse_portfolio_task(args.portfolio)
        jira_api.create_issue_link(
            type='Inclusion',
            inwardIssue=portfolio_key,
            outwardIssue=task.key
        )
        print(f'linked {get_task_url(task.key)} to {get_task_url(portfolio_key)}')


def _set_password(args):
    config = get_config()
    user = config['user']
    keyring.set_password(JIRA_SERVICE, user, getpass(f'set password for user {user}'))
    try:
        get_jira_api(max_retries=0)
        print('password set')
    except:
        print('bad password')


def _fill_defense_galochka(args):
    jira_api = get_jira_api()
    issue = jira_api.issue(_parse_portfolio_task(args.portfolio[0]))
    print(f'fill "ya proveril bezopasnost" galochka for {get_task_url(issue.key)}')
    issue.update(fields={'customfield_32210': [{'value': DEFENSE_TEXT}]})


def _parse_args():
    parser = argparse.ArgumentParser(description='Create jira.hh.ru tasks and optionally link to portfolio')
    subparsers = parser.add_subparsers(help='sub-command help', required=True)

    parser_create = subparsers.add_parser('create', help='create jira task')
    parser_create.add_argument(dest='task_type', default='hh', help='task type', nargs='?',
                               choices=('hh', 'at', 'test', 'bg', 'bag'))
    parser_create.add_argument('-s', dest='service', default=None,
                               help='task service - used for [{task service} prefix only')
    parser_create.add_argument('-p', dest='portfolio', default=None, help='[optional] portfolio to link')
    parser_create.add_argument('-m', dest='message', required=True, help='task name')
    parser_create.set_defaults(func=_create_new_task)

    parser_setpass = subparsers.add_parser('setpass', help='set jira password')
    parser_setpass.set_defaults(func=_set_password)

    for short_name in ('stas', 'defense'):
        parser_defense = subparsers.add_parser(short_name, help='fill portfolio defense galochka')
        parser_defense.add_argument(dest='portfolio', help='portfolio', nargs=1)
        parser_defense.set_defaults(func=_fill_defense_galochka)

    return parser.parse_args()


def main():
    args = _parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
