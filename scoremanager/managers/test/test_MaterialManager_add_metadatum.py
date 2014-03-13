# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialManager_add_metadatum_01():

    score_manager = scoremanager.core.ScoreManager()

    # make sure no flavor_type metadatum found
    input_ = 'lmm example~numbers mmg flavor_type default q'
    score_manager._run(pending_user_input=input_, is_test=True)
    assert score_manager._transcript.entries[-4].title == 'None'

    # add flavor_type metadatum
    score_manager._session._reinitialize()
    input_ = 'lmm example~numbers mma flavor_type cherry q'
    score_manager._run(pending_user_input=input_, is_test=True)

    # maker sure flavor_type metadatum now equal to 'cherry'
    score_manager._session._reinitialize()
    input_ = 'lmm example~numbers mmg flavor_type default q'
    score_manager._run(pending_user_input=input_, is_test=True)
    assert score_manager._transcript.entries[-4].title == "'cherry'"

    # remove flavor_type metadatum
    score_manager._session._reinitialize()
    input_ = 'lmm example~numbers mmrm flavor_type default q'
    score_manager._run(pending_user_input=input_, is_test=True)

    # make sure no flavor_type metadatum found
    score_manager._session._reinitialize()
    input_ = 'lmm example~numbers mmg flavor_type default q'
    score_manager._run(pending_user_input=input_, is_test=True)
    assert score_manager._transcript.entries[-4].title == 'None'
