import re

from bjira.operations import BJiraOperation
from bjira.operations.tax import DEFAULT_TAX_FIELDS
from bjira.utils import parse_portfolio_task

PORTFOLIO_PROJECT_ID = 'PORTFOLIO'
HH_PROJECT_ID = 'HH'
MARK_AS_NOT_AUTOTESTING_TRANSITION = '1211'

TASK_MAPPING = {
    'bg': ('330', HH_PROJECT_ID),
    'bug': ('330', HH_PROJECT_ID),
    'at': ('348', HH_PROJECT_ID),
    'hh': ('3', HH_PROJECT_ID),
    'feature': ('26500', PORTFOLIO_PROJECT_ID),
    'dwh': ('3', 'DWH'),
    'release': ('182', 'EXP'),
}

JQL_ESCAPE_PATTERN = r'([\]\["])'

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

def escape_jql(jql_string: str) -> str:
    return re.sub(JQL_ESCAPE_PATTERN, r"\\\\\1", jql_string)


class Operation(BJiraOperation):
    def __init__(self):
        super().__init__()
        self.dryrun = None
        self.jira_api = self.get_jira_api()

    def configure_arg_parser(self, subparsers):
        parser = subparsers.add_parser('create', help='create jira task')
        parser.add_argument(
            dest='task_type', default='hh', help='task type', nargs='?', choices=tuple(TASK_MAPPING.keys())
        )
        parser.add_argument(
            '-s', dest='service', default=None, help='task service - used for [{task service} prefix only'
        )
        parser.add_argument('-p', dest='portfolio', default=None, help='[optional] portfolio to link')
        parser.add_argument('-d', dest='description', default=None, help='[optional] task description')
        parser.add_argument('-v', dest='version', default=None, help='release version, required for release tasks')
        parser.add_argument('-m', dest='message', default=None, help='task name')
        parser.add_argument('-t', dest='team', default=None, help='team to assign task')
        parser.add_argument('-sp', dest='sp', default=None, help='task storypoints, example: 0.5')
        parser.add_argument('-l', dest='labels', default=None, help='сomma-separated list of labels')
        parser.add_argument(
            '--check', dest='check', default=False, action='store_true', help='check existing task before'
        )
        parser.add_argument(
            '--dryrun', dest='dryrun', default=False, action='store_true', help='just show params and exit'
        )
        parser.add_argument('--tax', dest='tax', default=False, action='store_true', help='fill default tax galochkas')
        parser.set_defaults(func=self._create_new_task)

    def _create_new_task(self, args):
        assert (
            args.task_type == 'release' and args.service is not None and args.version is not None
        ) or args.message is not None

        self.dryrun = args.dryrun

        task_message = _get_task_message(args)

        if args.check:
            escaped = escape_jql(task_message)
            query = f"""summary ~ '{escaped}'"""
            print(f'checking task {query}')
            found_issues = self.jira_api.search_issues(query, maxResults=10)
            for issue in found_issues:
                if issue.fields.summary.lower() == task_message.lower():
                    print(f'found existing task: {issue.permalink()} {issue.fields.summary}')
                    return None

        print(f'creating task "{task_message}"')

        issue_type, proj_id = _get_project_issue_type(args)
        labels = [label.strip() for label in args.labels.split(',')] if args.labels else None
        sp = float(args.sp) if args.sp else None
        release = args.task_type == 'release'
        task = self.create_task(issue_type, proj_id, task_message, args.team, args.description, labels, sp,
                                release, args.service, args.tax)
        if not task:
            return None
        print(self.get_task_url(task.key))

        if args.portfolio:
            portfolio_key = parse_portfolio_task(args.portfolio)
            self.jira_api.create_issue_link(type='Inclusion', inwardIssue=portfolio_key, outwardIssue=task.key)
            print(f'linked {self.get_task_url(task.key)} to {self.get_task_url(portfolio_key)}')

        if args.task_type == 'release':
            self.jira_api.transition_issue(issue=task.key, transition=MARK_AS_NOT_AUTOTESTING_TRANSITION)
            self.jira_api.assign_issue(issue=task.key, assignee='expsvc_jira')

        return CreateResult(task)


    def create_task(self, issue_type, proj_id, task_message, team=None, description=None, labels=None,
                    sp=None, release=False, service=None, version=None, tax=False):
        fields = {
            'project': proj_id,
            'issuetype': {'id': issue_type},
            'summary': task_message,
        }
        if not team:
            fields['assignee'] = {'name': self.get_user()}

        if description:
            fields['description'] = description

        if labels:
            fields['labels'] = labels

        if proj_id in (HH_PROJECT_ID, PORTFOLIO_PROJECT_ID):
            team = team or self.get_team()
            if team is not None:
                # Development team
                if proj_id == HH_PROJECT_ID:
                    fields['customfield_10961'] = {'value': team}
                else:
                    fields['customfield_34238'] = [{'value': team}]

            fields['customfield_11212'] = float(sp) if sp else None  # Story Points

        if release:
            fields['customfield_28411'] = f'{service}: {version}'  # Application
        if tax:
            fields.update(DEFAULT_TAX_FIELDS)

        if self.dryrun:
            print(fields)
            return None

        return self.jira_api.create_issue(prefetch=True, fields=fields)


class CreateResult:
    def __init__(self, task):
        self.task = task
