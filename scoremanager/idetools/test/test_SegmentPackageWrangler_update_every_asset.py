# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_SegmentPackageWrangler_update_every_asset_01():
    r'''Works in score.
    '''

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    score_manager._session._is_repository_test = True
    input_ = 'red~example~score g rup* q'
    score_manager._run(input_=input_)
    assert score_manager._session._attempted_to_update


def test_SegmentPackageWrangler_update_every_asset_02():
    r'''Works in library.
    '''

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    score_manager._session._is_repository_test = True
    input_ = 'G rup* q'
    score_manager._run(input_=input_)
    assert score_manager._session._attempted_to_update