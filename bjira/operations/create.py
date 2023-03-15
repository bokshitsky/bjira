from bjira.operations import BJiraOperation
from bjira.utils import parse_portfolio_task

HH_PROJECT_ID = 'HH'
MARK_AS_NOT_AUTOTESTING_TRANSITION = '1211'

TASK_MAPPING = {
    'bg': ('330', HH_PROJECT_ID),
    'bug': ('330', HH_PROJECT_ID),
    'at': ('348', HH_PROJECT_ID),
    'hh': ('3', HH_PROJECT_ID),
    'dwh': ('3', 'DWH'),
    'release': ('182', 'EXP')
}

def _get_project_issue_type(args):
    return TASK_MAPPING.get(args.task_type.lower())


def _get_prefix(args):
    if not args.service and args.task_type == 'at':
        return '[at] '
    elif args.service:
        return f'[{args.service}] '
    return ''


def _get_task_message(args):
    if args.task_type == 'release':
        return f'{args.service}={args.version}'
    return _get_prefix(args) + args.message


class Operation(BJiraOperation):

    def configure_arg_parser(self, subparsers):
        parser = subparsers.add_parser('create', help='create jira task')
        parser.add_argument(dest='task_type', default='hh', help='task type', nargs='?',
                            choices=tuple(TASK_MAPPING.keys()))
        parser.add_argument('-s', dest='service', default=None,
                            help='task service - used for [{task service} prefix only')
        parser.add_argument('-p', dest='portfolio', default=None, help='[optional] portfolio to link')
        parser.add_argument('-d', dest='description', default=None, help='[optional] task description')
        parser.add_argument('-v', dest='version', default=None, help='release version, required for release tasks')
        parser.add_argument('-m', dest='message', default=None, help='task name')
        parser.add_argument('-sp', dest='sp', default=None, help='task storypoints, example: 0.5')
        parser.set_defaults(func=self._create_new_task)

    def _create_new_task(self, args):
        assert (
           args.task_type == "release"
           and args.service is not None
           and args.version is not None
        ) or args.message is not None

        task_message = _get_task_message(args)
        print(f'creating task "{task_message}"')

        jira_api = self.get_jira_api()
        issue_type, proj_id = _get_project_issue_type(args)

        fields = {
            'project': proj_id,
            'issuetype': {'id': issue_type},
            'assignee': {'name': self.get_user()},
            'summary': task_message,
        }
        if args.description:
            fields['description'] = args.description

        if proj_id == HH_PROJECT_ID:
            fields['customfield_10961'] = {'value': self.get_team()}  # Development team
            fields['customfield_11212'] = float(args.sp) if args.sp else None  # Story Points

        if args.task_type == 'release':
            fields['customfield_28411'] = f'{args.service}: {args.version}'  # Application

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

        if args.task_type == 'release':
            jira_api.transition_issue(
                issue=task.key,
                transition=MARK_AS_NOT_AUTOTESTING_TRANSITION
            )
            jira_api.assign_issue(issue=task.key, assignee='expsvc_jira')

        return CreateResult(task)


class CreateResult:

    def __init__(self, task):
        self.task = task
