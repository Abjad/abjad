# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_ScorePackageManager_edit_forces_tagline_01():

    path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        )
    metadata_path = os.path.join(path, '__metadata__.py')

    manager = scoremanager.idetools.ScorePackageManager
    manager = manager(path=path, session=ide._session)
    assert manager._get_metadatum('forces_tagline') == 'for piano'

    with systemtools.FilesystemState(keep=[metadata_path]):
        input_ = 'red~example~score p tagline for~foo~bar q'
        ide._run(input_=input_)
        session = scoremanager.idetools.Session(is_test=True)
        assert manager._get_metadatum('forces_tagline') == 'for foo bar'