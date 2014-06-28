# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_remove_files_01():

    path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'makers',
        'Foo.py',
        )

    with systemtools.FilesystemState(remove=[path]):
        with open(path, 'w') as file_pointer:
            file_pointer.write('This is a test file.')
        assert os.path.exists(path)
        input_ = 'red~example~score k rm Foo.py remove q'
        ide._run(input_=input_)
        assert not os.path.exists(path)