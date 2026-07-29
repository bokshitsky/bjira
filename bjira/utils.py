import re
from collections import defaultdict, namedtuple

JIRA_SERVICE = 'bjira'

IMG_STATUS_PREFIX = {
    'Closed': '✅',
    'Resolved': '✅',
    'Released': '✅',
    'Deployed': '✅',
    'Fixed': '✅',
    'Open': '⭕️',
    'Reopened': '⭕️',
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


IssueLinkType = namedtuple('IssueLinkType', ['type_name', 'from_name', 'to_name'])


_ISSUE_LINK_TYPES = [
    IssueLinkType('Based', 'git based on', 'git based by'),
    IssueLinkType('Blocks', 'blocks', 'blocked by'),
    IssueLinkType('Cancellation', 'cancels', 'is cancelled by'),
    IssueLinkType('Cloners', 'clones', 'is cloned by'),
    IssueLinkType('Dependence', 'depends on', 'is depended by'),
    IssueLinkType('Duplicate', 'duplicates', 'is duplicated by'),
    IssueLinkType('Finish-to-Finish Dependency', 'FF-depends on', 'is FF-depended by'),
    IssueLinkType('Finish-to-Start Dependency', 'FS-depends on', 'is FS-depended by'),
    IssueLinkType('Fix', 'is a fix for', 'is fixed by'),
    IssueLinkType('Inclusion', 'includes', 'consists in'),
    IssueLinkType('Problem/Incident', 'causes', 'is caused by'),
    IssueLinkType('Relation', 'relates', 'is related by'),
    IssueLinkType('Risk mitigation', 'mitigates risk', 'is mitigated by'),
    IssueLinkType('Start-to-Finish Dependency', 'SF-depends on', 'is SF-depended by'),
    IssueLinkType('Start-to-Start Dependency', 'SS-depends on', 'is SS-depended by'),
    IssueLinkType('Проблема, разделенная', 'разделить на', 'разделить от'),
]

ISSUE_LINK_TYPES_MAP = {}
for link_type in _ISSUE_LINK_TYPES:
    ISSUE_LINK_TYPES_MAP[link_type.from_name] = (link_type.type_name, False)
    ISSUE_LINK_TYPES_MAP[link_type.to_name] = (link_type.type_name, True)
