# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_open_views_py_01():

    input_ = 'U vo q'
    score_manager._run(input_=input_)

    assert score_manager._session._attempted_to_open_file


def test_BuildFileWrangler_open_views_py_02():

    input_ = 'blue~example~score u vo q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert not score_manager._session._attempted_to_open_file
    assert 'No __views.py__ found.' in contents