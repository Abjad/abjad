# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.AbjadIDE(is_test=True)


def test_DistributionFileWrangler_repository_status_01():
    r'''Works with distribution file library.
    '''

    input_ = 'd rst q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents


def test_DistributionFileWrangler_repository_status_02():
    r'''Works with Git-managed score.
    '''

    input_ = 'red~example~score d rst q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents


def test_DistributionFileWrangler_repository_status_03():
    r'''Works with Subversion-managed score.
    '''

    score_name = score_manager._score_package_wrangler._find_svn_score_name()
    if not score_name:
        return

    input_ = '{} d rst q'.format(score_name)
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents