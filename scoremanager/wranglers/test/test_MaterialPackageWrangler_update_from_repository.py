# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)
score_manager._session._is_repository_test = True


def test_MaterialPackageWrangler_update_from_repository_01():
    r'''Works in score.
    '''

    input_ = 'red~example~score m rup <return> q'
    score_manager._run(input_=input_)
    assert score_manager._session._attempted_to_update_from_repository


def test_MaterialPackageWrangler_update_from_repository_02():
    r'''Works in library.
    '''

    input_ = 'm rup <return> q'
    score_manager._run(input_=input_)
    assert score_manager._session._attempted_to_update_from_repository