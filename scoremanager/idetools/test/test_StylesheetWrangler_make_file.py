# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_make_file_01():

    path = os.path.join(
        score_manager._configuration.user_library_stylesheets_directory,
        'test-stylesheet.ily',
        )

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'Y new My~stylesheets test-stylesheet q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        assert os.path.exists(path)

    assert 'Select storehouse:' in contents


def test_StylesheetWrangler_make_file_02():
    r'''Makes sure that file name 'new-*.ily' doesn't alias command (new).
    '''

    path_1 = os.path.join(
        score_manager._configuration.user_library_stylesheets_directory,
        'new-test-stylesheet-1.ily',
        )
    path_2 = os.path.join(
        score_manager._configuration.user_library_stylesheets_directory,
        'new-test-stylesheet-2.ily',
        )

    with systemtools.FilesystemState(remove=[path_1, path_2]):
        input_ = 'Y new My~stylesheets new-test-stylesheet-1 q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        assert os.path.exists(path_1)
        input_ = 'Y new My~stylesheets new-test-stylesheet-2 q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        assert os.path.exists(path_2)
        input_ = 'Y new-test-stylesheet-1.ily q'
        score_manager._run(input_=input_)
        assert score_manager._session._attempted_to_open_file