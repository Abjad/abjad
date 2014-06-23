# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_update_from_repository_01():
    r'''Works in score.
    '''

    score_manager._session._is_repository_test = True
    input_ = 'red~example~score y rup* q'
    score_manager._run(input_=input_)
    assert score_manager._session._attempted_to_update_from_repository


def test_StylesheetWrangler_update_from_repository_02():
    r'''Works in library.
    '''

    score_manager._session._is_repository_test = True
    input_ = 'Y rup* q'
    score_manager._run(input_=input_)
    assert score_manager._session._attempted_to_update_from_repository