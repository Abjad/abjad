# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_BuildFileWrangler_generate_preface_source_01():
    r'''Works when preface source doesn't yet exist.

    Supplies papersize={8.5in, 11in} as a default.
    '''

    source_path = os.path.join(
        score_manager._configuration.score_manager_directory_path,
        'boilerplate',
        'preface.tex',
        )
    destination_path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'blue_example_score',
        'build',
        'preface.tex',
        )

    source_contents = ''.join(file(source_path).readlines())
    assert 'PAPER_SIZE' in source_contents
    assert '{8.5in, 11in}' not in source_contents

    with systemtools.FilesystemState(
        keep=[source_path], remove=[destination_path]):
        input_ = 'blue~example~score u pg q'
        score_manager._run(pending_input=input_)
        assert os.path.isfile(destination_path)
        destination_contents = ''.join(file(destination_path).readlines())
        assert 'PAPER_SIZE' not in destination_contents
        assert '{8.5in, 11in}' in destination_contents
        contents = score_manager._transcript.contents
        assert 'Overwrite' not in contents
        assert 'Overwrote' not in contents


def test_BuildFileWrangler_generate_preface_source_02():
    r'''Works when preface source already exists.
    '''

    source_path = os.path.join(
        score_manager._configuration.score_manager_directory_path,
        'boilerplate',
        'preface.tex',
        )
    destination_path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'build',
        'preface.tex',
        )

    source_contents = ''.join(file(source_path).readlines())
    assert 'PAPER_SIZE' in source_contents
    assert '{8.5in, 11in}' not in source_contents

    with systemtools.FilesystemState(keep=[source_path, destination_path]):
        input_ = 'red~example~score u pg y q'
        score_manager._run(pending_input=input_)
        assert os.path.isfile(destination_path)
        destination_contents = ''.join(file(destination_path).readlines())
        assert 'PAPER_SIZE' not in destination_contents
        assert '{8.5in, 11in}' in destination_contents
        contents = score_manager._transcript.contents
        assert 'Overwrite' in contents
        assert 'Overwrote' in contents