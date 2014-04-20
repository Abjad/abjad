# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScorePackageWrangler_repository_status_01():
    r'''Works with all scores.
    '''

    input_ = 'ssl rst q'
    score_manager._run(pending_user_input=input_)
    titles = score_manager._transcript.titles

    assert titles[-1] == '# On branch master'


def test_ScorePackageWrangler_repository_status_02():
    r'''Works with active scores.
    '''

    input_ = 'ssv rst q'
    score_manager._run(pending_user_input=input_)

    assert '...' in score_manager._transcript.contents


def test_ScorePackageWrangler_repository_status_03():
    r'''Works with example scores.
    '''

    input_ = 'ssx rst q'
    score_manager._run(pending_user_input=input_)
    titles = score_manager._transcript.titles

    assert titles[-1] == '# On branch master'