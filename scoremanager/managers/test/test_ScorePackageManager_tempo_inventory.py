# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_ScorePackageManager_tempo_inventory_01():

    configuration = scoremanager.core.ScoreManagerConfiguration()
    path = os.path.join(
        configuration.abjad_score_packages_directory_path,
        'red_example_score',
        )
        
    session = scoremanager.core.Session(is_test=True)
    score_package_manager = scoremanager.managers.ScorePackageManager(
        path=path,
        session=session,
        )

    assert score_package_manager._get_tempo_inventory() == \
        indicatortools.TempoInventory([
        indicatortools.Tempo(durationtools.Duration(1, 8), 72),
        indicatortools.Tempo(durationtools.Duration(1, 8), 108),
        indicatortools.Tempo(durationtools.Duration(1, 8), 90),
        indicatortools.Tempo(durationtools.Duration(1, 8), 135),
        ])
