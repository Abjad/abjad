# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialManager_add_metadatum_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)

    # make sure no flavor_type metadatum found
    input_ = 'lmm example~numbers mdg flavor_type default q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.entries[-4].title == 'None'

    # add flavor_type metadatum
    input_ = 'lmm example~numbers mda flavor_type cherry q'
    score_manager._run(pending_user_input=input_)

    # maker sure flavor_type metadatum now equal to 'cherry'
    input_ = 'lmm example~numbers mdg flavor_type default q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.entries[-4].title == "'cherry'"

    # remove flavor_type metadatum
    input_ = 'lmm example~numbers mdrm flavor_type default q'
    score_manager._run(pending_user_input=input_)

    # make sure no flavor_type metadatum found
    input_ = 'lmm example~numbers mdg flavor_type default q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.entries[-4].title == 'None'
