# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_ScorePackageManager_write_stub_init_py_01():

    path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        '__init__.py',
        )

    with systemtools.FilesystemState(keep=[path]):
        os.remove(path)
        assert not os.path.exists(path)
        input_ = 'red~example~score ns y q'
        ide._run(input_=input_)
        assert os.path.isfile(path)
        contents = ide._transcript.contents
        assert 'Will write stub to' in contents