# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialPackageManager_edit_illustrate_py_01():

    ide = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score m magic~numbers le q'
    ide._run(input_=input_)

    assert ide._session._attempted_to_open_file