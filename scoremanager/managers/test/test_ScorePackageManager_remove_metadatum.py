# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScorePackageManager_remove_metadatum_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)

    # make sure no flavor_type metadatum found
    input_ = 'red~example~score mdg flavor_type default q'
    score_manager._run(input_=input_)
    assert 'None' in score_manager._transcript.contents

    # add flavor_type metadatum
    input_ = 'red~example~score mda flavor_type cherry q'
    score_manager._run(input_=input_)

    # maker sure flavor_type metadatum now equal to 'cherry'
    input_ = 'red~example~score mdg flavor_type default q'
    score_manager._run(input_=input_)
    assert "'cherry'" in score_manager._transcript.contents

    # remove flavor_type metadatum
    input_ = 'red~example~score mdrm flavor_type default q'
    score_manager._run(input_=input_)

    # make sure no flavor_type metadatum found
    input_ = 'red~example~score mdg flavor_type default q'
    score_manager._run(input_=input_)
    assert 'None' in score_manager._transcript.contents