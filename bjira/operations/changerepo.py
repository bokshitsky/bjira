from bjira.operations import BJiraOperation


class Operation(BJiraOperation):
    def configure_arg_parser(self, subparsers):
        parser = subparsers.add_parser("changerepo", help="show my tasks")
        parser.set_defaults(func=self._execute_search)

    def _execute_search(self, args):
        api = self.get_jira_api()

        found_issues = api.search_issues(
            f'project = "R&D :: Development (HH)" AND Repository in (hh.sites.main) AND status not in (Released, Closed)',
            maxResults=30,
        )

        max_len = max(len(issue.permalink()) for issue in found_issues)
        for issue in found_issues:
            print(f"{issue.permalink().ljust(max_len)} {issue.fields.summary[:80]}")
            issue.update(fields={'customfield_12623': [{'value': "xhh"}]})
