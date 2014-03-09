# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager
pytest.skip('unskip me after making decision about cache.')


def test_ScorePackageManager_edit_title_01():

    try:
        score_manager = scoremanager.core.ScoreManager()
        input_ = 'green~example~score setup title Foo q'
        score_manager._run(pending_user_input=input_, is_test=True)
        assert score_manager._transcript.signature == (9,)
        string = 'Green Example Score (2013) - setup'
        assert score_manager._transcript[-5].title == string
        string = 'Foo (2013) - setup'
        assert score_manager._transcript.last_title == string
    finally:
        input_ = 'foo setup title Green~Example~Score q'
        score_manager._run(pending_user_input=input_, is_test=True)
        assert score_manager._transcript.signature == (9,)
        string = 'Foo (2013) - setup'
        assert score_manager._transcript[-5].title == string
        string = 'Green Example Score (2013) - setup'
        assert score_manager._transcript.last_title == string
