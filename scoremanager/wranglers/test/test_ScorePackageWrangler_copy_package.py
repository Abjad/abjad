# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.iotools.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_copy_package_01():

    pretty_path = os.path.join(
        score_manager._configuration.user_score_packages_directory,
        'pretty_example_score',
        )

    with systemtools.FilesystemState(remove=[pretty_path]):
        input_ = 'cp Red~Example~Score Pretty~Example~Score y q'
        score_manager._run(input_=input_)
        assert os.path.exists(pretty_path)
        manager = scoremanager.wranglers.ScorePackageManager
        manager = manager(path=pretty_path, session=score_manager._session)
        title = 'Pretty Example Score'
        manager._add_metadatum('title', title)
        input_ = 'rm Pretty~Example~Score remove q'
        score_manager._run(input_=input_)
        assert not os.path.exists(pretty_path)