# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_check_every_file_01():
    r'''Works in build directory.
    '''

    input_ = 'red~example~score u ck* y q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert 'Build directory (18 files): OK' in contents


def test_BuildFileWrangler_check_every_file_02():
    r'''Works in build depot.
    '''

    input_ = 'uu ck* q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert 'Build depot' in contents


def test_BuildFileWrangler_check_every_file_03():
    r'''Reports unrecognized file.
    '''

    false_file = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'build',
        'false_file.txt',
        )

    with systemtools.FilesystemState(remove=[false_file]):
        with open(false_file, 'w') as file_pointer:
            file_pointer.write('')
        input_ = 'red~example~score u ck* y q'
        ide._run(input_=input_)
        contents = ide._transcript.contents

    assert '1 unrecognized file found:' in contents