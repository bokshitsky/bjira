import re
from collections import defaultdict

JIRA_SERVICE = 'bjira'

IMG_STATUS_PREFIX = {
    'Closed': '✅',
    'Resolved': '✅',
    'Released': '✅',
    'Fixed': '✅',
    'Open': '⭕️',
    'In Progress': '⭕️',
    'In progress': '⭕️',
    'Need Review': '⭕️',
    'Backlog': '⭕️',
    'Planned Backlog': '⭕️',
    'Rejected': '❌',
}

STATUS_ALIASES = defaultdict(list)
for status, img in IMG_STATUS_PREFIX.items():
    symbols = {
        '✅': ['y', 'v'],
        '⭕️': ['o'],
        '❌': ['x'],
    }[img.strip()]
    for symbol in symbols:
        STATUS_ALIASES[symbol].append(status)
        STATUS_ALIASES[symbol.upper()].append(status)


def parse_portfolio_task(portfolio):
    return 'PORTFOLIO-' + re.sub('[^0-9]', '', portfolio)
