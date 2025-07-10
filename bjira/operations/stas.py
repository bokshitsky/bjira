from bjira.operations import BJiraOperation
from bjira.utils import parse_portfolio_task


class Operation(BJiraOperation):
    def configure_arg_parser(self, subparsers):
        for short_name in ('stas', 'defense'):
            parser_defense = subparsers.add_parser(short_name, help='fill portfolio defense galochka')
            parser_defense.add_argument(dest='portfolio', help='portfolio', nargs=1)
            parser_defense.set_defaults(func=self._fill_defense_galochka)

    def _fill_defense_galochka(self, args):
        jira_api = self.get_jira_api()
        issue = jira_api.issue(parse_portfolio_task(args.portfolio[0]))
        print(f'filling "ya proveril bezopasnost" galochka for {self.get_task_url(issue.key)}')
        issue.update(fields={'customfield_32210': [{'id': '34781'}]})
