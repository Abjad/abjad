# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
configuration = scoremanager.idetools.Configuration()
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_rename_file_01():
    r'''Works in library.
    '''

    path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'makers',
        'RedExampleScoreTemplate.py',
        )
    new_path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'makers',
        'FooRedExampleScoreTemplate.py',
        )

    assert os.path.exists(path)

    input_ = 'kk ren RedExampleScoreTemplate.py~(Red~Example~Score)'
    input_ += ' FooRedExampleScoreTemplate.py y q'
    ide._run(input_=input_)
    assert not os.path.exists(path)
    assert os.path.exists(new_path)

    # no shutil because need to rename file in repository
    input_ = 'kk ren FooRedExampleScoreTemplate.py~(Red~Example~Score)'
    input_ += ' RedExampleScoreTemplate.py y q'
    ide._run(input_=input_)
    assert not os.path.exists(new_path)
    assert os.path.exists(path)


def test_MakerFileWrangler_rename_file_02():
    r'''Works in score package.
    '''

    path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'makers',
        'RedExampleScoreTemplate.py',
        )
    new_path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'makers',
        'FooRedExampleScoreTemplate.py',
        )

    assert os.path.exists(path)

    input_ = 'red~example~score k ren RedExampleScoreTemplate.py'
    input_ += ' FooRedExampleScoreTemplate.py y q'
    ide._run(input_=input_)
    assert not os.path.exists(path)
    assert os.path.exists(new_path)

    # no shutil because need to rename file in repository
    input_ = 'red~example~score k ren FooRedExampleScoreTemplate.py'
    input_ += ' RedExampleScoreTemplate.py y q'
    ide._run(input_=input_)
    assert not os.path.exists(new_path)
    assert os.path.exists(path)