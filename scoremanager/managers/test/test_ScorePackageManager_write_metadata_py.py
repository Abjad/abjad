# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.AbjadIDE(is_test=True)


def test_ScorePackageManager_write_metadata_py_01():

    metadata_py_path = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        '__metadata__.py',
        )

    with systemtools.FilesystemState(keep=[metadata_py_path]):
        input_ = 'red~example~score mdw <return> q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents

    assert 'Will write ...' in contents
    assert metadata_py_path in contents