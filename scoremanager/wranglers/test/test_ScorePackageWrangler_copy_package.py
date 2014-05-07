# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScorePackageWrangler_copy_package_01():

    pretty_path = os.path.join(
        score_manager._configuration.user_score_packages_directory_path,
        'pretty_example_score',
        )

    assert not os.path.exists(pretty_path)

    try:
        input_ = 'cp Red~Example~Score Pretty~Example~Score y q'
        score_manager._run(pending_input=input_)
        assert os.path.exists(pretty_path)
        manager = scoremanager.managers.ScorePackageManager
        manager = manager(path=pretty_path, session=score_manager._session)
        title = 'Pretty Example Score'
        manager._add_metadatum('title', title)
        input_ = 'rm Pretty~Example~Score remove q'
        score_manager._run(pending_input=input_)
        assert not os.path.exists(pretty_path)
    finally:
        if os.path.exists(pretty_path):
            shtuil.rmtree(pretty_path)

    assert not os.path.exists(pretty_path)