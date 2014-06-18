# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_check_every_file_01():
    r'''Works in score.
    '''

    input_ = 'red~example~score u ck* y q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'Build files (18 files): OK' in contents


def test_BuildFileWrangler_check_every_file_02():
    r'''Works in library.
    '''

    input_ = 'U ck* y q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'Build files' in contents


def test_BuildFileWrangler_check_every_file_03():
    r'''Reports unrecognized file.
    '''

    false_file = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'build',
        'false_file.txt',
        )

    with systemtools.FilesystemState(remove=[false_file]):
        with open(false_file, 'w') as file_pointer:
            file_pointer.write('')
        input_ = 'red~example~score u ck* y q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents

    assert '1 unrecognized file found:' in contents