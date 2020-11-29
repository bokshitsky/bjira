import re

JIRA_SERVICE = 'bjira'


def parse_portfolio_task(portfolio):
    return 'PORTFOLIO-' + re.sub('[^0-9]', '', portfolio)
