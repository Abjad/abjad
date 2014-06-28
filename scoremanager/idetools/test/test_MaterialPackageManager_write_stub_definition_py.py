# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageManager_write_stub_definition_py_01():

    package = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'test_package',
        )
    definition_py = os.path.join(package, 'definition.py')

    with systemtools.FilesystemState(remove=[package]):
        input_ = 'red~example~score m new test~package ds y q'
        ide._run(input_=input_)
        assert os.path.isfile(definition_py)