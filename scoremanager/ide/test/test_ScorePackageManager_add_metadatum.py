# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.ide.AbjadIDE(is_test=True)
metadata_py_path = os.path.join(
    score_manager._configuration.example_score_packages_directory,
    'red_example_score',
    '__metadata__.py',
    )


def test_ScorePackageManager_add_metadatum_01():


    with systemtools.FilesystemState(keep=[metadata_py_path]):
        # make sure no flavor_type metadatum found
        input_ = 'red~example~score mdg flavor_type <return> q'
        score_manager._run(input_=input_)
        assert 'None' in score_manager._transcript.contents

        # add flavor_type metadatum
        input_ = 'red~example~score mda flavor_type cherry q'
        score_manager._run(input_=input_)

        # maker sure flavor_type metadatum now equal to 'cherry'
        input_ = 'red~example~score mdg flavor_type <return> q'
        score_manager._run(input_=input_)
        assert "'cherry'" in score_manager._transcript.contents