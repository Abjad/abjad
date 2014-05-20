# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScorePackageManager_edit_year_01():

    metadata_file = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        '__metadata__.py',
        )
        
    with systemtools.FilesystemState(keep=[metadata_file]):
        input_ = 'red~example~score p year 2001 default q'
        score_manager._run(pending_input=input_)
        contents = score_manager._transcript.contents
        string = 'Red Example Score (2001)'
        assert string in contents