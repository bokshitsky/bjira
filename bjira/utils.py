import re

JIRA_SERVICE = 'bjira'

IMG_STATUS_PREFIX = {
    'Closed': '✅',
    'Resolved': '✅',
    'Released': '✅',
    'Fixed': '✅',
    'Open': '⭕️',
    'In Progress': '⭕️',
    'Need Review': '⭕️',
}


def parse_portfolio_task(portfolio):
    return 'PORTFOLIO-' + re.sub('[^0-9]', '', portfolio)
