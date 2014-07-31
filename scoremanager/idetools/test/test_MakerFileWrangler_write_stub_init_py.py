# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_write_stub_init_py_01():

    input_ = 'red~example~score k ns y q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert 'Will write stub to' in contents