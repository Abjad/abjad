# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
session = scoremanager.idetools.Session()


def test_Getter_append_values_01():

    getter = scoremanager.idetools.Getter(session=session)
    getter.append_integer('attribute')
    input_ = 'foo -99'
    getter._session._pending_input = input_
    assert getter._run() == -99

    getter = scoremanager.idetools.Getter(session=session)
    getter.append_integer_in_range('attribute', 1, 10)
    input_ = 'foo -99 99 7'
    getter._session._pending_input = input_
    assert getter._run() == 7

    getter = scoremanager.idetools.Getter(session=session)
    menu_entries = ['apple', 'banana', 'cherry', 'durian', 'endive', 'fennel']
    section = scoremanager.idetools.MenuSection(
        is_numbered=True,
        menu_entries=menu_entries,
        name='test',
        )
    getter.append_menu_section_range('attribute', section)
    result = [6, 5, 4, 1, 3]
    input_ = 'fen-dur, app, che'
    getter._session._pending_input = input_
    assert getter._run() == result

    getter = scoremanager.idetools.Getter(session=session)
    getter.append_markup('attribute')
    input_ = 'foo'
    getter._session._pending_input = input_
    assert getter._run() == markuptools.Markup('foo')

    getter = scoremanager.idetools.Getter(session=session)
    getter.append_named_pitch('attribute')
    input_ = "cs'"
    getter._session._pending_input = input_
    assert getter._run() == NamedPitch("cs'")

    getter = scoremanager.idetools.Getter(session=session)
    getter.append_string('attribute')
    input_ = 'None -99 99 1-4 foo'
    getter._session._pending_input = input_
    assert getter._run() == 'foo'

    getter = scoremanager.idetools.Getter(session=session)
    getter.append_string_or_none('attribute')
    input_ = '-99 99 1-4 None'
    getter._session._pending_input = input_
    assert getter._run() is None