# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MakerModuleWrangler_make_module_01():

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'makers',
        'FooMaker.py',
        )

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'red~example~score k new FooMaker.py q'
        score_manager._run(pending_input=input_)
        assert os.path.exists(path)