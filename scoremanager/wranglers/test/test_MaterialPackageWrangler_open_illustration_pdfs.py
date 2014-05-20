# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageWrangler_open_illustration_pdfs_01():

    package_names = ('pitch_range_inventory', 'tempo_inventory')
    paths = []
    for name in package_names:
        path = os.path.join(
            score_manager._configuration.example_score_packages_directory,
            'red_example_score',
            'materials',
            name,
            'illustration.pdf',
            )
        paths.append(path)

    input_ = 'red~example~score m ipo y q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents
    assert score_manager._session._attempted_to_open_file
    assert 'Will open ...' in contents
    for path in paths:
        assert path in contents