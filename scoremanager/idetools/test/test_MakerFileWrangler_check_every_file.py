# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_check_every_file_01():
    r'''Works in score.
    '''

    input_ = 'red~example~score k ck* y q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'Maker files (2 files): OK' in contents


def test_MakerFileWrangler_check_every_file_02():
    r'''Works in library.
    '''

    input_ = 'k ck* y q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'Maker files' in contents


def test_MakerFileWrangler_check_every_file_03():
    r'''Reports unrecognized file. Maker files must be upper camel case.
    '''

    false_file = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'makers',
        'false-maker.py',
        )

    with systemtools.FilesystemState(remove=[false_file]):
        with open(false_file, 'w') as file_pointer:
            file_pointer.write('')
        input_ = 'red~example~score k ck* y q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents

    assert '1 unrecognized file found:' in contents