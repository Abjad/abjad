# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_update_every_asset_01():
    r'''Works in score.
    '''

    ide._session._is_repository_test = True
    input_ = 'red~example~score y rup* q'
    ide._run(input_=input_)
    assert ide._session._attempted_to_update


def test_StylesheetWrangler_update_every_asset_02():
    r'''Works in library.
    '''

    ide._session._is_repository_test = True
    input_ = 'yy rup* q'
    ide._run(input_=input_)
    assert ide._session._attempted_to_update