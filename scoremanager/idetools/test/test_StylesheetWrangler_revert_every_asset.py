# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_revert_every_asset_01():

    ide._session._is_repository_test = True
    input_ = 'red~example~score y rrv* q'
    ide._run(input_=input_)
    assert ide._session._attempted_to_revert


def test_StylesheetWrangler_revert_every_asset_02():

    ide._session._is_repository_test = True
    input_ = 'yy rrv* q'
    ide._run(input_=input_)
    assert ide._session._attempted_to_revert