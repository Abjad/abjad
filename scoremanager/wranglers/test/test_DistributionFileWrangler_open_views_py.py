# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_DistributionFileWrangler_open_views_py_01():

    input_ = 'd vo q'
    score_manager._run(pending_input=input_)

    assert score_manager._session._attempted_to_open_file


def test_DistributionFileWrangler_open_views_py_02():

    input_ = 'blue~example~score d vo q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents

    assert not score_manager._session._attempted_to_open_file
    assert 'No __views.py__ found.' in contents