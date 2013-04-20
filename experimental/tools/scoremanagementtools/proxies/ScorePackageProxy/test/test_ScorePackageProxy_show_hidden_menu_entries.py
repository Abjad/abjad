from experimental import *


def test_ScorePackageProxy_show_hidden_menu_entries_01():

    studio = scoremanagementtools.studio.ScoreManager()
    studio.run(user_input='example~score~i hidden q')

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
      '     fix package structure (fix)',
      '     list directory contents (ls)',
      '     profile package structure (profile)',
      '     remove score package (removescore)',
      '     manage repository (svn)',
      '     manage tags (tags)',
      '']
