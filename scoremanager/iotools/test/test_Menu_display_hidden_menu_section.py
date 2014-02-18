# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager



def test_Menu_display_hidden_menu_section_01():

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='hidden q')
    assert score_manager.session.io_transcript[-2][1] == \
        ['Score manager - active scores - hidden commands',
        '',
        '     code location - edit (sce)',
        '     code location - where (scl)',
        '     location-tracking - toggle (ltt)',
        '',
        '     display hidden menu (hidden)',
        '     execute statement (exec)',
        '     go back (b)',
        '     go home (h)',
        '     go to current score (s)',
        '     go to next score (next)',
        '     go to prev score (prev)',
        '     quit (q)',
        '     toggle menu commands (tmc)',
        '     view LilyPond log (log)',
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
        '     code location - edit (sce)',
        '     code location - where (scl)',
        '     location-tracking - toggle (ltt)',
        '',
        '     display hidden menu (hidden)',
        '     execute statement (exec)',
        '     go back (b)',
        '     go home (h)',
        '     go to current score (s)',
        '     go to next score (next)',
        '     go to prev score (prev)',
        '     quit (q)',
        '     toggle menu commands (tmc)',
        '     view LilyPond log (log)',
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
