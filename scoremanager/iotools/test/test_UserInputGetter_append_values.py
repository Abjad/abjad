# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_UserInputGetter_append_values_01():

    getter = scoremanager.iotools.UserInputGetter()
    getter.append_integer('attribute')
    assert getter._run(pending_user_input='foo -99') == -99

    getter = scoremanager.iotools.UserInputGetter()
    getter.append_integer_in_range('attribute', 1, 10)
    assert getter._run(pending_user_input='foo -99 99 7') == 7

    getter = scoremanager.iotools.UserInputGetter()
    menu_section = scoremanager.iotools.MenuSection(
        name='test',
        is_numbered=True,
        )
    menu_entries = ['apple', 'banana', 'cherry', 'durian', 'endive', 'fennel']
    for menu_entry in menu_entries:
        menu_section.append(menu_entry)
    getter.append_menu_section_range('attribute', menu_section)
    result = [6, 5, 4, 1, 3]
    assert getter._run(pending_user_input='fen-dur, app, che') == result

    getter = scoremanager.iotools.UserInputGetter()
    getter.append_markup('attribute')
    assert getter._run(pending_user_input='foo') == markuptools.Markup('foo')

    getter = scoremanager.iotools.UserInputGetter()
    getter.append_named_pitch('attribute')
    assert getter._run(pending_user_input="cs'") == NamedPitch("cs'")

    getter = scoremanager.iotools.UserInputGetter()
    getter.append_string('attribute')
    assert getter._run(pending_user_input='None -99 99 1-4 foo') == 'foo'

    getter = scoremanager.iotools.UserInputGetter()
    getter.append_string_or_none('attribute')
    assert getter._run(pending_user_input='-99 99 1-4 None') is None
