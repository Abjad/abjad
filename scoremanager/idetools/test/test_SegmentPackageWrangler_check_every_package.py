# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_check_every_package_01():
    r'''Works in score.
    '''

    lines = [
        'Segments (3 packages)',
        'A: OK',
        'B: OK',
        'C: OK',
        ]

    input_ = 'red~example~score g ck* y n q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents
    for line in lines:
        assert line in contents


def test_SegmentPackageWrangler_check_every_package_02():
    r'''Works in library.
    '''

    lines = [
        'A (Red Example Score): OK',
        'B (Red Example Score): OK',
        'C (Red Example Score): OK',
        ]

    input_ = 'g ck* y n q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents
    for line in lines:
        assert line in contents


def test_SegmentPackageWrangler_check_every_package_03():
    r'''Supplies missing directory and missing file.
    '''

    segment_directory = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'segments',
        'segment_01',
        )
    versions_directory = os.path.join(segment_directory, 'versions')
    initializer = os.path.join(segment_directory, '__init__.py')
        
    with systemtools.FilesystemState(keep=[versions_directory, initializer]):
        os.remove(initializer)
        shutil.rmtree(versions_directory)
        input_ = 'red~example~score g ck* y y q'
        score_manager._run(input_=input_)
        assert os.path.isfile(initializer)
        assert os.path.isdir(versions_directory)