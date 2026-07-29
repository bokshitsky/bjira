from collections import namedtuple
from itertools import chain

import yaml
from pykwalify.core import Core

import bjira
from bjira.operations import create
from bjira.operations.create import TASK_MAPPING, PORTFOLIO_PROJECT_ID
from bjira.utils import ISSUE_LINK_TYPES_MAP

Issue = namedtuple('Issue',
                   ['name',
                    'service',
                    'existing',
                    'type',
                    'description',
                    'storypoints'])
Link = namedtuple('Link', ['type', 'inward', 'outward'])


SUM_STORYPOINTS = 'SUM_STORYPOINTS'


def _process_issue(issue):
    return Issue(*[issue[field] if field in issue else None for field in Issue._fields])


def _process_link(from_id, link, labels):
    if link['type'] not in ISSUE_LINK_TYPES_MAP:
        raise Exception(f"unknown link type {link['type']}")
    to_id = labels[link['label']]
    link_type, reverse = ISSUE_LINK_TYPES_MAP[link['type']]
    if reverse:
        from_id, to_id = to_id, from_id
    return Link(link_type, from_id, to_id)


def _read_script(filename):
    with open(filename) as file:
        data = yaml.safe_load(file)

    schema_file = bjira.__path__[0] + "/schema/script_schema.yaml"
    validator = Core(source_data=data, schema_files=[schema_file])

    try:
        validator.validate()
    except Exception as e:
        print("Wrong script file format:")
        print(e)
        return None

    _issues = data['issues']
    issues = [_process_issue(issue) for issue in _issues]
    labels = {issue['label']: idx for idx, issue in enumerate(_issues) if 'label' in issue}
    links = list(chain.from_iterable([_process_link(idx, link, labels) for link in issue['links']]
                                     for idx, issue in enumerate(_issues) if 'links' in issue))

    Script = namedtuple('Script', ['issues', 'links', 'parent', 'storypoints'])
    parent_storypoints = None
    portfolio_parent = False
    if 'parent' in data:
        Parent = namedtuple('Parent', ['key', 'tax', 'link_type'])
        parent = Parent(
            key=data['parent']['key'],
            tax=data['parent']['tax'] if 'tax' in data['parent'] else False,
            link_type=data['parent']['link_type'])
        if 'storypoints' in parent:
            parent_storypoints = parent['storypoints']
        if parent.key.startswith(PORTFOLIO_PROJECT_ID):
            portfolio_parent = True
    else:
        parent = None

    total_storypoints = None
    if portfolio_parent and parent_storypoints:
        total_storypoints = float(parent_storypoints)
    elif portfolio_parent and any(issue.storypoints for issue in issues):
        total_storypoints = SUM_STORYPOINTS
    return Script(issues=issues, links=links, parent=parent, storypoints=total_storypoints)


class Operation(create.Operation):
    def __init__(self):
        super().__init__()
        self.dryrun = None
        self.jira_api = self.get_jira_api()
        self.dryrun_counter = None

    def configure_arg_parser(self, subparsers):
        parser = subparsers.add_parser('script', help='create issues using script')
        parser.add_argument(dest='script_file', help='path to script file')
        parser.add_argument(
            '--dryrun', dest='dryrun', default=False, action='store_true', help='just show params and exit'
        )
        parser.set_defaults(func=self._script_task)

    def _script_task(self, args):
        self.dryrun = args.dryrun
        data = _read_script(args.script_file)
        if not data:
            return
        parent = data.parent
        parent_link_type = ISSUE_LINK_TYPES_MAP[parent.link_type] if parent else None
        created_issues = []
        for issue in data.issues:
            created_issue = self._create_issue(issue, parent.tax)
            created_issues.append(created_issue.key)
            print(f'Created issue {created_issue.key}')
            if parent:
                link_type, reverse = parent_link_type
                self._create_issue_link(link_type, parent.key, created_issue.key, reverse)

        for link in data.links:
            inward = created_issues[link.inward]
            outward = created_issues[link.outward]
            self._create_issue_link(link.type, inward, outward, False)

        if data.storypoints == SUM_STORYPOINTS:
            if not self.dryrun:
                parent_issue = self.jira_api.issue(parent.key)
                parent_issue.update(fields={'customfield_39035': [{'id': '45091'}]})
            print(f'Mark issue {parent.key} as summing storypoints')
        elif data.storypoints:
            if not self.dryrun:
                parent_issue = self.jira_api.issue(parent.key)
                parent_issue.update(fields={
                    'customfield_39035': [],
                    'customfield_11212': data.storypoints,
                })
            print(f'Set storypoint for {parent.key} to {data.storypoints}')

    def _create_issue_link(self, link_type, inward, outward, reverse):
        if reverse:
            inward, outward = outward, inward
        if not self.dryrun:
            self.jira_api.create_issue_link(type=link_type, inwardIssue=inward, outwardIssue=outward)
        print(f"Created link of type {link_type} from {inward} to {outward}")

    def _create_issue(self, issue, tax):
        if issue.existing:
            return DummyIssue(issue.existing)
        (issue_type, proj_id) = TASK_MAPPING.get(issue.type.lower())
        sp = float(issue.storypoints) if issue.storypoints else None
        result = self.create_task(issue_type, proj_id, issue.name, self.get_team(),
                                  issue.description, None, sp, False,
                                  issue.service, None, tax)
        if result:
            return result
        elif self.dryrun:
            self.dryrun_counter = self.dryrun_counter + 1 if self.dryrun_counter else 12345678
            return DummyIssue(f'{proj_id}-{self.dryrun_counter}')
        else:
            raise Exception('Failed to create issue')

DummyIssue = namedtuple('DummyIssue', "key")
