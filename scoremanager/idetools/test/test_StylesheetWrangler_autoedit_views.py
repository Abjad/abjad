# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=False)
views_file = os.path.join(
    ide._configuration.wrangler_views_directory,
    '__StylesheetWrangler_views__.py',
    )
metadata_file = os.path.join(
    ide._configuration.wrangler_views_directory,
    '__metadata__.py',
    )


def test_StylesheetWrangler_autoedit_views_01():

    with systemtools.FilesystemState(keep=[views_file, metadata_file]):
        os.remove(views_file)
        os.remove(metadata_file)
        input_ = "Y va add _test add 'clean-letter-14'~in~:ds:"
        input_ += " add 'clean-letter-16'~in~:ds: done"
        input_ += " ren _test _new_test"
        input_ += " _new_test rm 'clean-letter-14' done"
        input_ += " rm _new_test done q"
        ide._run(input_=input_)
        transcript = ide._transcript

    lines = [
        'Abjad IDE - stylesheets - views - _test (EDIT)',
        '',
        '      elements - add (add)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - stylesheets - views - _test (EDIT)',
        '',
        "   1: 'clean-letter-14' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - stylesheets - views - _test (EDIT)',
        '',
        "   1: 'clean-letter-14' in :ds:",
        "   2: 'clean-letter-16' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - move (mv)',
        '      elements - remove (rm)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - stylesheets - views (EDIT)',
        '',
        "   1: _test: 'clean-letter-14' in :ds:, 'clean-letter-16' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '      elements - rename (ren)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - stylesheets - views (EDIT)',
        '',
        "   1: _new_test: 'clean-letter-14' in :ds:, 'clean-letter-16' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '      elements - rename (ren)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - stylesheets - views - _new_test (EDIT)',
        '',
        "   1: 'clean-letter-14' in :ds:",
        "   2: 'clean-letter-16' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - move (mv)',
        '      elements - remove (rm)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - stylesheets - views - _new_test (EDIT)',
        '',
        "   1: 'clean-letter-16' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - stylesheets - views (EDIT)',
        '',
        "   1: _new_test: 'clean-letter-16' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '      elements - rename (ren)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - stylesheets - views (EDIT)',
        '',
        '      elements - add (add)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)