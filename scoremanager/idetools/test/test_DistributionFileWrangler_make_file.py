# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_DistributionFileWrangler_make_file_01():

    path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'distribution',
        'test-file.txt',
        )

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'red~example~score d new test-file.txt q'
        ide._run(input_=input_)
        assert os.path.exists(path)