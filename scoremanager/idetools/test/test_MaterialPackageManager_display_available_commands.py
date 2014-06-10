# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageManager_display_available_commands_01():
    
    input_ = 'red~example~score m tempo~inventory ? q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'tempo inventory (O) - available commands' in contents