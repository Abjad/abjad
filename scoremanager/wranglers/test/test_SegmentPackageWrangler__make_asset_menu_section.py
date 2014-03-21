# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_SegmentPackageWrangler__make_asset_menu_section_01():
    r'''Omits score annotation when listing segments in score.
    '''

    score_manager = scoremanager.core.ScoreManager()
    input_ = 'red~example~score g q'
    score_manager._run(pending_user_input=input_)

    string = 'Red Example Score (2013) - segments'
    assert score_manager._transcript.last_menu_lines[0] == string

    found_asset_entry_without_annotation = False
    for line in score_manager._transcript.last_menu_lines:
        if line.endswith('segment 01'):
            found_asset_entry_without_annotation = True
    assert found_asset_entry_without_annotation