# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_quit_01():
    
    input_ = 'red~example~score m q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert contents


def test_MaterialPackageWrangler_quit_02():
    
    input_ = 'm q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert contents