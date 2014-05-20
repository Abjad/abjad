# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MakerFileWrangler_remove_files_01():

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'makers',
        'Foo.py',
        )

    with systemtools.FilesystemState(remove=[path]):
        with file(path, 'w') as file_pointer:
            file_pointer.write('This is a test file.')
        assert os.path.exists(path)
        input_ = 'red~example~score k rm Foo.py remove q'
        score_manager._run(pending_input=input_)
        assert not os.path.exists(path)