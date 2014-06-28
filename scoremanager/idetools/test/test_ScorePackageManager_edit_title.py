# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_ScorePackageManager_edit_title_01():

    metadata_file_path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'etude_example_score',
        '__metadata__.py',
        )

    with systemtools.FilesystemState(keep=[metadata_file_path]):
        input_ = 'étude~example~score p title Foo~Example~Score q'
        ide._run(input_=input_)
        contents = ide._transcript.contents
        string = 'Foo Example Score (2013) - setup'
        assert string in contents