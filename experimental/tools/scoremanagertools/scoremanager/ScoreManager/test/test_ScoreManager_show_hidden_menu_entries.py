from experimental import *


def test_ScoreManager_show_hidden_menu_entries_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(user_input='hidden q')
    assert score_manager._session.transcript[-2][1] == \
        ['     back (b)',
         '     exec statement (exec)',
         '     grep directories (grep)',
         '     edit client source (here)',
         '     display hidden menu section (hidden)',
         '     home (home)',
         '     next score (next)',
         '     prev score (prev)',
         '     quit (q)',
         '     redraw (r)',
         '     current score (score)',
         '     show/hide commands (cmds)',
         '     toggle where (tw)',
         '     display calling code line number (where)',
         '',
         '     show active scores only (active)',
         '     show all scores (all)',
         '     fix all score package structures (fix)',
         '     show mothballed scores only (mb)',
         '     profile packages (profile)',
         '     run py.test on all scores (py.test)',
         '     work with repository (svn)',
         '     write cache (wc)',
         '']
