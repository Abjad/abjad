# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_edit_metadata_py_01():

    input_ = 'red~example~score k mde q'
    ide._run(input_=input_)

    assert ide._session._attempted_to_open_file