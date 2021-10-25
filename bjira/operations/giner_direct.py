import time
from datetime import datetime

from bjira.operations import BJiraOperation


TEXT_TO_SEARCH = ('macbook', 'lenovo', 'apple', 'ноутбук', 'техника')

start_time = datetime(2021, 10, 20, 17, 59, 55)

class Operation(BJiraOperation):

    def configure_arg_parser(self, subparsers):
        parser = subparsers.add_parser('giner_direct', help='buy everything')
        parser.set_defaults(func=self._buy_everything)

    def _buy_everything(self, args):
        jira_api = self.get_jira_api()
        current = 50
        while True:
            try:
                issue = jira_api.issue(f'BUYNOW-{current}')
                print('нашел ' + str(current))
                current += 1
                if self._is_interesting_issue(issue):
                    try:
                        print(f'покупаю {self.get_task_url(issue.key)}: {issue.fields.summary}')
                        jira_api.transition_issue(issue, transition='21')
                    except:
                        pass

            except:
                print("не нашел")

            if datetime.now() < start_time:
                time.sleep(2)



    def _is_interesting_issue(self, issue):
        summary = issue.fields.summary.lower()
        return any(word in summary for word in TEXT_TO_SEARCH)
