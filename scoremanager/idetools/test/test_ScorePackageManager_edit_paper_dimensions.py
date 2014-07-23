# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_ScorePackageManager_edit_paper_dimensions_01():

    path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        )
    metadata_path = os.path.join(path, '__metadata__.py')

    with systemtools.FilesystemState(keep=[metadata_path]):
        manager = scoremanager.idetools.ScorePackageManager
        manager = manager(path=path, session=ide._session)
        manager._get_metadatum('paper_dimensions') == '8.5 x 11 in'
        input_ = 'red~example~score p paper~dimensions 11~x~17~in q'
        ide._run(input_=input_)
        assert manager._get_metadatum('paper_dimensions') == '11 x 17 in'