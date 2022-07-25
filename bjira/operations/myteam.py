from bjira.operations import BJiraOperation


class Operation(BJiraOperation):

    def configure_arg_parser(self, subparsers):
        parser = subparsers.add_parser('myteam', help='show my team tasks')
        parser.add_argument(dest='limit', type=int, default=10, help='limit', nargs='?')
        parser.set_defaults(func=self._execute_search)

    def _execute_search(self, args):
        api = self.get_jira_api()
        found_issues = api.search_issues(f'"Development Team" = "{self.get_team()}" ORDER BY updated DESC',
                                         maxResults=args.limit)
        max_len = max(len(issue.permalink()) for issue in found_issues)
        for issue in found_issues:
            print(f'{issue.permalink().ljust(max_len)} [{issue.fields.assignee}] {issue.fields.summary[:80]}')
