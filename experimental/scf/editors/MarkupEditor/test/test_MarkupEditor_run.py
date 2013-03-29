from abjad import *
import scf


def test_MarkupEditor_run_01():

    editor = scf.editors.MarkupEditor()
    editor.run(user_input='''arg '"foo~text~here"' dir up done''')
    markup = markuptools.Markup('"foo text here"', direction='up')

    assert editor.target == markup


def test_MarkupEditor_run_02():

    editor = scf.editors.MarkupEditor()
    editor.run(user_input='arg foo~text done')
    markup = markuptools.Markup('foo text')

    assert editor.target == markup


def test_MarkupEditor_run_03():

    markup = markuptools.Markup('foo bar', markup_name='foo')
    editor = scf.editors.MarkupEditor(target=markup)
    editor.run(user_input='arg entirely~new~text name bar direction up done')

    assert editor.target == markuptools.Markup('entirely new text', direction='up', markup_name='bar')
