# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_ScorePackageManager_check_package_01():
    r'''Reports problems only.
    '''

    input_ = 'red~example~score ck y q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    lines = [
        'Build directory (18 files): OK',
        'Distribution directory (2 files): OK',
        'Makers directory (2 files): OK',
        'Materials directory (5 packages):',
        'Segments directory (3 packages):',
        'Stylesheets directory (3 files): OK',
        ]
    for line in lines:
        assert line in contents
    assert 'found' not in contents


def test_ScorePackageManager_check_package_02():
    r'''Reports everything.
    '''

    input_ = 'red~example~score ck n q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    lines = [
        '6 of 6 required directories found:',
        '2 of 2 required files found:',
        '1 optional directory found:',
        ]
    for line in lines:
        assert line in contents


def test_ScorePackageManager_check_package_03():
    r'''Reports unrecognized file.
    '''

    extra_file = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'extra_file.txt',
        )

    with systemtools.FilesystemState(remove=[extra_file]):
        with open(extra_file, 'w') as file_pointer:
            file_pointer.write('')
        input_ = 'red~example~score ck y q'
        ide._run(input_=input_)
        contents = ide._transcript.contents

    line = '1 unrecognized file found:'
    assert line in contents


def test_ScorePackageManager_check_package_04():
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
        input_ = 'red~example~score ck y y q'
        ide._run(input_=input_)
        assert os.path.isfile(initializer)
        assert os.path.isdir(build_directory)


def test_ScorePackageManager_check_package_05():
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
        input_ = 'red~example~score ck y y q'
        ide._run(input_=input_)
        assert os.path.isfile(initializer)
        assert os.path.isdir(versions_directory)