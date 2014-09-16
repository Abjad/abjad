# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Markup_autoedit_01():
    r'''Edits markup contents.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=Markup(),
        )
    input_ = 'arg foo~text done'
    autoeditor._session._pending_input = input_
    autoeditor._run()

    markup = markuptools.Markup('foo text')
    assert autoeditor.target == markup


def test_Markup_autoedit_02():
    r'''Edits markup contents and direction.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=Markup(),
        )
    input_ = '''arg '"foo~text~here"' dir up done'''
    autoeditor._session._pending_input = input_
    autoeditor._run()

    assert autoeditor.target == Markup('"foo text here"', direction=Up)


def test_Markup_autoedit_03():
    r'''Edits markup contents and direction.
    '''

    target = Markup('foo bar')
    session = scoremanager.idetools.Session(is_test=True)
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = 'arg entirely~new~text direction up done'
    autoeditor._session._pending_input = input_
    autoeditor._run()

    assert autoeditor.target == Markup('entirely new text', direction=Up)