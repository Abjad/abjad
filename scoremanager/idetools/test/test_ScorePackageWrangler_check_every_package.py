# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_check_every_package_01():

    lines = [
        'Étude Example Score (2013):',
        '    Top level (9 assets): OK',
        '    Build directory (1 files): OK',
        '    Distribution directory (0 files): OK',
        '    Makers directory (0 files): OK',
        '    Materials directory (0 packages): OK',
        '    Segments directory (0 packages): OK',
        '    Stylesheets directory (0 files): OK',
        'Red Example Score (2013):',
        '    Top level (9 assets): OK',
        '    Build directory (18 files): OK',
        '    Distribution directory (2 files): OK',
        '    Makers directory (2 files): OK',
        '    Materials directory (5 packages):',
        '        Magic numbers: OK',
        '        Performer inventory: OK',
        '        Pitch range inventory: OK',
        '        Tempo inventory: OK',
        '        Time signatures: OK',
        '    Segments directory (3 packages):',
        '        A: OK',
        '        B: OK',
        '        C: OK',
        '    Stylesheets directory (3 files): OK',
        ]

    input_ = 'ck* y n q'
    ide._run(input_=input_)
    contents = ide._transcript.contents
    for line in lines:
        assert line in contents


def test_ScorePackageWrangler_check_every_package_02():
    r'''Supplies missing directory and missing file in immediate package.
    '''

    score_directory = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        )
    build_directory = os.path.join(score_directory, 'build')
    initializer = os.path.join(score_directory, '__init__.py')
        
    with systemtools.FilesystemState(keep=[build_directory, initializer]):
        os.remove(initializer)
        shutil.rmtree(build_directory)
        input_ = 'ck* y y q'
        ide._run(input_=input_)
        assert os.path.isfile(initializer)
        assert os.path.isdir(build_directory)


def test_ScorePackageWrangler_check_every_package_03():
    r'''Supplies missing directory and missing file in nested package.
    '''

    segment_directory = os.path.join(
        ide._configuration.example_score_packages_directory,
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
        ide._run(input_=input_)
        assert os.path.isfile(initializer)
        assert os.path.isdir(versions_directory)