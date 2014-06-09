# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.iotools.AbjadIDE(is_test=True)
metadata_py_path = os.path.join(
    score_manager._configuration.example_score_packages_directory,
    'red_example_score',
    'materials',
    'magic_numbers',
    '__metadata__.py',
    )


def test_MaterialPackageManager_write_metadata_py_01():

    with systemtools.FilesystemState(keep=[metadata_py_path]):
        input_ = 'red~example~score m magic~numbers mdw <return> q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents

    assert 'Will write ...' in contents
    assert metadata_py_path in contents