# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_write_every_metadata_py_01():

    input_ = 'mdw* n q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert 'Will write ...' in contents
    assert '__metadata__.py' in contents