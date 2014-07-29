# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)
views_file = os.path.join(
    ide._configuration.wrangler_views_directory,
    '__MakerFileWrangler_views__.py',
    )


def test_MakerFileWrangler_autoedit_views_01():

    with systemtools.FilesystemState(keep=[views_file]):
        os.remove(views_file)
        input_ = "kk wa add _test add 'RedExampleScoreRhythmMaker.py'~in~:ds:"
        input_ += " add 'RedExampleScoreTemplate.py'~in~:ds: done"
        input_ += " ren _test _new_test"
        input_ += " _new_test rm 'RedExampleScoreRhythmMaker.py' done"
        input_ += " rm _new_test done q"
        ide._run(input_=input_)
        transcript = ide._transcript

    lines = [
        'Abjad IDE - makers depot - views - _test (EDIT)',
        '',
        '      elements - add (add)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - makers depot - views - _test (EDIT+)',
        '',
        "   1: 'RedExampleScoreRhythmMaker.py' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - makers depot - views - _test (EDIT+)',
        '',
        "   1: 'RedExampleScoreRhythmMaker.py' in :ds:",
        "   2: 'RedExampleScoreTemplate.py' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - move (mv)',
        '      elements - remove (rm)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - makers depot - views (EDIT+)',
        '',
        "   1: _test: 'RedExampleScoreRhythmMaker.py' in :ds:, 'RedExampleScoreTemplate.py' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '      elements - rename (ren)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - makers depot - views (EDIT+)',
        '',
        "   1: _new_test: 'RedExampleScoreRhythmMaker.py' in :ds:, 'RedExampleScoreTemplate.py' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '      elements - rename (ren)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - makers depot - views - _new_test (EDIT)',
        '',
        "   1: 'RedExampleScoreRhythmMaker.py' in :ds:",
        "   2: 'RedExampleScoreTemplate.py' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - move (mv)',
        '      elements - remove (rm)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - makers depot - views - _new_test (EDIT+)',
        '',
        "   1: 'RedExampleScoreTemplate.py' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - makers depot - views (EDIT+)',
        '',
        "   1: _new_test: 'RedExampleScoreTemplate.py' in :ds:",
        '',
        '      elements - add (add)',
        '      elements - remove (rm)',
        '      elements - rename (ren)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)

    lines = [
        'Abjad IDE - makers depot - views (EDIT)',
        '',
        '      elements - add (add)',
        '      editing - done (done)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)