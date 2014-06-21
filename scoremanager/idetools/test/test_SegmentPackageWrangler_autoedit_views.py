# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=False)
views_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__SegmentPackageWrangler_views__.py',
    )
metadata_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__metadata__.py',
    )


def test_SegmentPackageWrangler_autoedit_views_01():

    with systemtools.FilesystemState(keep=[views_file, metadata_file]):
        os.remove(views_file)
        os.remove(metadata_file)
        input_ = "G va add _test add 'A'~in~:ds:"
        input_ += " add 'B'~in~:ds: done"
        input_ += " ren _test _new_test"
        input_ += " _new_test rm 'A' done"
        input_ += " rm _new_test done q"
        score_manager._run(input_=input_)
        transcript = score_manager._transcript

    lines = [
        'Abjad IDE - segments - views - _test (EDIT)',
        '',
        '      elements - add (add)',
        '',
        '      done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - segments - views - _test (EDIT)',
        '',
        "   1: 'A' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '',
        '      done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - segments - views - _test (EDIT)',
        '',
        "   1: 'A' in :ds:",
        "   2: 'B' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - move (mv)',
        '      elements - remove (rm)',
        '',
        '      done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - segments - views (EDIT)',
        '',
        "   1: _test: 'A' in :ds:, 'B' in :ds:",
        '',
        '      element - rename (ren)',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '',
        '      done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - segments - views (EDIT)',
        '',
        "   1: _new_test: 'A' in :ds:, 'B' in :ds:",
        '',
        '      element - rename (ren)',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '',
        '      done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - segments - views - _new_test (EDIT)',
        '',
        "   1: 'A' in :ds:",
        "   2: 'B' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - move (mv)',
        '      elements - remove (rm)',
        '',
        '      done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - segments - views - _new_test (EDIT)',
        '',
        "   1: 'B' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '',
        '      done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - segments - views (EDIT)',
        '',
        "   1: _new_test: 'B' in :ds:",
        '',
        '      element - rename (ren)',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '',
        '      done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - segments - views (EDIT)',
        '',
        '      elements - add (add)',
        '',
        '      done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)