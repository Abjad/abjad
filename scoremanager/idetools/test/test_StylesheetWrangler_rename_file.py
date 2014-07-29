# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
configuration = scoremanager.idetools.Configuration()
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_rename_file_01():
    r'''Works in library.
    '''

    path = os.path.join(
        configuration.example_stylesheets_directory,
        'clean-letter-14.ily',
        )
    new_path = os.path.join(
        configuration.example_stylesheets_directory,
        'very-clean-letter-14.ily',
        )

    assert os.path.exists(path)

    input_ = 'yy ren clean-letter-14.ily very-clean-letter-14.ily y q'
    ide._run(input_=input_)
    assert not os.path.exists(path)
    assert os.path.exists(new_path)

    # no shutil because need to rename file in repository
    input_ = 'yy ren very-clean-letter-14.ily clean-letter-14.ily y q'
    ide._run(input_=input_)
    assert not os.path.exists(new_path)
    assert os.path.exists(path)


def test_StylesheetWrangler_rename_file_02():
    r'''Works in library.
    '''

    path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'stylesheets',
        'stylesheet.ily',
        )
    new_path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'stylesheets',
        'foo-stylesheet.ily',
        )

    assert os.path.exists(path)

    input_ = 'red~example~score y ren stylesheet.ily foo-stylesheet.ily y q'
    ide._run(input_=input_)
    assert not os.path.exists(path)
    assert os.path.exists(new_path)

    # no shutil because need to rename file in repository
    input_ = 'yy ren foo-stylesheet.ily stylesheet.ily y q'
    ide._run(input_=input_)
    assert not os.path.exists(new_path)
    assert os.path.exists(path)