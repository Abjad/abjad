# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_Menu__change_input_to_directive_01():
    r'''Works with accented characters.
    '''

    input_ = 'étude q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    string = 'Étude Example Score (2013)'
    assert string in contents


def test_Menu__change_input_to_directive_02():
    r'''Works without accented characters.
    '''

    input_ = 'etude q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    string = 'Étude Example Score (2013)'
    assert string in contents


def test_Menu__change_input_to_directive_03():
    r'''Works with mixed case.
    '''

    input_ = 'Red~example~score q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    string = 'Red Example Score (2013)'
    assert string in contents


def test_Menu__change_input_to_directive_04():
    r'''Works with mixed case.
    '''

    input_ = 'red~Example~score q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    string = 'Red Example Score (2013)'
    assert string in contents


def test_Menu__change_input_to_directive_05():
    r'''Works with mixed case.
    '''

    input_ = 'red~example~Score q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    string = 'Red Example Score (2013)'
    assert string in contents


def test_Menu__change_input_to_directive_06():
    r'''Works with mixed case.
    '''

    input_ = 'RED~EXAMPLE~SCORE q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    string = 'Red Example Score (2013)'
    assert string in contents