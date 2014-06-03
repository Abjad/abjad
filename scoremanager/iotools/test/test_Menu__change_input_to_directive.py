# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.AbjadIDE(is_test=True)


def test_Menu__change_input_to_directive_01():
    r'''Works with accented characters.
    '''

    input_ = 'étude q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    string = 'Étude Example Score (2013)'
    assert string in contents


def test_Menu__change_input_to_directive_02():
    r'''Works without accented characters.
    '''

    input_ = 'etude q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    string = 'Étude Example Score (2013)'
    assert string in contents


def test_Menu__change_input_to_directive_03():
    r'''Works with mixed case.
    '''

    input_ = 'Red~example~score q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    string = 'Red Example Score (2013)'
    assert string in contents


def test_Menu__change_input_to_directive_04():
    r'''Works with mixed case.
    '''

    input_ = 'red~Example~score q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    string = 'Red Example Score (2013)'
    assert string in contents


def test_Menu__change_input_to_directive_05():
    r'''Works with mixed case.
    '''

    input_ = 'red~example~Score q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    string = 'Red Example Score (2013)'
    assert string in contents


def test_Menu__change_input_to_directive_06():
    r'''Works with mixed case.
    '''

    input_ = 'RED~EXAMPLE~SCORE q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    string = 'Red Example Score (2013)'
    assert string in contents