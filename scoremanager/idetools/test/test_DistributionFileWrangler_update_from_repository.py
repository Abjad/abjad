# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_DistributionFileWrangler_update_from_repository_01():
    r'''Works in score.
    '''

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    score_manager._session._is_repository_test = True
    input_ = 'red~example~score d rup* q'
    score_manager._run(input_=input_)
    assert score_manager._session._attempted_to_update_from_repository


def test_DistributionFileWrangler_update_from_repository_02():
    r'''Works in library.
    '''

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    score_manager._session._is_repository_test = True
    input_ = 'D rup* q'
    score_manager._run(input_=input_)
    assert score_manager._session._attempted_to_update_from_repository