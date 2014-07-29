# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)
views_file = os.path.join(
    ide._configuration.wrangler_views_directory,
    '__ScorePackageWrangler_views__.py',
    )


def test_ScorePackageWrangler_autoedit_views_01():

    with systemtools.FilesystemState(keep=[views_file]):
        os.remove(views_file)
        input_ = "ss wa add _test add 'Red~Example~Score'~in~:ds:"
        input_ += " add 'Blue~Example~Score'~in~:ds: done"
        input_ += " ren _test _new_test"
        input_ += " _new_test rm 'Red~Example~Score' done"
        input_ += " rm _new_test done q"
        ide._run(input_=input_)
        transcript = ide._transcript

    lines = [
        'Abjad IDE - scores - views - _test (EDIT)',
        '',
        '      elements - add (add)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - scores - views - _test (EDIT+)',
        '',
        "   1: 'Red Example Score' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - scores - views - _test (EDIT+)',
        '',
        "   1: 'Red Example Score' in :ds:",
        "   2: 'Blue Example Score' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - move (mv)',
        '      elements - remove (rm)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - scores - views (EDIT+)',
        '',
        "   1: _test: 'Red Example Score' in :ds:, 'Blue Example Score' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '      elements - rename (ren)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - scores - views (EDIT+)',
        '',
        "   1: _new_test: 'Red Example Score' in :ds:, 'Blue Example Score' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '      elements - rename (ren)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - scores - views - _new_test (EDIT)',
        '',
        "   1: 'Red Example Score' in :ds:",
        "   2: 'Blue Example Score' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - move (mv)',
        '      elements - remove (rm)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - scores - views - _new_test (EDIT+)',
        '',
        "   1: 'Blue Example Score' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - scores - views (EDIT+)',
        '',
        "   1: _new_test: 'Blue Example Score' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '      elements - rename (ren)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - scores - views (EDIT)',
        '',
        '      elements - add (add)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)