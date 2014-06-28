# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_edit_front_cover_source_01():

    input_ = 'red~example~score u fce q'
    ide._run(input_=input_)

    assert ide._session._attempted_to_open_file