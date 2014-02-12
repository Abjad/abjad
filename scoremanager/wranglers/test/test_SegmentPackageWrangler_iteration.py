# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_SegmentPackageWrangler_iteration_01():

    score_manager = scoremanager.core.ScoreManager()
    wrangler = score_manager.segment_package_wrangler
