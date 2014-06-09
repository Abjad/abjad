# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScorePackageWrangler_add_to_repository_01():
    r'''Flow control reaches add.
    '''

    score_manager = scoremanager.iotools.AbjadIDE(is_test=True)
    score_manager._session._is_repository_test = True
    input_ = 'rad <return> q'
    score_manager._run(input_=input_)
    assert score_manager._session._attempted_to_add_to_repository