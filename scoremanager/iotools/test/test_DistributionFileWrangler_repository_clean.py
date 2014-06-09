# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.iotools.AbjadIDE(is_test=True)

foo_path = os.path.join(
    score_manager._configuration.example_score_packages_directory,
    'red_example_score',
    'distribution',
    'test_foo.txt',
    )


def test_DistributionFileWrangler_repository_clean_01():
    r'''In score.
    '''

    with systemtools.FilesystemState(remove=[foo_path]):
        with open(foo_path, 'w') as file_pointer:
            file_pointer.write('')
        assert os.path.isfile(foo_path)
        input_ = 'red~example~score d rcn y q'
        score_manager._run(input_=input_)
        assert not os.path.exists(foo_path)


def test_DistributionFileWrangler_repository_clean_02():
    r'''Out of score.
    '''

    with systemtools.FilesystemState(remove=[foo_path]):
        with open(foo_path, 'w') as file_pointer:
            file_pointer.write('')
        assert os.path.isfile(foo_path)
        input_ = 'd rcn y q'
        score_manager._run(input_=input_)
        assert not os.path.exists(foo_path)