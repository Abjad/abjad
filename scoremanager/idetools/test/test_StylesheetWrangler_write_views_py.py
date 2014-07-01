# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_write_views_py_01():

    input_ = 'red~example~score y ww y q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert 'Will write ...' in contents
    assert 'Wrote' in contents