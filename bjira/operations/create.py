from bjira.operations import BJiraOperation
from bjira.utils import parse_portfolio_task

HH_PROJECT_ID = 'HH'

TASK_MAPPING = {
    'bg': '330',
    'bug': '330',

    'at': '348',

    'hh': '3',

    'dwh': '3',
}

PROJ_MAPPING = {
    'bg': HH_PROJECT_ID,
    'bug': HH_PROJECT_ID,
    'at': HH_PROJECT_ID,
    'hh': HH_PROJECT_ID,

    'dwh': 'DWH',
}


def _get_proj_id(args):
    return PROJ_MAPPING.get(args.task_type.lower())


def _get_issue_id(args):
    return TASK_MAPPING.get(args.task_type.lower())


def _get_prefix(args):
    if not args.service and args.task_type == 'at':
        return '[at] '
    elif args.service:
        return f'[{args.service}] '
    return ''


def _get_task_message(args):
    return _get_prefix(args) + args.message


class CreateJiraTask(BJiraOperation):

    def configure_arg_parser(self, subparsers):
        parser = subparsers.add_parser('create', help='create jira task')
        parser.add_argument(dest='task_type', default='hh', help='task type', nargs='?',
                            choices=tuple(TASK_MAPPING.keys()))
        parser.add_argument('-s', dest='service', default=None,
                            help='task service - used for [{task service} prefix only')
        parser.add_argument('-p', dest='portfolio', default=None, help='[optional] portfolio to link')
        parser.add_argument('-m', dest='message', required=True, help='task name')
        parser.add_argument('-sp', dest='sp', default=None, help='task storypoints, example: 0.5')
        parser.set_defaults(func=self._create_new_task)

    def _create_new_task(self, args):
        task_message = _get_task_message(args)
        print(f'creating task "{task_message}"')

        jira_api = self.get_jira_api()
        proj_id = _get_proj_id(args)
        fields = {
            'project': proj_id,
            'issuetype': {'id': _get_issue_id(args)},
            'assignee': {'name': self.get_user()},
            'summary': task_message,
        }
        if proj_id == HH_PROJECT_ID:
            fields['customfield_10961'] = {'value': self.get_team()}  # Development team
            fields['customfield_11212']: float(args.sp) if args.sp else None  # Story Points

        task = jira_api.create_issue(
            prefetch=True,
            fields=fields
        )
        print(self.get_task_url(task.key))

        if args.portfolio:
            portfolio_key = parse_portfolio_task(args.portfolio)
            jira_api.create_issue_link(
                type='Inclusion',
                inwardIssue=portfolio_key,
                outwardIssue=task.key
            )
            print(f'linked {self.get_task_url(task.key)} to {self.get_task_url(portfolio_key)}')
