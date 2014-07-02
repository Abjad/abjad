# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageManager_check_package_01():
    r'''Reports problems only.
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
        input_ = 'red~example~score g B ck y n q'
        ide._run(input_=input_)
        contents = ide._transcript.contents

    lines = [
        '1 of 1 required directory missing:',
        '1 of 3 required files missing:',
        ]
    for line in lines:
        assert line in contents
    assert 'optional directories' not in contents
    assert 'optional files' not in contents


def test_SegmentPackageManager_check_package_02():
    r'''Reports everything.
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
        input_ = 'red~example~score g B ck n n q'
        ide._run(input_=input_)
        contents = ide._transcript.contents

    lines = [
        '1 of 1 required directory missing:',
        '1 of 3 required files missing:',
        '2 optional files found:',
        ]
    for line in lines:
        assert line in contents


def test_SegmentPackageManager_check_package_03():
    r'''Supplies missing directory and missing file.
    '''

    segment_directory = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'segments',
        'segment_01',
        )
    versions_directory = os.path.join(segment_directory, 'versions')
    initializer = os.path.join(segment_directory, '__init__.py')
        
    with systemtools.FilesystemState(keep=[versions_directory, initializer]):
        os.remove(initializer)
        shutil.rmtree(versions_directory)
        input_ = 'red~example~score g A ck y y q'
        ide._run(input_=input_)
        assert os.path.isfile(initializer)
        assert os.path.isdir(versions_directory)