# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_PackageManager__display_status_command_01():

    manager = ide._score_package_wrangler._find_up_to_date_manager(
        repository='git',
        system=True,
        )

    command = 'git status {}'.format(manager._path)
    assert manager._display_status_command == command


def test_PackageManager__display_status_command_02():

    manager = ide._score_package_wrangler._find_up_to_date_manager(
        repository='svn',
        system=False,
        )

    if manager is None:
        return

    command = 'svn st {}'.format(manager._path)
    assert manager._display_status_command == command