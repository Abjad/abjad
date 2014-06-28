# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)
metadata_py_path = os.path.join(
    ide._configuration.example_score_packages_directory,
    'red_example_score',
    'segments',
    'segment_01',
    '__metadata__.py',
    )


def test_SegmentPackageManager_write_metadata_py_01():

    with systemtools.FilesystemState(keep=[metadata_py_path]):
        input_ = 'red~example~score g A mdw q'
        ide._run(input_=input_)
        contents = ide._transcript.contents

    assert 'Will write ...' in contents
    assert metadata_py_path in contents