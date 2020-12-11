#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name='bjira',
    version='0.0.5',
    description='CLI utils for hh jira',
    author='Evgeniy Bokshitskiy',
    author_email='e.bokshitskiy@hh.ru',
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=[
        'keyring==21.2.1',
        'jira==2.0.0',
        'GitPython>=3.1.11',
    ],
    entry_points={
        'console_scripts': [
            'bjira = bjira.main:main',
        ],
    },
)
