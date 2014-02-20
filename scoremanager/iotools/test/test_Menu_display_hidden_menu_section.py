# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager
pytest.skip('unskip and reimplement after finalizing hidden menu.')



def test_Menu_display_hidden_menu_section_01():

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='hidden q')
    assert score_manager._session.io_transcriptlast_menu_lines == \
        ['Score manager - active scores - hidden commands',
        '',
        '     hidden commands - toggle (hct)',
        '',
        '     LilyPond log - view (lvl)',
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
        '     metadata module - remove (mdmrm)',
        '     metadata module - rewrite (mdmrw)',
        '     metadata module - view (mdmv)',
        '',
        ]
