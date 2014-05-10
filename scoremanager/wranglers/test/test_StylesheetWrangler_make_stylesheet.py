# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_StylesheetWrangler_make_stylesheet_01():

    path = os.path.join(
        score_manager._configuration.user_library_stylesheets_directory_path,
        'test-stylesheet.ily',
        )

    with systemtools.AssetState(remove=[path]):
        input_ = 'y new 1 test-stylesheet q'
        score_manager._run(pending_input=input_)
        assert os.path.exists(path)