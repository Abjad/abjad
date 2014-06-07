# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_make_package_01():
    r'''Makes score package.
    '''

    path = os.path.join(
        score_manager._configuration.user_score_packages_directory,
        'example_score',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'build',
        'distribution',
        'makers',
        'materials',
        'segments',
        'stylesheets',
        ]

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'new example~score y q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        assert os.path.exists(path)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.ScorePackageManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries

    assert 'Enter score package name>' in contents


def test_ScorePackageWrangler_make_package_02():
    r'''Makes score package. Clears view after package is made.
    Must set is_test=False to work with views.
    '''

    score_manager = scoremanager.core.AbjadIDE(is_test=False)
    score_package = os.path.join(
        score_manager._configuration.user_score_packages_directory,
        'example_score',
        )
    cache = score_manager._configuration.cache_file_path
    views_file = os.path.join(
        score_manager._configuration.wrangler_views_directory,
        '__ScorePackageWrangler_views__.py',
        )
    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - scores - views - _test_view (EDIT)',
        'Abjad IDE - scores',
        'Abjad IDE - scores (_test_view)',
        '(untitled score)',
        ]
    
    with systemtools.FilesystemState(
        keep=[cache, views_file], remove=[score_package]
        ):
        input_ = 'vnew _test_view done vap _test_view new example~score y q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        assert os.path.exists(score_package)

    assert score_manager._transcript.titles == titles


def test_ScorePackageWrangler_make_package_03():
    r'''Accepts flexible package name input.
    '''

    score_package = os.path.join(
        score_manager._configuration.user_score_packages_directory,
        'example_score_1',
        )

    with systemtools.FilesystemState(remove=[score_package]):
        input_ = 'new ExampleScore1 y q'
        score_manager._run(input_=input_)
        assert os.path.exists(score_package)

    with systemtools.FilesystemState(remove=[score_package]):
        input_ = 'new exampleScore1 y q'
        score_manager._run(input_=input_)
        assert os.path.exists(score_package)

    with systemtools.FilesystemState(remove=[score_package]):
        input_ = 'new EXAMPLE_SCORE_1 y q'
        score_manager._run(input_=input_)
        assert os.path.exists(score_package)

    with systemtools.FilesystemState(remove=[score_package]):
        input_ = 'new example_score_1 y q'
        score_manager._run(input_=input_)
        assert os.path.exists(score_package)