# -*- encoding: utf-8 -*-
import os
from experimental import *


def test_ScorePackageManager_tempo_inventory_01():

    configuration = scoremanagertools.core.ScoreManagerConfiguration()
    directory_path = os.path.join(
        configuration.built_in_score_packages_directory_path,
        'red_example_score',
        )
        
    score_package_manager = scoremanagertools.managers.ScorePackageManager(
        directory_path
        )

    assert score_package_manager._get_tempo_inventory() == \
        indicatortools.TempoInventory([
        indicatortools.Tempo(durationtools.Duration(1, 8), 72),
        indicatortools.Tempo(durationtools.Duration(1, 8), 108),
        indicatortools.Tempo(durationtools.Duration(1, 8), 90),
        indicatortools.Tempo(durationtools.Duration(1, 8), 135),
        ])
