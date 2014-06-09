# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.ide.AbjadIDE(is_test=True)


def test_ScorePackageManager_repository_status_01():
    r'''Works with Git.
    '''

    input_ = 'red~example~score rst q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents


def test_ScorePackageManager_repository_status_02():
    r'''Works with Subversion.
    '''

    name = score_manager._score_package_wrangler._find_svn_score_name()
    if not name:
        return

    input_ = '{} rst q'.format(name)
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents