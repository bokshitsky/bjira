from bjira.operations import BJiraOperation
from bjira.utils import IMG_STATUS_PREFIX

DEFAULT_SUMMARY_LENGTH = 80

class Operation(BJiraOperation):
    def configure_arg_parser(self, subparsers):
        parser = subparsers.add_parser("search", help="search tasks")
        parser.add_argument(dest="limit", type=int, default=10, help="limit", nargs="?")
        parser.add_argument("-t", "--types", nargs="+", default=[])
        parser.add_argument("-dt", "--devteam", nargs="+", default=[])
        parser.add_argument("-st", "--statuses", nargs="+", default=[])
        parser.add_argument("-s", dest="search", default=None)
        parser.add_argument("-m", "--my", dest="my", nargs="?", default=[])
        parser.add_argument("-tr", "--trim", dest="trim_output", type=int, default=None)
        parser.set_defaults(func=self._execute_search)

    def _execute_search(self, args):
        api = self.get_jira_api()
        user = api.current_user()
        predicate = ""

        if args.my is None:  # if -m flag is set without any arguments
            args.my = ["assignee", "reporter"]
        if isinstance(args.my, str):
            args.my = [args.my]
        if args.my:
            predicate = "(" + " or ".join(f"{field} = {user}" for field in args.my) + ")"

        if args.types:
            if predicate:
                predicate += " and "
            predicate += "project in (" + ",".join(f'"{t}"' for t in args.types) + ")"

        include_statuses = [st for st in (args.statuses or []) if not st.startswith("!")]
        if include_statuses:
            if predicate:
                predicate += " and "
            predicate += "status in (" + ",".join(f'"{t}"' for t in include_statuses) + ")"

        exclude_statuses = [st.removeprefix("!") for st in (args.statuses or []) if st.startswith("!")]
        if exclude_statuses:
            if predicate:
                predicate += " and "
            predicate += "status not in (" + ",".join(f'"{t}"' for t in exclude_statuses) + ")"

        if args.search:
            if predicate:
                predicate += " and "
            predicate += f"(text ~ {args.search} or labels = {args.search})"

        if args.devteam:
            if predicate:
                predicate += " and "
            predicate += '"Development Team" in (' + ",".join(f'"{t}"' for t in args.devteam) + ")"

        query = f"{predicate} ORDER BY created DESC".strip()
        print(f"query: {query}")
        found_issues = api.search_issues(query, maxResults=args.limit)
        max_len_link = max(len(issue.permalink()) for issue in found_issues)
        max_len_status = max(len(str(issue.fields.status)) for issue in found_issues)
        for issue in found_issues:
            img = IMG_STATUS_PREFIX.get(str(issue.fields.status), '❔')
            output_line = (
                f"{img} {str(issue.fields.status).ljust(max_len_status)} {issue.permalink().ljust(max_len_link)} {issue.fields.summary[:DEFAULT_SUMMARY_LENGTH]}"
            )
            print(output_line[:args.trim_output])


        return MyResult(found_issues)


class MyResult:
    def __init__(self, found_issues):
        self.found_issues = found_issues
