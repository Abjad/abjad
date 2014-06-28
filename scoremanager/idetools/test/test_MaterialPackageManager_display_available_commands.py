# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageManager_display_available_commands_01():
    
    input_ = 'red~example~score m tempo~inventory ?? q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert 'tempo inventory - available commands' in contents