# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_write_metadata_py_01():

    metadata_py_path = os.path.join(
        ide._configuration.wrangler_views_directory,
        '__metadata__.py',
        )

    with systemtools.FilesystemState(keep=[metadata_py_path]):
        input_ = 'Mdw y q'
        ide._run(input_=input_)
        contents = ide._transcript.contents

    assert 'Will write ...' in contents
    assert metadata_py_path in contents