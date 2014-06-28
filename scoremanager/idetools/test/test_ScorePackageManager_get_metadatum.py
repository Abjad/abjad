# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True) 
metadata_py_path = os.path.join(
    ide._configuration.example_score_packages_directory,
    'red_example_score',
    '__metadata__.py',
    )


def test_ScorePackageManager_get_metadatum_01():


    with systemtools.FilesystemState(keep=[metadata_py_path]):
        # make sure no flavor_type metadatum found
        input_ = 'red~example~score mdg flavor_type q'
        ide._run(input_=input_)
        assert 'None' in ide._transcript.contents

        # add flavor_type metadatum
        input_ = 'red~example~score mda flavor_type cherry q'
        ide._run(input_=input_)

        # maker sure flavor_type metadatum now equal to 'cherry'
        input_ = 'red~example~score mdg flavor_type q'
        ide._run(input_=input_)
        assert "'cherry'" in ide._transcript.contents