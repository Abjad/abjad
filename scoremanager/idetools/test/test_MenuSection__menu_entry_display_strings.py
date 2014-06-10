# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
session = scoremanager.idetools.Session()


def test_MenuSection__menu_entry_display_strings_01():
    r'''Menu entry display_strings equal menu entry menu_entries
    when menu entry menu_entries are strings.
    True whether section is numbered or not.
    '''

    menu = scoremanager.idetools.Menu(session=session)
    commands = []
    commands.append('apple')
    commands.append('banana')
    commands.append('cherry')
    section = menu._make_section(
        menu_entries=commands,
        name='test', 
        title='section',
        )
    assert not section.is_numbered
    assert section._menu_entry_display_strings == \
        ['apple', 'banana', 'cherry']

    menu = scoremanager.idetools.Menu(session=session)
    commands = []
    commands.append('apple')
    commands.append('banana')
    commands.append('cherry')
    section = menu._make_section(
        is_numbered=True,
        menu_entries=commands,
        name='test',
        title='section',
        )
    assert section.is_numbered
    assert section._menu_entry_display_strings == \
        ['apple', 'banana', 'cherry']


def test_MenuSection__menu_entry_display_strings_02():
    r'''Menu entry display_strings equal index 1 of menu entry
    menu_entries when menu entry menu_entries are tuples.
    True whether section is numbered or not.
    '''

    menu = scoremanager.idetools.Menu(session=session)
    commands = []
    commands.append(('add something', 'add'))
    commands.append(('delete something', 'rm'))
    commands.append(('modify something', 'mod'))
    section = menu._make_section(
        menu_entries=commands,
        name='test', 
        title='section title',
        )
    assert not section.is_numbered
    assert section._menu_entry_display_strings == \
        ['add something', 'delete something', 'modify something']
    assert section._menu_entry_display_strings == \
        [x.display_string for x in section.menu_entries]

    menu = scoremanager.idetools.Menu(session=session)
    commands = []
    commands.append(('add something', 'add'))
    commands.append(('delete something', 'rm'))
    commands.append(('modify something', 'mod'))
    section = menu._make_section(
        is_numbered=True,
        menu_entries=commands,
        name='test',
        title='section title',
        )
    assert section.is_numbered
    assert section._menu_entry_display_strings == \
        ['add something', 'delete something', 'modify something']
    assert section._menu_entry_display_strings == \
        [x.display_string for x in section.menu_entries]