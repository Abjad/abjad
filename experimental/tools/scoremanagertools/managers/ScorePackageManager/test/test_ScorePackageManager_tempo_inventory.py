# -*- encoding: utf-8 -*-
from experimental import *


def test_ScorePackageManager_tempo_inventory_01():

    score_package_manager = scoremanagertools.managers.ScorePackageManager(
        'scoremanagertools.scorepackages.red_example_score')

    assert score_package_manager._get_tempo_inventory() == \
        contexttools.TempoMarkInventory([
        contexttools.TempoMark(durationtools.Duration(1, 8), 72),
        contexttools.TempoMark(durationtools.Duration(1, 8), 108),
        contexttools.TempoMark(durationtools.Duration(1, 8), 90),
        contexttools.TempoMark(durationtools.Duration(1, 8), 135),
        ])
