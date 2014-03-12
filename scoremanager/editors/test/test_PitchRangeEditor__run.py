# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_PitchRangeEditor__run_01():

    session = scoremanager.core.Session()
    editor = scoremanager.editors.PitchRangeEditor(session=session)
    editor._run(pending_user_input="1 [F#3, C5) q")
    assert editor.target == pitchtools.PitchRange('[F#3, C5)')

    session = scoremanager.core.Session()
    editor = scoremanager.editors.PitchRangeEditor(session=session)
    editor._run(pending_user_input='1 (A0, C8] q')
    assert editor.target == pitchtools.PitchRange('(A0, C8]')


def test_PitchRangeEditor__run_02():
    r'''Quit, score, home & junk all work.

    Note that back doesn't yet work here
    because 'b' interprets as named chromatic pitch.
    '''

    session = scoremanager.core.Session()
    editor = scoremanager.editors.PitchRangeEditor(session=session)
    editor._run(pending_user_input='q')
    assert editor._transcript.signature == (2,)

    session = scoremanager.core.Session()
    editor = scoremanager.editors.PitchRangeEditor(session=session)
    editor._run(pending_user_input='sco q')
    assert editor._transcript.signature == (4, (0, 2))

    session = scoremanager.core.Session()
    editor = scoremanager.editors.PitchRangeEditor(session=session)
    editor._run(pending_user_input='h')
    assert editor._transcript.signature == (2,)

    session = scoremanager.core.Session()
    editor = scoremanager.editors.PitchRangeEditor(session=session)
    editor._run(pending_user_input='foo q')
    assert editor._transcript.signature == (4, (0, 2))
