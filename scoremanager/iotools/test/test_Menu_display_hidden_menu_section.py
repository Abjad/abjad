# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager
pytest.skip('unskip and reimplement after finalizing hidden menu.')



def test_Menu_display_hidden_menu_section_01():

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='hidden q')
    assert score_manager.session.io_transcript[-2][1] == \
        ['Score manager - active scores - hidden commands',
        '',
        '     developer commands - toggle (dct)',
        '     hidden commands - toggle (hct)',
        '     menu commands - toggle (mct)',
        '',
        '     LilyPond log - view (llv)',
        '     Python prompt - interact (ppi)',
        '',
        '     back - go (b)',
        '     home - go (h)',
        '     current score - go (s)',
        '     next score - go (next)',
        '     previous score - go (prev)',
        '     quit (q)',
        '',
        '     cache - view (cv)',
        '     cache - write (cw)',
        '',
        '     repository - add (radd)',
        '     repository - commit (rci)',
        '     repository - status (rst)',
        '     repository - update (rup)',
        '',
        '     scores - show all (ssl)',
        '     scores - show active (ssv)',
        '     scores - show mothballed (ssmb)',
        '',
        '     tests - doctest (tdoc)',
        '     tests - py.test (tpy)',
        '',
        ]


def test_Menu_display_hidden_menu_section_02():

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='red~example~score hidden q')

    assert score_manager.session.io_transcript[-2][1] == \
        ['Red Example Score (2013) - hidden commands',
        '',
        '     developer commands - toggle (dct)',
        '     hidden commands - toggle (hct)',
        '     menu commands - toggle (mct)',
        '',
        '     LilyPond log - view (llv)',
        '     Python prompt - interact (ppi)',
        '',
        '     back - go (b)',
        '     home - go (h)',
        '     current score - go (s)',
        '     next score - go (next)',
        '     previous score - go (prev)',
        '     quit (q)',
        '',
        '     fix package structure (fix)',
        '     list directory contents (ls)',
        '     run pytest (pytest)',
        '     remove score package (removescore)',
        '     view initializer (inv)',
        '     view instrumentation (instrumentation)',
        '',
        '     metadata - add (mda)',
        '     metadata - get (mdg)',
        '     metadata - remove (mdrm)',
        '     metadata module - remove (MDrm)',
        '     metadata module - rewrite (MDrw)',
        '     metadata module - view (MDv)',
        '',
        ]
