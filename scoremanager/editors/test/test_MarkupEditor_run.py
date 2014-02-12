# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MarkupEditor_run_01():

    editor = scoremanager.editors.MarkupEditor()
    editor._run(pending_user_input='''arg '"foo~text~here"' dir up done''')
    markup = markuptools.Markup('"foo text here"', direction='up')

    assert editor.target == markup


def test_MarkupEditor_run_02():

    editor = scoremanager.editors.MarkupEditor()
    editor._run(pending_user_input='arg foo~text done')
    markup = markuptools.Markup('foo text')

    assert editor.target == markup


def test_MarkupEditor_run_03():

    markup = markuptools.Markup('foo bar', markup_name='foo')
    editor = scoremanager.editors.MarkupEditor(target=markup)
    string = 'arg entirely~new~text name bar direction up done'
    editor._run(pending_user_input=string)

    assert editor.target == markuptools.Markup(
        'entirely new text', 
        direction='up', 
        markup_name='bar',
        )
