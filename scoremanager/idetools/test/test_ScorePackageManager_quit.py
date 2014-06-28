# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_ScorePackageManager_quit_01():
    
    input_ = 'red~example~score q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert contents