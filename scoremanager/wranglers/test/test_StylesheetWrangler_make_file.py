# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_StylesheetWrangler_make_file_01():

    path = os.path.join(
        score_manager._configuration.user_library_stylesheets_directory,
        'test-stylesheet.ily',
        )

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'y new My~stylesheets test-stylesheet q'
        score_manager._run(input_=input_)
        assert os.path.exists(path)