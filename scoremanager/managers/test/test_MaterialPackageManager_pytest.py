# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialPackageManager_pytest_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score m tempo~inventory pyt default q'
    score_manager._run(pending_user_input=input_)
    contents = score_manager._transcript.contents

    assert 'Running py.test ...' in contents
    assert 'testable assets found' in contents