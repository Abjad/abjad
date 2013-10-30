# -*- encoding: utf-8 -*-
import os
from experimental import *


def test_ScorePackageManager_tempo_inventory_01():

    configuration = scoremanagertools.scoremanager.ScoreManagerConfiguration()
    directory_path = os.path.join(
        configuration.built_in_score_packages_directory_path,
        'red_example_score',
        )
        
    score_package_manager = scoremanagertools.managers.ScorePackageManager(
        directory_path
        )

    assert score_package_manager._get_tempo_inventory() == \
        marktools.TempoMarkInventory([
        marktools.TempoMark(durationtools.Duration(1, 8), 72),
        marktools.TempoMark(durationtools.Duration(1, 8), 108),
        marktools.TempoMark(durationtools.Duration(1, 8), 90),
        marktools.TempoMark(durationtools.Duration(1, 8), 135),
        ])
