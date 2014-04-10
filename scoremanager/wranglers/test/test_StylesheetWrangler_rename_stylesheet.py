# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()


def test_StylesheetWrangler_rename_stylesheet_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    path = os.path.join(
        configuration.abjad_stylesheets_directory_path,
        'clean-letter-14.ily',
        )
    new_path = os.path.join(
        configuration.abjad_stylesheets_directory_path,
        'very-clean-letter-14.ily',
        )

    assert os.path.exists(path)

    input_ = 'y ren clean-letter-14.ily very-clean-letter-14.ily y q'
    score_manager._run(pending_user_input=input_)
    assert not os.path.exists(path)
    assert os.path.exists(new_path)

    input_ = 'y ren very-clean-letter-14.ily clean-letter-14.ily y q'
    score_manager._run(pending_user_input=input_)
    assert not os.path.exists(new_path)
    assert os.path.exists(path)