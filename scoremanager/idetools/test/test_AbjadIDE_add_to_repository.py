# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_add_to_repository_01():
    r'''Flow control reaches method.
    '''

    score_manager._session._is_repository_test = True
    input_ = '** rad q'
    score_manager._run(input_=input_)
    assert score_manager._session._attempted_to_add_to_repository