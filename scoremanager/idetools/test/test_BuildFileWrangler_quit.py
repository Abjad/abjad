# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_quit_01():
    
    input_ = 'red~example~score u q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert contents


def test_BuildFileWrangler_quit_02():
    
    input_ = 'uu q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert contents