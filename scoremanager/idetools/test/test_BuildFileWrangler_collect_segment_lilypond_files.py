# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_collect_segment_lilypond_files_01():
    r'''Copies LilyPond files from segment packages to build directory
    when build directory contains no segment LilyPond files.
    '''

    build_directory = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'build',
        )

    segment_names, segment_paths = [], []
    for number in ('01', '02', '03'):
        segment_name = 'segment-{}.ly'
        segment_name = segment_name.format(number)
        segment_names.append(segment_name)
        segment_path = os.path.join(build_directory, segment_name)
        segment_paths.append(segment_path)

    with systemtools.FilesystemState(keep=segment_paths):
        for segment_path in segment_paths:
            os.remove(segment_path)
        input_ = 'red~example~score u mc y q'
        ide._run(input_=input_)
        for segment_path in segment_paths:
            assert os.path.isfile(segment_path)

    contents = ide._transcript.contents
    assert 'Will copy ...' in contents
    assert 'FROM:' in contents
    assert 'TO:' in contents


def test_BuildFileWrangler_collect_segment_lilypond_files_02():
    r'''Preseves build directory segment LilyPond files when segment package
    LilyPond files compare equal to build directory segment LilyPond files.
    '''

    build_directory = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'build',
        )

    segment_names, segment_paths = [], []
    for number in ('01', '02', '03'):
        segment_name = 'segment-{}.ly'
        segment_name = segment_name.format(number)
        segment_names.append(segment_name)
        segment_path = os.path.join(build_directory, segment_name)
        segment_paths.append(segment_path)

    with systemtools.FilesystemState(keep=segment_paths):
        input_ = 'red~example~score u mc y q'
        ide._run(input_=input_)

    contents = ide._transcript.contents
    assert 'Will copy ...' in contents
    assert 'FROM:' in contents
    assert 'TO:' in contents
    assert 'The files ...' in contents
    assert '... compare the same.' in contents
    assert 'Preserved' in contents