# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageManager_get_metadatum_01():

    # make sure no flavor metadatum found
    input_ = 'red~example~score g A mdg flavor <return> q'
    score_manager._run(input_=input_)
    assert 'None' in score_manager._transcript.contents

    # add flavor metadatum
    input_ = 'red~example~score g A mda flavor cherry q'
    score_manager._run(input_=input_)

    # maker sure flavor metadatum now equal to 'cherry'
    input_ = 'red~example~score g A mdg flavor <return> q'
    score_manager._run(input_=input_)
    assert "'cherry'" in score_manager._transcript.contents

    # remove flavor metadatum
    input_ = 'red~example~score g A mdrm flavor <return> q'
    score_manager._run(input_=input_)

    # make sure no flavor metadatum found
    input_ = 'red~example~score g A mdg flavor <return> q'
    score_manager._run(input_=input_)
    assert 'None' in score_manager._transcript.contents