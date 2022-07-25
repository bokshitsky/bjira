#!/usr/bin/env python3
import argparse
from importlib import import_module
from pkgutil import walk_packages

import bjira.operations


def _parse_args():
    parser = argparse.ArgumentParser(description='jira helper')
    subparsers = parser.add_subparsers(help='sub-command help', required=True)

    for module_info in walk_packages(bjira.operations.__path__, bjira.operations.__name__ + '.'):
        import_module(module_info.name).Operation().configure_arg_parser(subparsers)

    return parser.parse_args()


def main():
    args = _parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
