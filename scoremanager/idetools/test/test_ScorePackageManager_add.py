# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_ScorePackageManager_add_01():
    r'''Add two files to Git-managed score package.
    Make sure Git recognizes the files as added.
    Then unadd the files and leave the score package as found.
    '''

    manager = ide._score_package_wrangler._find_up_to_date_manager(
        repository='git',
        system=True,
        )

    assert manager._test_add()


def test_ScorePackageManager_add_02():
    r'''Add two files to Subversioned-managed score package.
    Make sure Subversion recognizes the files as added.
    Then unadd the file and leave the score package as found.
    '''

    manager = ide._score_package_wrangler._find_up_to_date_manager(
        repository='svn',
        system=False,
        )

    if not manager:
        return

    assert manager._test_add()


def test_ScorePackageManager_add_03():
    r'''Displays informative message when nothing to add.
    '''

    input_ = 'red~example~score rad q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert 'Nothing to add.' in contents