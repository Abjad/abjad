# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialPackageWrangler__run_01():
    r'''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='lmm q', is_test=True)
    assert score_manager._transcript.signature == (4,)

    score_manager._run(pending_user_input='lmm b q', is_test=True)
    assert score_manager._transcript.signature == (6, (0, 4))

    score_manager._run(pending_user_input='lmm h q', is_test=True)
    assert score_manager._transcript.signature == (6, (0, 4))

    score_manager._run(pending_user_input='lmm s q', is_test=True)
    assert score_manager._transcript.signature == (6, (2, 4))

    score_manager._run(pending_user_input='lmm asdf q', is_test=True)
    assert score_manager._transcript.signature == (6, (2, 4))


def test_MaterialPackageWrangler__run_02():
    r'''Breadcrumbs work.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='lmm q', is_test=True)
    title_line = 'Score manager - material library'
    assert score_manager._transcript.last_title == title_line


def test_MaterialPackageWrangler__run_03():
    r'''Menu displays at least one test material.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='lmm q', is_test=True)
    menu_lines = score_manager._transcript.last_menu_lines
    assert any(x.endswith('example sargasso measures') for x in menu_lines)


def test_MaterialPackageWrangler__run_04():
    r'''Current score is reset on return to home.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score h lmm q'
    score_manager._run(pending_user_input=string, is_test=True)

    found_example_articulation_handler = False
    for line in score_manager._transcript.last_menu_lines:
        if 'example articulation handler' in line:
            found_example_articulation_handler = True

    assert found_example_articulation_handler 
