from experimental import *


def test_ScoreManager_show_hidden_menu_entries_01():

    studio = scoremanagementtools.studio.ScoreManager()
    studio.run(user_input='hidden q')
    assert studio.transcript[-2] == \
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
      '     studio (studio)',
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
