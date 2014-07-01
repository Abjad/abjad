# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_SegmentPackageManager_edit_definition_py_01():

    ide = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score g A de q'
    ide._run(input_=input_)

    assert ide._session._attempted_to_open_file