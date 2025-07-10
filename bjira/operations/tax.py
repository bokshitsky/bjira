from bjira.operations import BJiraOperation
from bjira.utils import parse_portfolio_task

DEFAULT_TAX_FIELDS = {
    'customfield_35513': {'id': '38846'},
    'customfield_37951': [{'id': '42875'}],
    'customfield_32210': [{'id': '34781'}],
}


class Operation(BJiraOperation):
    def configure_arg_parser(self, subparsers):
        parser_defense = subparsers.add_parser('tax', help='fill galochki for tax portfolio')
        parser_defense.add_argument(dest='portfolio', help='portfolio', nargs=1)
        parser_defense.set_defaults(func=self._fill_galochki)

    def _fill_galochki(self, args):
        jira_api = self.get_jira_api()
        issue = jira_api.issue(parse_portfolio_task(args.portfolio[0]))
        print(f'filling all required galochkas for {self.get_task_url(issue.key)}')
        issue.update(fields=DEFAULT_TAX_FIELDS)
