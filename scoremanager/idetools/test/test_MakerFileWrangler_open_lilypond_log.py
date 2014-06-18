# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_open_lilypond_log_01():
    r'''In score.
    '''

    input_ = 'red~example~score k log q'
    score_manager._run(input_=input_)
    
    assert score_manager._session._attempted_to_open_file


def test_MakerFileWrangler_open_lilypond_log_02():
    r'''Out of score.
    '''

    input_ = 'K log q'
    score_manager._run(input_=input_)
    
    assert score_manager._session._attempted_to_open_file