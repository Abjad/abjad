# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_copy_file_01():

    source_path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'makers',
        'RedExampleScoreTemplate.py',
        )
    target_path = os.path.join(
        ide._configuration.makers_library,
        'ReusableScoreTemplate.py',
        )

    with systemtools.FilesystemState(keep=[source_path], remove=[target_path]):
        input_ = 'kk cp RedExampleScoreTemplate.py'
        input_ += ' My~maker~library ReusableScoreTemplate y q'
        ide._run(input_=input_)
        contents = ide._transcript.contents
        assert os.path.exists(source_path)
        assert os.path.exists(target_path)
        assert 'ReusableScoreTemplate.py' in contents


def test_MakerFileWrangler_copy_file_02():

    input_ = 'etude~example~score k cp q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    message = 'Nothing to copy.'
    assert message in contents


def test_MakerFileWrangler_copy_file_03():

    temporary_maker = os.path.join(
        ide._configuration.library,
        'makers',
        'FooBarMaker.py',
        )
    input_ = 'kk cp RedExampleScoreRhythmMaker.py'
    input_ += ' My~maker~library FooBarMaker.py y q'

    with systemtools.FilesystemState(remove=[temporary_maker]):
        assert not os.path.exists(temporary_maker)
        with open(temporary_maker, 'w') as file_pointer:
            file_pointer.write('foo bar.')
        assert os.path.isfile(temporary_maker)
        ide._run(input_=input_)
        contents = ide._transcript.contents

    assert 'Already exists:' in contents

def test_MakerFileWrangler_copy_file_04():
    r'''Raises no exception when user enters garbage for source file name.
    '''

    input_ = 'kk cp ZZZZZZ q'
    ide._run(input_=input_)