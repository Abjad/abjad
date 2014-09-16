# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_Autoeditor__run_01():
    r'''Lone bang doesn't blow up autoeditor.
    '''

    ide = scoremanager.idetools.AbjadIDE(is_test=True)
    ide._session._allow_unknown_command_during_test = True
    input_ = 'red~example~score m tempo~inventory da ! q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert "Unknown command: '!'." in contents


def test_Autoeditor__run_02():
    r'''Double bang doesn't blow up autoeditor.
    '''

    ide = scoremanager.idetools.AbjadIDE(is_test=True)
    ide._session._allow_unknown_command_during_test = True
    input_ = 'red~example~score m tempo~inventory da !! q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert "Unknown command: '!!'." in contents


def test_Autoeditor__run_03():
    r'''Lone question mark doesn't blow up autoeditor.
    '''

    ide = scoremanager.idetools.AbjadIDE(is_test=True)
    ide._session._allow_unknown_command_during_test = True
    input_ = 'red~example~score m tempo~inventory da ? q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert "Unknown command: '?'." in contents


def test_Autoeditor__run_04():
    r'''Double question mark doesn't blow up autoeditor.
    '''

    ide = scoremanager.idetools.AbjadIDE(is_test=True)
    ide._session._allow_unknown_command_during_test = True
    input_ = 'red~example~score m tempo~inventory da ?? q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert "Unknown command: '??'." in contents


def test_Autoeditor__run_05():
    r'''Bang-suffixed done doesn't blow up autoeditor.
    '''

    ide = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score m tempo~inventory da done! q'
    ide._run(input_=input_)


def test_Autoeditor__run_06():
    r'''The (EDIT+) label shows up after target has been modified.
    '''

    ide = scoremanager.idetools.AbjadIDE(is_test=True)

    definition_py = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'tempo_inventory',
        'definition.py',
        )

    with systemtools.FilesystemState(keep=[definition_py]):
        input_ = 'red~example~score m tempo~inventory da add ((1, 8), 136) q'
        ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials directory',
        'Red Example Score (2013) - materials directory - tempo inventory',
        'Red Example Score (2013) - materials directory - tempo inventory (EDIT)',
        'Red Example Score (2013) - materials directory - tempo inventory (EDIT+)',
        ]

    assert ide._transcript.titles == titles