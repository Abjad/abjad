# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)
views_file = os.path.join(
    ide._configuration.wrangler_views_directory,
    '__BuildFileWrangler_views__.py',
    )


def test_BuildFileWrangler_autoedit_views_01():

    with systemtools.FilesystemState(keep=[views_file]):
        os.remove(views_file)
        input_ = "uu wa add _test add 'front-cover'~in~:ds:"
        input_ += " add 'back-cover'~in~:ds: done"
        input_ += " ren _test _new_test"
        input_ += " _new_test rm 'front-cover' done"
        input_ += " rm _new_test done q"
        ide._run(input_=input_)
        transcript = ide._transcript

    lines = [
        'Abjad IDE - build depot - views - _test (EDIT)',
        '',
        '      elements - add (add)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - build depot - views - _test (EDIT+)',
        '',
        "   1: 'front-cover' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - build depot - views - _test (EDIT+)',
        '',
        "   1: 'front-cover' in :ds:",
        "   2: 'back-cover' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - move (mv)',
        '      elements - remove (rm)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - build depot - views (EDIT+)',
        '',
        "   1: _test: 'front-cover' in :ds:, 'back-cover' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '      elements - rename (ren)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - build depot - views (EDIT+)',
        '',
        "   1: _new_test: 'front-cover' in :ds:, 'back-cover' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '      elements - rename (ren)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - build depot - views - _new_test (EDIT)',
        '',
        "   1: 'front-cover' in :ds:",
        "   2: 'back-cover' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - move (mv)',
        '      elements - remove (rm)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - build depot - views - _new_test (EDIT+)',
        '',
        "   1: 'back-cover' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - build depot - views (EDIT+)',
        '',
        "   1: _new_test: 'back-cover' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '      elements - rename (ren)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - build depot - views (EDIT)',
        '',
        '      elements - add (add)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)