# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialPackageWrangler__run_01():
    r'''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'm q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (4,)

    input_ = 'm b q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (6, (0, 4))

    input_ = 'm h q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (6, (0, 4))

    input_ = 'm s q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (6, (2, 4))

    input_ = 'm asdf q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (6, (2, 4))


def test_MaterialPackageWrangler__run_02():
    r'''Breadcrumbs work.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'm q'
    score_manager._run(pending_user_input=input_)
    title_line = 'Score manager - material library'
    assert score_manager._transcript.last_title == title_line


def test_MaterialPackageWrangler__run_03():
    r'''Menu displays at least one test material.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'm q'
    score_manager._run(pending_user_input=input_)
    menu_lines = score_manager._transcript.last_menu_lines
    input_ = 'example sargasso measures (Abjad)'
    assert any(x.endswith(input_) for x in menu_lines)


def test_MaterialPackageWrangler__run_04():
    r'''Current score is reset on return to home.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score h m q'
    score_manager._run(pending_user_input=input_)

    found_example_articulation_handler = False
    for line in score_manager._transcript.last_menu_lines:
        if 'example articulation handler' in line:
            found_example_articulation_handler = True

    assert found_example_articulation_handler


def test_MaterialPackageWrangler__run_05():
    r'''Current score is reset on backtrack from score to home.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score b m q'
    score_manager._run(pending_user_input=input_)

    input_ = 'Score manager - material library'
    assert score_manager._transcript.entries[-2].title == input_