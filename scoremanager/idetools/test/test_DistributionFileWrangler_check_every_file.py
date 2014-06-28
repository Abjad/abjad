# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_DistributionFileWrangler_check_every_file_01():
    r'''Works in score.
    '''

    input_ = 'red~example~score d ck* y q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert 'Distribution files (2 files): OK' in contents


def test_DistributionFileWrangler_check_every_file_02():
    r'''Works in library.
    '''

    input_ = 'D ck* y q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert 'Distribution files' in contents


def test_DistributionFileWrangler_check_every_file_03():
    r'''Reports unrecognized file. Distribution files must be dash case.
    '''

    false_file = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'distribution',
        'false_file.txt',
        )

    with systemtools.FilesystemState(remove=[false_file]):
        with open(false_file, 'w') as file_pointer:
            file_pointer.write('')
        input_ = 'red~example~score d ck* y q'
        ide._run(input_=input_)
        contents = ide._transcript.contents

    assert '1 unrecognized file found:' in contents