# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
configuration = scoremanager.idetools.Configuration()
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_DistributionFileWrangler_rename_file_01():
    r'''Works in library.
    '''

    path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'distribution',
        'red-example-score.pdf',
        )
    new_path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'distribution',
        'foo-score.pdf',
        )

    assert os.path.exists(path)

    input_ = 'dd ren red-example-score.pdf~(Red~Example~Score)'
    input_ += ' foo-score.pdf y q'
    ide._run(input_=input_)
    assert not os.path.exists(path)
    assert os.path.exists(new_path)

    # no shutil because need to rename file in repository
    input_ = 'dd ren foo-score.pdf~(Red~Example~Score)'
    input_ += ' red-example-score.pdf y q'
    ide._run(input_=input_)
    assert not os.path.exists(new_path)
    assert os.path.exists(path)


def test_DistributionFileWrangler_rename_file_02():
    r'''Works in score package.
    '''

    path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'distribution',
        'red-example-score.pdf',
        )
    new_path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'distribution',
        'foo-score.pdf',
        )

    assert os.path.exists(path)

    input_ = 'red~example~score d ren red-example-score.pdf'
    input_ += ' foo-score.pdf y q'
    ide._run(input_=input_)
    assert not os.path.exists(path)
    assert os.path.exists(new_path)

    # no shutil because need to rename file in repository
    input_ = 'red~example~score d ren foo-score.pdf'
    input_ += ' red-example-score.pdf y q'
    ide._run(input_=input_)
    assert not os.path.exists(new_path)
    assert os.path.exists(path)