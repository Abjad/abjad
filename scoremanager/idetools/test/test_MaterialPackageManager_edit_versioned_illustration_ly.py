# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageManager_edit_versioned_illustration_ly_01():

    input_ = 'red~example~score m tempo~inventory vie 1 q'
    ide._run(input_=input_)

    assert ide._session._attempted_to_open_file