# -*- encoding: utf-8 -*-
import scoremanager


def test_SegmentPackageWrangler_revert_every_asset_01():

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    score_manager._session._is_repository_test = True
    input_ = 'red~example~score g rrv* q'
    score_manager._run(input_=input_)
    assert score_manager._session._attempted_to_revert


def test_SegmentPackageWrangler_revert_every_asset_02():

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    score_manager._session._is_repository_test = True
    input_ = 'G rrv* q'
    score_manager._run(input_=input_)
    assert score_manager._session._attempted_to_revert