# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)
views_file = os.path.join(
    ide._configuration.wrangler_views_directory,
    '__DistributionFileWrangler_views__.py',
    )


def test_DistributionFileWrangler_autoedit_views_01():

    with systemtools.FilesystemState(keep=[views_file]):
        os.remove(views_file)
        input_ = "dd wa add _test add 'score'~in~:ds:"
        input_ += " add 'audio'~in~:ds: done"
        input_ += " ren _test _new_test"
        input_ += " _new_test rm 'score' done"
        input_ += " rm _new_test done q"
        ide._run(input_=input_)
        transcript = ide._transcript

    lines = [
        'Abjad IDE - distribution depot - views - _test (EDIT)',
        '',
        '      elements - add (add)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - distribution depot - views - _test (EDIT+)',
        '',
        "   1: 'score' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - distribution depot - views - _test (EDIT+)',
        '',
        "   1: 'score' in :ds:",
        "   2: 'audio' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - move (mv)',
        '      elements - remove (rm)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - distribution depot - views (EDIT+)',
        '',
        "   1: _test: 'score' in :ds:, 'audio' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '      elements - rename (ren)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - distribution depot - views (EDIT+)',
        '',
        "   1: _new_test: 'score' in :ds:, 'audio' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '      elements - rename (ren)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - distribution depot - views - _new_test (EDIT)',
        '',
        "   1: 'score' in :ds:",
        "   2: 'audio' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - move (mv)',
        '      elements - remove (rm)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - distribution depot - views - _new_test (EDIT+)',
        '',
        "   1: 'audio' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - distribution depot - views (EDIT+)',
        '',
        "   1: _new_test: 'audio' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '      elements - rename (ren)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - distribution depot - views (EDIT)',
        '',
        '      elements - add (add)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)