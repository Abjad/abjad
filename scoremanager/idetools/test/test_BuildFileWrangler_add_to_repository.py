# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_BuildFileWrangler_add_to_repository_01():
    r'''Flow control reaches method in score.
    '''

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    score_manager._session._is_repository_test = True
    input_ = 'red~example~score u rad q'
    score_manager._run(input_=input_)
    assert score_manager._session._attempted_to_add_to_repository


def test_BuildFileWrangler_add_to_repository_02():
    r'''Flow control reaches method in library.
    '''

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    score_manager._session._is_repository_test = True
    input_ = 'U rad q'
    score_manager._run(input_=input_)
    assert score_manager._session._attempted_to_add_to_repository