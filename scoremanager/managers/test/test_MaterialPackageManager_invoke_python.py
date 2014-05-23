# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageManager_invoke_python_01():
    
    input_ = 'red~example~score m tempo~inventory pyi 2**38 q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert '274877906944' in contents