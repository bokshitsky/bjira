import argparse

from bjira.operations import BJiraOperation


class Operation(BJiraOperation):
    def configure_arg_parser(self, subparsers):
        parser = subparsers.add_parser("search", help="search tasks")
        parser.add_argument(dest="limit", type=int, default=10, help="limit", nargs="?")
        parser.add_argument("-t", "--types", nargs="+", default=[])
        parser.add_argument("-st", "--statuses", nargs="+", default=[])
        parser.add_argument("-s", dest="search", default=None)
        parser.add_argument("-m", "--my", dest="my", action=argparse.BooleanOptionalAction)
        parser.set_defaults(func=self._execute_search)

    def _execute_search(self, args):
        api = self.get_jira_api()
        user = api.current_user()

        predicate = ""
        if args.my:
            predicate = f"(reporter = {user} or assignee = {user})"

        if args.types:
            if predicate:
                predicate += " and "
            predicate += "project in (" + ",".join(f'"{t}"' for t in args.types) + ")"

        if args.statuses:
            if predicate:
                predicate += " and "
            predicate += "status in (" + ",".join(f'"{t}"' for t in args.statuses) + ")"

        if args.search:
            if predicate:
                predicate += " and "
            predicate += f"(text ~ {args.search} or labels = {args.search})"

        query = f"{predicate} ORDER BY created DESC".strip()
        print(f"query: {query}")
        found_issues = api.search_issues(query, maxResults=args.limit)
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
