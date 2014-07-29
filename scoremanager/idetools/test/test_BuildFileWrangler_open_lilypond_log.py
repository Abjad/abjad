# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_open_lilypond_log_01():
    r'''In score.
    '''

    input_ = 'red~example~score u ll q'
    ide._run(input_=input_)
    
    assert ide._session._attempted_to_open_file


def test_BuildFileWrangler_open_lilypond_log_02():
    r'''Out of score.
    '''

    input_ = 'uu ll q'
    ide._run(input_=input_)
    
    assert ide._session._attempted_to_open_file