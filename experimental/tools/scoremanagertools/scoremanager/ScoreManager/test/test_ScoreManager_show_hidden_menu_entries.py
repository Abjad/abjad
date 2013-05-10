from experimental import *


def test_ScoreManager_show_hidden_menu_entries_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(user_input='hidden q')
    assert score_manager._session.transcript[-2][1] == \
     ['     back (b)',
      '     exec statement (exec)',
      '     grep directories (grep)',
      '     edit client source (here)',
      '     show hidden items (hidden)',
      '     next score (next)',
      '     prev score (prev)',
      '     quit (q)',
      '     redraw (r)',
      '     score (score)',
      '     home (home)',
      '     toggle menu (tm)',
      '     toggle where (tw)',
      '     show menu client (where)',
      '',
      '     work with repository (svn)',
      '     show active scores only (active)',
      '     show all scores (all)',
      '     show mothballed scores only (mb)',
      '     profile packages (profile)',
      '']
