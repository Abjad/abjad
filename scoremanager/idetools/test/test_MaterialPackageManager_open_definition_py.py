# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialPackageManager_open_definition_py_01():

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score m magic~numbers do q'
    score_manager._run(input_=input_)

    assert score_manager._session._attempted_to_open_file