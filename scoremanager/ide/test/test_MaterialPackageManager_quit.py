# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.ide.AbjadIDE(is_test=True)


def test_MaterialPackageManager_quit_01():
    
    input_ = 'red~example~score m tempo~inventory q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert contents