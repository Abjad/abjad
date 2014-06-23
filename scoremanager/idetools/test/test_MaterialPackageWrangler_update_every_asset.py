# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
score_manager._session._is_repository_test = True


def test_MaterialPackageWrangler_update_every_asset_01():
    r'''Works in score.
    '''

    input_ = 'red~example~score m rup* q'
    score_manager._run(input_=input_)
    assert score_manager._session._attempted_to_update


def test_MaterialPackageWrangler_update_every_asset_02():
    r'''Works in library.
    '''

    input_ = 'M rup* q'
    score_manager._run(input_=input_)
    assert score_manager._session._attempted_to_update