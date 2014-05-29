# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScorePackageManager__handle_numeric_user_input_01():

    input_ = 'red~example~score __init__.py q'
    score_manager._run(input_=input_)

    assert score_manager._session._attempted_to_open_file


def test_ScorePackageManager__handle_numeric_user_input_02():

    input_ = 'red~example~score segments q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    strings = [
        '__init__.py',
        '__metadata__.py',
        '__views__.py',
        'segment_01',
        'segment_02',
        'segment_03',
        ]

    for string in strings:
        assert string in contents