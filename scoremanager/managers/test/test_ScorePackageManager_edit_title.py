# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScorePackageManager_edit_title_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'étude~example~score setup title Foo q'
    score_manager._run(pending_user_input=input_)
    string = 'Étude Example Score (2013) - setup'
    assert score_manager._transcript[-5].title == string
    string = 'Foo (2013) - setup'
    assert score_manager._transcript.last_title == string

    input_ = 'foo setup title Étude~Example~Score q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (9,)
    string = 'Foo (2013) - setup'
    assert score_manager._transcript[-5].title == string
    string = 'Étude Example Score (2013) - setup'
    assert score_manager._transcript.last_title == string
