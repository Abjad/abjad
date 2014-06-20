# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=False)
views_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__AbjadIDE_views__.py',
    )
metadata_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__metadata__.py',
    )


def test_AbjadIDE_autoedit_views_01():

    with systemtools.FilesystemState(keep=[views_file, metadata_file]):
        os.remove(metadata_file)
        input_ = "** va add _test add 'clean-letter'~in~:ds:"
        input_ += " add 'rhythm-letter'~in~:ds: done"
        input_ += " ren _test _new_test"
        input_ += " _new_test rm 'clean-letter done"
        input_ += " rm _new_test done q"
        score_manager._run(input_=input_)
        transcript = score_manager._transcript

    lines = [
        'Abjad IDE - views - _test (EDIT)',
        '',
        '      elements - add (add)',
        '',
        '      done (done)',
        '',
        ]
    assert any(_.lines for _ in transcript)

    lines = [
        'Abjad IDE - views - _test (EDIT)',
        '',
        "   1: 'clean-letter' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '',
        '      done (done)',
        '',
        ]
    assert any(_.lines for _ in transcript)

    lines = [
        'Abjad IDE - views - _test (EDIT)',
        '',
        "   1: 'clean-letter' in :ds:",
        "   2: 'rhythm-letter' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - move (mv)',
        '      elements - remove (rm)',
        '',
        '      done (done)',
        '',
        ]
    assert any(_.lines for _ in transcript)

    lines = [
        'Abjad IDE - views (EDIT)',
        '',
        "   1: _test: 'clean-letter' in :ds:, 'rhythm-letter' in :ds:",
        '',
        '      element - rename (ren)',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '',
        '      done (done)',
        '',
        ]
    assert any(_.lines for _ in transcript)

    lines = [
        'Abjad IDE - views (EDIT)',
        '',
        "   1: _new_test: 'clean-letter' in :ds:, 'rhythm-letter' in :ds:",
        '',
        '      element - rename (ren)',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '',
        '      done (done)',
        '',
        ]
    assert any(_.lines for _ in transcript)

    lines = [
        'Abjad IDE - views - _new_test (EDIT)',
        '',
        "   1: 'clean-letter' in :ds:",
        "   2: 'rhythm-letter' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - move (mv)',
        '      elements - remove (rm)',
        '',
        '      done (done)',
        '',
        ]
    assert any(_.lines for _ in transcript)

    lines = [
        'Abjad IDE - views - _new_test (EDIT)',
        '',
        "   1: 'rhythm-letter' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '',
        '      done (done)',
        '',
        ]
    assert any(_.lines for _ in transcript)

    lines = [
        'Abjad IDE - views (EDIT)',
        '',
        "   1: _new_test: 'rhythm-letter' in :ds:",
        '',
        '      element - rename (ren)',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '',
        '      done (done)',
        '',
        ]
    assert any(_.lines for _ in transcript)

    lines = [
        'Abjad IDE - views (EDIT)',
        '',
        '      elements - add (add)',
        '',
        '      done (done)',
        '',
        ]
    assert any(_.lines for _ in transcript)