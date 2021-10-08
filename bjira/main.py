#!/usr/bin/env python3
import argparse

from bjira.operations.create import CreateJiraTask
from bjira.operations.view import ViewJiraTask
from bjira.operations.my import ShowMyTasks
from bjira.operations.setpass import SetPasswordTask
from bjira.operations.stas import FillDefenseGalochkaTask


def _parse_args():
    parser = argparse.ArgumentParser(description='jira helper')
    subparsers = parser.add_subparsers(help='sub-command help', required=True)

    for task in (CreateJiraTask,
                 ViewJiraTask,
                 SetPasswordTask,
                 FillDefenseGalochkaTask,
                 ShowMyTasks):
        task().configure_arg_parser(subparsers)

    return parser.parse_args()


def main():
    args = _parse_args()
    args.func(args)
