# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_interpret_music_01():
    r'''Works when music already exists.
    '''

    source_path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'build',
        'music.ly',
        )
    path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'build',
        'music.pdf',
        )

    with systemtools.FilesystemState(keep=[source_path, path]):
        os.remove(path)
        assert not os.path.exists(path)
        input_ = 'red~example~score u mi q'
        ide._run(input_=input_)
        assert os.path.isfile(path)
        assert systemtools.TestManager.compare_lys(
            source_path,
            source_path + '.backup',
            )
        #assert pdf-diff(path, path + '.backup')