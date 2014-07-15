# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Menu__display_available_commands_01():

    ide = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = '?? q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert 'system - commands' in contents
    assert 'scores - new' in contents


def test_Menu__display_available_commands_02():
    r'''Hidden menu persists after junk.
    '''

    ide = scoremanager.idetools.AbjadIDE(is_test=True)
    ide._session._allow_unknown_command_during_test = True
    input_ = '?? asdf q'
    ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - scores - available commands',
        ]
    assert ide._transcript.titles == titles


def test_Menu__display_available_commands_03():
    r'''Hidden menu persists after LilyPond log.
    '''

    ide = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = '?? ll q'
    ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - scores - available commands',
        ]
    assert ide._transcript.titles == titles


def test_Menu__display_available_commands_04():
    r'''Hidden menu is available when managing score package.
    '''

    ide = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score ?? q'
    ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - available commands',
        ]
    assert ide._transcript.titles == titles