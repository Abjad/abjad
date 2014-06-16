# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Menu__display_available_commands_01():

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = '?? q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'system - available commands' in contents
    assert 'scores - new' in contents


def test_Menu__display_available_commands_02():
    r'''Hidden menu persists after junk.
    '''

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = '?? asdf q'
    score_manager._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - scores - available commands',
        ]
    assert score_manager._transcript.titles == titles


def test_Menu__display_available_commands_03():
    r'''Hidden menu persists after 'LilyPond log view.
    '''

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = '?? log q'
    score_manager._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - scores - available commands',
        ]
    assert score_manager._transcript.titles == titles


def test_Menu__display_available_commands_04():
    r'''Hidden menu is available when managing score package.
    '''

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score ?? q'
    score_manager._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - available commands',
        ]
    assert score_manager._transcript.titles == titles