from experimental import *


def test_ScorePackageProxy_show_hidden_menu_entries_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(user_input='red~example~score hidden q')

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
      '     fix package structure (fix)',
      '     list directory contents (ls)',
      '     profile package structure (profile)',
      '     remove score package (removescore)',
      '     manage repository (svn)',
      '     manage tags (tags)',
      '']
