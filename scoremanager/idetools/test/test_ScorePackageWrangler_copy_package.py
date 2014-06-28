# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_copy_package_01():

    pretty_path = os.path.join(
        ide._configuration.user_score_packages_directory,
        'pretty_example_score',
        )

    with systemtools.FilesystemState(remove=[pretty_path]):
        input_ = 'cp Red~Example~Score Pretty~Example~Score y q'
        ide._run(input_=input_)
        assert os.path.exists(pretty_path)
        manager = scoremanager.idetools.ScorePackageManager
        manager = manager(path=pretty_path, session=ide._session)
        title = 'Pretty Example Score'
        manager._add_metadatum('title', title)
        input_ = 'rm Pretty~Example~Score remove q'
        ide._run(input_=input_)
        assert not os.path.exists(pretty_path)