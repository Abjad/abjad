# -*- encoding: utf-8 -*-
import pytest
pytest.skip('make me work')
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageWrangler_copy_package_01():
    r'''Works in library.
    
    Partial test because we can't be sure any user score packages will be
    present. And because Score Manager allows copying into user score packges
    only (because copying into example score packages could pollute the example
    score packages).
    '''

    input_ = 'g cp segment~01~(Red~Example~Score) q'
    score_manager._run(pending_user_input=input_)

    titles = [
        'Score manager - example scores',
        'Score manager - materials',
        '',
        'Score manager - materials - select storehouse:',
        ]
    assert score_manager._transcript.titles == titles


def test_SegmentPackageWrangler_copy_package_02():
    r'''Works in score.
    '''

    source_path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'materials',
        'instrumentation',
        )
    target_path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'materials',
        'copied_instrumentation',
        )

    assert os.path.exists(source_path)
    assert not os.path.exists(target_path)
    try:
        input_ = 'red~example~score m cp'
        input_ += ' instrumentation copied_instrumentation y q'
        score_manager._run(pending_user_input=input_)
        contents = score_manager._transcript.contents
        assert os.path.exists(source_path)
        assert os.path.exists(target_path)
        assert 'copied_instrumentation' in contents
        shutil.rmtree(target_path)
    finally:
        if os.path.exists(target_path):
            shutil.rmtree(target_path)
    assert os.path.exists(source_path)
    assert not os.path.exists(target_path)