# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_StylesheetWrangler__make_asset_menu_section_01():
    r'''Behaves gracefully when no assets are found.
    '''

    ide = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = 'blue~example~score y q'
    ide._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Blue Example Score (2013)',
        'Blue Example Score (2013) - stylesheets directory',
        ]
    assert ide._transcript.titles == titles