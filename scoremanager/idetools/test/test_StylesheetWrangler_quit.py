# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_quit_01():
    
    input_ = 'red~example~score y q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert contents


def test_StylesheetWrangler_quit_02():
    
    input_ = 'Y q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert contents