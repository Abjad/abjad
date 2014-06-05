# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_check_every_package_01():

    lines = [
        'Étude Example Score (2013):',
        '    Top level (9 assets): OK',
        '    Build files (1 files): OK',
        '    Distribution files (0 files): OK',
        '    Maker files (0 files): OK',
        '    Materials (0 packages): OK',
        '    Segments (0 packages): OK',
        '    Stylesheets (0 files): OK',
        'Red Example Score (2013):',
        '    Top level (9 assets): OK',
        '    Build files (18 files): OK',
        '    Distribution files (2 files): OK',
        '    Maker files (2 files): OK',
        '    Materials (5 packages):',
        '        Instrumentation: OK',
        '        Magic numbers: OK',
        '        Pitch range inventory: OK',
        '        Tempo inventory: OK',
        '        Time signatures: OK',
        '    Segments (3 packages):',
        '        A: OK',
        '        B: OK',
        '        C: OK',
        '    Stylesheets (2 files): OK',
        ]

    input_ = 'ck* y n q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents
    for line in lines:
        assert line in contents


def test_ScorePackageWrangler_check_every_package_02():
    r'''Supplies missing directory and missing file in immediate package.
    '''

    score_directory = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        )
    build_directory = os.path.join(score_directory, 'build')
    initializer = os.path.join(score_directory, '__init__.py')
        
    with systemtools.FilesystemState(keep=[build_directory, initializer]):
        os.remove(initializer)
        shutil.rmtree(build_directory)
        input_ = 'ck* y y q'
        score_manager._run(input_=input_)
        assert os.path.isfile(initializer)
        assert os.path.isdir(build_directory)


def test_ScorePackageWrangler_check_every_package_03():
    r'''Supplies missing directory and missing file in nested package.
    '''

    segment_directory = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'segments',
        'segment_02',
        )
    versions_directory = os.path.join(segment_directory, 'versions')
    initializer = os.path.join(segment_directory, '__init__.py')
        
    with systemtools.FilesystemState(keep=[versions_directory, initializer]):
        os.remove(initializer)
        shutil.rmtree(versions_directory)
        input_ = 'ck* y y q'
        score_manager._run(input_=input_)
        assert os.path.isfile(initializer)
        assert os.path.isdir(versions_directory)