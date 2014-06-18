# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_DistributionFileWrangler_display_available_commands_01():
    
    input_ = 'red~example~score d ?? q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'distribution files - available commands' in contents


def test_DistributionFileWrangler_display_available_commands_02():
    
    input_ = 'D ?? q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    string = 'Abjad IDE - distribution files - available commands'
    assert string in contents