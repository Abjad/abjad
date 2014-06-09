# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.ide.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_display_available_commands_01():
    
    input_ = 'red~example~score g ? q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'segments - available commands' in contents


def test_SegmentPackageWrangler_display_available_commands_02():
    
    input_ = 'g ? q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'Abjad IDE - segments - available commands' in contents