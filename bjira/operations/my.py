from bjira.operations import BJiraOperation


class Operation(BJiraOperation):
    def configure_arg_parser(self, subparsers):
        parser = subparsers.add_parser("my", help="show my tasks")
        parser.add_argument(dest="limit", type=int, default=10, help="limit", nargs="?")
        parser.add_argument("-t", "--types", nargs="+", default=[])
        parser.add_argument("-s", dest="search", default=None)
        parser.set_defaults(func=self._execute_search)

    def _execute_search(self, args):
        api = self.get_jira_api()
        user = self.get_user()

        project_filter_clause = ""
        if args.types:
            project_filter_clause = "and project in (" + ",".join(f'"{t}"' for t in args.types) + ")"

        project_search_clause = ""
        if args.search:
            project_search_clause = f"and (text ~ {args.search} or labels = {args.search})"

        found_issues = api.search_issues(
            f"(reporter = {user} or assignee = {user}) {project_filter_clause} {project_search_clause} ORDER BY created DESC",
            maxResults=args.limit,
        )
        max_len_link = max(len(issue.permalink()) for issue in found_issues)
        max_len_status = max(len(str(issue.fields.status)) for issue in found_issues)
        for issue in found_issues:
            print(
                f"{str(issue.fields.status).ljust(max_len_status)} {issue.permalink().ljust(max_len_link)} {issue.fields.summary[:80]}"
            )

        return MyResult(found_issues)


class MyResult:
    def __init__(self, found_issues):
        self.found_issues = found_issues
