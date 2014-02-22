# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_SegmentPackageWrangler_read_only_attributes_01():

    score_manager = scoremanager.core.ScoreManager()
    wrangler = score_manager._segment_package_wrangler
    assert not wrangler._session.is_in_score

    assert wrangler._breadcrumb == 'segments'

    parts = ('segments',)
    assert wrangler.score_storehouse_path_infix_parts == parts


def test_SegmentPackageWrangler_read_only_attributes_02():

    score_manager = scoremanager.core.ScoreManager()
    wrangler = score_manager._segment_package_wrangler
    wrangler._session.current_score_snake_case_name = 'red_example_score'
    assert wrangler._session.is_in_score

    assert wrangler._breadcrumb == 'segments'

    string = 'scoremanager.scorepackages.red_example_score.segments'
    assert wrangler._current_storehouse_package_path == string

    parts = ('segments',)
    assert wrangler.score_storehouse_path_infix_parts == parts

    string = 'scoremanager.scorepackages.red_example_score.segments'
    string += '.__temporary_package'
    assert wrangler._temporary_asset_package_path == string
