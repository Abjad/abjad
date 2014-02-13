# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager



def test_Menu_display_hidden_menu_section_01():

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='hidden q')
    assert score_manager.session.io_transcript[-2][1] == \
        ['Score manager - active scores - hidden commands',
        '',
        '     display calling code (where)',
        '     display hidden menu (hidden)',
        '     edit client source (here)',
        '     execute statement (exec)',
        '     go back (b)',
        '     go home (home)',
        '     go home (H)',
        '     go to current score (score)',
        '     go to current score (S)',
        '     go to next score (next)',
        '     go to prev score (prev)',
        '     quit (q)',
        '     redraw (r)',
        '     toggle menu commands (tmc)',
        '     toggle where-tracking (twt)',
        '     view LilyPond log (log)',
        '',
        '     scores - fix (fix)',
        '     scores - profile (profile)',
        '     scores - test (test)',
        '',
        '     show - active scores (active)',
        '     show - all score (all)',
        '     show - mothballed scores (mothballed)',
        '',
        '     work with repository (rep)',
        '     write cache (wc)',
        '']


def test_Menu_display_hidden_menu_section_02():

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='red~example~score hidden q')

    assert score_manager.session.io_transcript[-2][1] == \
        ['Red Example Score (2013) - hidden commands',
        '',
        '     display calling code (where)',
        '     display hidden menu (hidden)',
        '     edit client source (here)',
        '     execute statement (exec)',
        '     go back (b)',
        '     go home (home)',
        '     go home (H)',
        '     go to current score (score)',
        '     go to current score (S)',
        '     go to next score (next)',
        '     go to prev score (prev)',
        '     quit (q)',
        '     redraw (r)',
        '     toggle menu commands (tmc)',
        '     toggle where-tracking (twt)',
        '     view LilyPond log (log)',
        '',
        '     fix package structure (fix)',
        '     list directory contents (ls)',
        '     manage repository (rep)',
        '     manage metadata (metadata)',
        '     profile package structure (profile)',
        '     run pytest (pytest)',
        '     remove score package (removescore)',
        '     view initializer (inv)',
        '     view instrumentation (instrumentation)',
        '     metadata - view (mdv)',
        '     metadata - write (mdw)',
        '']
