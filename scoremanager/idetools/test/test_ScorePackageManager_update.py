# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)
ide._session._is_repository_test = True


def test_ScorePackageManager_update_01():

    input_ = 'red~example~score rup q'
    ide._run(input_=input_)
    assert ide._session._attempted_to_update