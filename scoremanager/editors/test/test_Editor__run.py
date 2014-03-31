# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Editor__run_01():
    r'''Works to change clef name.
    '''

    target = Clef('alto')
    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.Editor(
        session=session,
        target=target,
        )
    input_ = 'nm tenor done'
    editor._run(pending_user_input=input_)

    assert editor.target == Clef('tenor')


def test_Editor__run_02():
    r'''Works with unmodified tempo.
    '''

    target = Tempo()
    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.Editor(
        session=session,
        target=target,
        )
    input_ = 'done'
    editor._run(pending_user_input=input_)

    assert editor.target is target


def test_Editor__run_03():
    r'''Works to change tempo duration with pair.
    '''

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.Editor(
        session=session,
        target=Tempo(),
        )
    input_ = 'duration (1, 8) units 98 done'
    editor._run(pending_user_input=input_)

    assert editor.target == Tempo(Duration(1, 8), 98)


def test_Editor__run_04():
    r'''Works to change tempo duration with duration object.
    '''

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.Editor(
        session=session,
        target=Tempo(),
        )
    input_ = 'duration Duration(1, 8) units 98 done'
    editor._run(pending_user_input=input_)

    assert editor.target == Tempo(Duration(1, 8), 98)


def test_Editor__run_05():
    r'''Works to change markup contents.
    '''

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.Editor(
        session=session,
        target=Markup(),
        )
    input_ = 'arg foo~text done'
    editor._run(pending_user_input=input_)

    markup = markuptools.Markup('foo text')
    assert editor.target == markup


def test_Editor__run_06():
    r'''Works to change markup contents and direction.
    '''

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.Editor(
        session=session,
        target=Markup(),
        )
    input_ = '''arg '"foo~text~here"' dir up done'''
    editor._run(pending_user_input=input_)

    assert editor.target == Markup('"foo text here"', direction=Up)


def test_Editor__run_07():
    r'''Works to change markup contents and direction.
    '''

    target = Markup('foo bar')
    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.Editor(
        session=session,
        target=target,
        )
    input_ = 'arg entirely~new~text direction up done'
    editor._run(pending_user_input=input_)

    assert editor.target == Markup('entirely new text', direction=Up)


def test_Editor__run_08():
    r'''Works to change component source and target.
    '''

    target = pitchtools.OctaveTranspositionMappingComponent()
    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.Editor(
        session=session,
        target=target,
        )
    input_ = 'source [A0, C8] target -18 q'
    editor._run(pending_user_input=input_)

    component = pitchtools.OctaveTranspositionMappingComponent('[A0, C8]', -18)
    assert editor.target == component