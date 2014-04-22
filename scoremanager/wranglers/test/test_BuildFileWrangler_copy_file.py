# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_BuildFileWrangler_copy_file_01():
    r'''In library: partial test because we can't be sure any user 
    score packages will be present. And because Score Manager allows copying 
    into user score packges only (because copying into example score packages
    could pollute the example score packages).
    '''

    input_ = 'u cp score.pdf q'
    score_manager._run(pending_user_input=input_)

    titles = [
        'Score manager - example scores',
        'Score manager - build file library',
        '',
        'Score manager - build file library - select storehouse:',
        ]
    assert score_manager._transcript.titles == titles


def test_BuildFileWrangler_copy_file_02():
    r'''In single build directory.
    '''

    source_path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'build',
        'score.pdf',
        )
    target_path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'build',
        'copied-score.pdf',
        )

    assert os.path.exists(source_path)
    assert not os.path.exists(target_path)
    try:
        input_ = 'red~example~score u cp'
        input_ += ' score.pdf copied-score.pdf y q'
        score_manager._run(pending_user_input=input_)
        contents = score_manager._transcript.contents
        assert os.path.exists(source_path)
        assert os.path.exists(target_path)
        assert 'copied-score.pdf' in contents
        os.remove(target_path)
    finally:
        if os.path.exists(target_path):
            os.remove(target_path)
    assert os.path.exists(source_path)
    assert not os.path.exists(target_path)