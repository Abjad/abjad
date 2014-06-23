# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_AbjadIDE_repository_clean_every_asset_01():

        input_ = '** rcn* q'
        score_manager._run(input_=input_)
        assert score_manager._session._attempted_repository_clean