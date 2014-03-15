# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager
pytest.skip('unskip after finalizing material management menu.')


def test_MaterialManager_screenscrapes_01():
    r'''Score material run from home.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score m tempo~inventory q'
    score_manager._run(pending_user_input=string, is_test=True)

    assert score_manager._transcript.last_menu_lines == [
        'Red Example Score (2013) - materials - tempo inventory', 
        '', 
        '     Tempo(Duration(1, 8), 72)', 
        '     Tempo(Duration(1, 8), 108)', 
        '     Tempo(Duration(1, 8), 90)', 
        '     Tempo(Duration(1, 8), 135)', 
        '', 
        '     material - edit (me)', 
        '     output material - view (omv)', 
        '', 
        '     illustration builder - edit (ibe)', 
        '     illustration builder - interpret (ibi)', 
        '     score stylesheet - select (sss)', 
        '', 
        '     output pdf - make (pdfm)', 
        '',
        ]
