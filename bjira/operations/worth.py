from bjira.operations import BJiraOperation
from bjira.utils import parse_portfolio_task

WORTH_FOR_USERS = {
    '-1': ('-1', 'Не заполнено'),
    '0': ('38846',  'Для пользователя вообще ничего не меняется (например tax)'),
    '1': ('38845',  'Минорное изменение взаимодействия пользователя с продуктом'),
    '2': ('38844',  'Немного меняет взаимодействие пользователя с продуктом'),
    '3': ('38843',  'Существенно меняет взаимодействие пользователя с продуктом')
}


class Operation(BJiraOperation):

    def configure_arg_parser(self, subparsers):
        parser = subparsers.add_parser('worth', help='fill worth for users in PORTFOLIO')
        parser.add_argument(dest='portfolio', help='portfolio', nargs=1)
        parser.add_argument(dest='worth_id', help='worth index 0..3. 0 - tax, 3 - significant changes', nargs=1)
        parser.set_defaults(func=self._fill_worth_for_users)

    def _fill_worth_for_users(self, args):
        jira_api = self.get_jira_api()
        worth_argument_index = args.worth_id[0]
        worth_id, worth_description = WORTH_FOR_USERS.get(worth_argument_index)

        issue = jira_api.issue(parse_portfolio_task(args.portfolio[0]))
        print(f'filling "worth for users" for {self.get_task_url(issue.key)} {worth_description}')
        issue.update(fields={'customfield_35513': {'id':  worth_id}})
