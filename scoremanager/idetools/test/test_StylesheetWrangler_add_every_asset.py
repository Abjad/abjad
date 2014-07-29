# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_add_every_asset_01():
    r'''Flow control reaches method in score.
    '''

    ide._session._is_repository_test = True
    input_ = 'red~example~score y rad* q'
    ide._run(input_=input_)
    assert ide._session._attempted_to_add


def test_StylesheetWrangler_add_every_asset_02():
    r'''Flow control reaches method in library.
    '''

    ide._session._is_repository_test = True
    input_ = 'yy rad* q'
    ide._run(input_=input_)
    assert ide._session._attempted_to_add