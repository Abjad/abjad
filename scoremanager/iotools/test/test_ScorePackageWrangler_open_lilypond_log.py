# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.iotools.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_open_lilypond_log_01():

    input_ = 'u log q'
    score_manager._run(input_=input_)
    
    assert score_manager._session._attempted_to_open_file