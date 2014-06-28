# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_ScorePackageManager_display_status_01():
    r'''Works with Git.
    '''

    input_ = 'red~example~score rst q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents


def test_ScorePackageManager_display_status_02():
    r'''Works with Subversion.
    '''

    ide = scoremanager.idetools.AbjadIDE(is_test=False)
    name = ide._score_package_wrangler._find_svn_score_name()
    if not name:
        return

    input_ = '{} rst q'.format(name)
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents