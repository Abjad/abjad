# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager
pytest.skip('unskip me after making decision about cache.')


def test_ScorePackageManager_interactively_edit_title_01():

    try:
        score_manager = scoremanager.core.ScoreManager()
        string = 'green~example~score score~setup title Foo q'
        score_manager._run(pending_user_input=string)
        assert score_manager.session.io_transcript.signature == (9,)
        string = 'Green Example Score (2013) - setup'
        assert score_manager.session.io_transcript[-5][1][0] == string
        string = 'Foo (2013) - setup'
        assert score_manager.session.io_transcript[-2][1][0] == string
    finally:
        string = 'foo score~setup title Green~Example~Score q'
        score_manager._run(pending_user_input=string)
        assert score_manager.session.io_transcript.signature == (9,)
        string = 'Foo (2013) - setup'
        assert score_manager.session.io_transcript[-5][1][0] == string
        string = 'Green Example Score (2013) - setup'
        assert score_manager.session.io_transcript[-2][1][0] == string
