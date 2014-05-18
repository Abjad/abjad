# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_DistributionFileWrangler_open_lilypond_log_01():
    r'''In score.
    '''

    input_ = 'red~example~score d ll q'
    score_manager._run(pending_input=input_)
    
    assert score_manager._session._attempted_to_open_file


def test_DistributionFileWrangler_open_lilypond_log_02():
    r'''Out of score.
    '''

    input_ = 'd ll q'
    score_manager._run(pending_input=input_)
    
    assert score_manager._session._attempted_to_open_file