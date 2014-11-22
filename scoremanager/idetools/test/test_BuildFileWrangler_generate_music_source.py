# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_generate_music_source_01():
    r'''Works when music.ly source doesn't yet exist.

    (Can't use filecmp because music.ly file contains LilyPond version
    directive, LilyPond language directive and file paths all dependent
    on user environment.)
    '''

    music_path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'build',
        'music.ly',
        )

    with systemtools.FilesystemState(keep=[music_path]):
        os.remove(music_path)
        input_ = 'red~example~score u mg y y q'
        ide._run(input_=input_)
        assert os.path.isfile(music_path)
        with open(music_path, 'r') as file_pointer:
            file_lines = file_pointer.readlines()
            file_contents = ''.join(file_lines)
        assert 'Red Example Score (2013) for piano' in file_contents
        assert r'\language' in file_contents
        assert r'\version' in file_contents
        #assert r'\context Score = "Red Example Score"' in file_contents


def test_BuildFileWrangler_generate_music_source_02():
    r'''Works when music.ly already exists.
    '''

    music_path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'build',
        'music.ly',
        )

    with systemtools.FilesystemState(keep=[music_path]):
        input_ = 'red~example~score u mg y y q'
        ide._run(input_=input_)

    contents = ide._transcript.contents
    assert 'The files ...' in contents
    assert '... compare the same.' in contents
    assert 'Preserved' in contents