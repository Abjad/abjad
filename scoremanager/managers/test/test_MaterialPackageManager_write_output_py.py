# -*- encoding: utf-8 -*-
import filecmp
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageManager_write_output_module_01():

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'materials',
        'magic_numbers',
        'output.py',
        )

    with systemtools.FilesystemState(keep=[path]):
        os.remove(path)
        assert not os.path.exists(path)
        input_ = 'red~example~score m magic~numbers omw y q'
        score_manager._run(pending_input=input_)
        assert os.path.isfile(path)
        contents = score_manager._transcript.contents
        assert 'Will write output material to' in contents