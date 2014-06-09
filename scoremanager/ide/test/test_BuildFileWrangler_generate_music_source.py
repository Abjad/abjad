# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.ide.AbjadIDE(is_test=True)


def test_BuildFileWrangler_generate_music_source_01():
    r'''Works when music.ly source already exists.

    (Can't use filecmp because music.ly file contains LilyPond version
    directive, LilyPond language directive and file paths all dependent
    on user environment.)
    '''

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'build',
        'music.ly',
        )

    with systemtools.FilesystemState(keep=[path]):
        input_ = 'red~example~score u mg y y q'
        score_manager._run(input_=input_)
        assert os.path.isfile(path)
        with open(path, 'r') as file_pointer:
            file_lines = file_pointer.readlines()
            file_contents = ''.join(file_lines)
        assert 'Red Example Score (2013) for piano' in file_contents
        assert r'\language' in file_contents
        assert r'\version' in file_contents
        assert r'\context Score = "Red Example Score"' in file_contents