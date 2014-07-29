# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_quit_01():
    
    input_ = 'red~example~score k q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert contents


def test_MakerFileWrangler_quit_02():
    
    input_ = 'kk q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert contents