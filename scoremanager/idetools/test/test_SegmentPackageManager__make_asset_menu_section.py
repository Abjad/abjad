# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_SegmentPackageManager__make_asset_menu_section_01():
    r'''Behaves gracefully when no assets are found.
    '''

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = 'blue~example~score g segment~01 q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Blue Example Score (2013)',
        'Blue Example Score (2013) - segments',
        'Blue Example Score (2013) - segments - segment 01',
        ]
    assert score_manager._transcript.titles == titles