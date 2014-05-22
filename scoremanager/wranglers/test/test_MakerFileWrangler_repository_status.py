# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MakerFileWrangler_repository_status_01():
    r'''Works with library.
    '''

    input_ = 'k rst q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents

    assert 'On branch master' in contents


def test_MakerFileWrangler_repository_status_02():
    r'''Works with Git-managed makers directory.
    '''

    input_ = 'red~example~score k rst q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents

    assert 'On branch master' in contents


def test_MakerFileWrangler_repository_status_03():
    r'''Works with Subversion-managed makers directory.
    '''

    score_name = score_manager._score_package_wrangler._find_svn_score_name()
    if not score_name:
        return

    input_ = '{} k rst q'.format(score_name)
    score_manager._run(pending_input=input_)

    assert '> rst' in score_manager._transcript.first_lines