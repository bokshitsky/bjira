from bjira.operations import BJiraOperation


class Operation(BJiraOperation):

    def configure_arg_parser(self, subparsers):
        parser = subparsers.add_parser('my', help='show my tasks')
        parser.add_argument(dest='limit', type=int, default=10, help='limit', nargs='?')
        parser.set_defaults(func=self._execute_search)

    def _execute_search(self, args):
        api = self.get_jira_api()
        user = self.get_user()
        found_issues = api.search_issues(f'(reporter = {user} or assignee = {user}) ORDER BY created DESC',
                                         maxResults=args.limit)
        max_len = max(len(issue.permalink()) for issue in found_issues)
        for issue in found_issues:
            print(f'{issue.permalink().ljust(max_len)} {issue.fields.summary[:80]}')

        return MyResult(found_issues)


class MyResult:

    def __init__(self, found_issues):
        self.found_issues = found_issues
