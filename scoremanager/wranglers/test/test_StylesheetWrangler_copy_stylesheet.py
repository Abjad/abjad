# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_StylesheetWrangler_copy_stylesheet_01():

    source_path = os.path.join(
        score_manager._configuration.abjad_stylesheets_directory_path,
        'clean-letter-14.ily',
        )
    target_path = os.path.join(
        score_manager._configuration.user_library_stylesheets_directory_path,
        'test-foo-stylesheet.ily',
        )

    assert os.path.exists(source_path)
    assert not os.path.exists(target_path)
    try:
        input_ = 'y cp clean-letter-14.ily'
        input_ += ' My~stylesheets test~foo~stylesheet y q'
        score_manager._run(pending_user_input=input_)
        contents = score_manager._transcript.contents
        assert os.path.exists(source_path)
        assert os.path.exists(target_path)
        assert 'test-foo-stylesheet.ily' in contents
        os.remove(target_path)
    finally:
        if os.path.exists(target_path):
            os.remove(target_path)
    assert os.path.exists(source_path)
    assert not os.path.exists(target_path)