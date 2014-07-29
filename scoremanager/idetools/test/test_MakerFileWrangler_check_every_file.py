# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_check_every_file_01():
    r'''Works in makers directory.
    '''

    input_ = 'red~example~score k ck* y q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert 'Makers directory (2 files): OK' in contents


def test_MakerFileWrangler_check_every_file_02():
    r'''Works in makers depot.
    '''

    input_ = 'kk ck* q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert 'Makers depot' in contents


def test_MakerFileWrangler_check_every_file_03():
    r'''Reports unrecognized file. Maker files must be upper camel case.
    '''

    false_file = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'makers',
        'false-maker.py',
        )

    with systemtools.FilesystemState(remove=[false_file]):
        with open(false_file, 'w') as file_pointer:
            file_pointer.write('')
        input_ = 'red~example~score k ck* y q'
        ide._run(input_=input_)
        contents = ide._transcript.contents

    assert '1 unrecognized file found:' in contents