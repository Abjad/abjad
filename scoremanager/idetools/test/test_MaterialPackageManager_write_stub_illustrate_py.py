# -*- encoding: utf-8 -*-
import filecmp
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageManager_write_stub_illustrate_py_01():

    path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'magic_numbers',
        '__illustrate__.py',
        )

    with systemtools.FilesystemState(keep=[path]):
        input_ = 'red~example~score m magic~numbers ls y q'
        ide._run(input_=input_)
        assert os.path.isfile(path)
        assert not filecmp.cmp(path, path + '.backup')
        contents = ide._transcript.contents
        assert 'Will write stub to' in contents
        assert 'Wrote stub to' in contents