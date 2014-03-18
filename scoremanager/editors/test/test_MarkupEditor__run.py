# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MarkupEditor__run_01():

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.MarkupEditor(session=session)
    input_ = '''arg '"foo~text~here"' dir up done'''
    editor._run(pending_user_input=input_)
    markup = markuptools.Markup('"foo text here"', direction='up')

    assert editor.target == markup


def test_MarkupEditor__run_02():

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.MarkupEditor(session=session)
    input_ = 'arg foo~text done'
    editor._run(pending_user_input=input_)
    markup = markuptools.Markup('foo text')

    assert editor.target == markup


def test_MarkupEditor__run_03():

    markup = markuptools.Markup('foo bar')
    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.MarkupEditor
    editor = editor(target=markup, session=session)
    input_ = 'arg entirely~new~text direction up done'
    editor._run(pending_user_input=input_)

    assert editor.target == markuptools.Markup(
        'entirely new text', 
        direction='up', 
        )
