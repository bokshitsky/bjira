import time
from datetime import datetime

from bjira.operations import BJiraOperation

TEXT_TO_SEARCH = ('macbook', 'lenovo', 'apple', 'ноутбук', 'техника')

threshold = datetime(2021, 10, 20, 17, 59, 50)

class Operation(BJiraOperation):

    def configure_arg_parser(self, subparsers):
        parser = subparsers.add_parser('giner_back', help='buy everything')
        parser.set_defaults(func=self._buy_everything)

    def _buy_everything(self, args):
        jira_api = self.get_jira_api()
        print('Запускаю Гинера...')
        while True:
            try:
                found_issues = jira_api.search_issues(f'project = "BUYNOW" AND status = 24299 ORDER BY key DESC', maxResults=100)
                for issue in found_issues:
                    summary = issue.fields.summary
                    description = f'{self.get_task_url(issue.key)}: {summary}'

                    if not self._is_interesting_issue(issue):
                        print(f'{datetime.now()} Игнорирую {description}')
                        continue

                    try:
                        print(f'{datetime.now()} Покупаю {description}')
                        jira_api.transition_issue(issue, transition='21')
                    except Exception as e:
                        print(f'Ошибка при покупке {description}')

            except Exception as e:
                print(e)
            try:
                if datetime.now() < threshold:
                    time.sleep(2)
            except KeyboardInterrupt:
                print('Гинер всё купил')
                return


    def _is_interesting_issue(self, issue):
        return any(word in issue.fields.summary.lower() for word in TEXT_TO_SEARCH)
