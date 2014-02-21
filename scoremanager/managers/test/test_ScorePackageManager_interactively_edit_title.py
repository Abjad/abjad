# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager
pytest.skip('unskip me after making decision about cache.')


def test_ScorePackageManager_interactively_edit_title_01():

    try:
        score_manager = scoremanager.core.ScoreManager()
        string = 'green~example~score setup title Foo q'
        score_manager._run(pending_user_input=string)
        assert score_manager._session.transcript.signature == (9,)
        string = 'Green Example Score (2013) - setup'
        assert score_manager._session.transcript[-5].title == string
        string = 'Foo (2013) - setup'
        assert score_manager._session.transcript.last_menu_title == string
    finally:
        string = 'foo setup title Green~Example~Score q'
        score_manager._run(pending_user_input=string)
        assert score_manager._session.transcript.signature == (9,)
        string = 'Foo (2013) - setup'
        assert score_manager._session.transcript[-5].title == string
        string = 'Green Example Score (2013) - setup'
        assert score_manager._session.transcript.last_menu_title == string
