# -*- encoding: utf-8 -*-
import filecmp
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.AbjadIDE(is_test=True)


def test_MaterialPackageManager_write_stub_definition_py_01():

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'magic_numbers',
        'definition.py',
        )

    with systemtools.FilesystemState(keep=[path]):
        input_ = 'red~example~score m magic~numbers ds y q'
        score_manager._run(input_=input_)
        assert os.path.isfile(path)
        assert not filecmp.cmp(path, path + '.backup')