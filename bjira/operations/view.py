import webbrowser

import git

from bjira.operations import BJiraOperation


class Operation(BJiraOperation):

    def configure_arg_parser(self, subparsers):
        parser = subparsers.add_parser('view', help='view jira task in browser')
        parser.add_argument(dest='task_name', nargs='?', help='task name')
        parser.set_defaults(func=self._view_jira_task)

    def _view_jira_task(self, args):
        task_name = self._get_task_name(args)
        if task_name:
            print(f'opening task https://jira.hh.ru/browse/{task_name}')
            webbrowser.open(f"https://jira.hh.ru/browse/{task_name}")

    def _get_task_name(self, args):
        if args.task_name is not None:
            return args.task_name
        try:
            repo = git.Repo('.', search_parent_directories=True)
            return repo.active_branch.name
        except git.exc.InvalidGitRepositoryError:
            print('you have to specify task_name or to be in a git-repository')
