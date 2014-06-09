# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.ide.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_display_available_commands_01():
    
    input_ = 'red~example~score m ? q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'materials - available commands' in contents


def test_MaterialPackageWrangler_display_available_commands_02():
    
    input_ = 'm ? q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'Abjad IDE - materials - available commands' in contents