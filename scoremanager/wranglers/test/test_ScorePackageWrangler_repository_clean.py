# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)

foo_path = os.path.join(
    score_manager._configuration.example_score_packages_directory,
    'red_example_score',
    'test_foo.txt',
    )


def test_ScorePackageWrangler_repository_clean_01():

    with systemtools.FilesystemState(remove=[foo_path]):
        with file(foo_path, 'w') as file_pointer:
            file_pointer.write('')
        assert os.path.isfile(foo_path)
        input_ = 'rcn y q'
        score_manager._run(pending_input=input_)
        assert not os.path.exists(foo_path)