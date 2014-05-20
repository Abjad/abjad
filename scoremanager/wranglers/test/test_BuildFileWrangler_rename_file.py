# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_BuildFileWrangler_rename_file_01():
    r'''Works in library.
    '''

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'build',
        'score.pdf',
        )
    new_path = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'build',
        'foo-score.pdf',
        )

    assert os.path.exists(path)

    input_ = 'u ren score.pdf~(Red~Example~Score)'
    input_ += ' foo-score.pdf y q'
    score_manager._run(pending_input=input_)
    assert not os.path.exists(path)
    assert os.path.exists(new_path)

    # no shutil because need to rename file in repository
    input_ = 'u ren foo-score.pdf~(Red~Example~Score)'
    input_ += ' score.pdf y q'
    score_manager._run(pending_input=input_)
    assert not os.path.exists(new_path)
    assert os.path.exists(path)


def test_BuildFileWrangler_rename_file_02():
    r'''Works in score package.
    '''

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'build',
        'score.pdf',
        )
    new_path = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'build',
        'foo-score.pdf',
        )

    assert os.path.exists(path)

    input_ = 'red~example~score u ren score.pdf'
    input_ += ' foo-score.pdf y q'
    score_manager._run(pending_input=input_)
    assert not os.path.exists(path)
    assert os.path.exists(new_path)

    # no shutil because need to rename file in repository
    input_ = 'red~example~score u ren foo-score.pdf'
    input_ += ' score.pdf y q'
    score_manager._run(pending_input=input_)
    assert not os.path.exists(new_path)
    assert os.path.exists(path)