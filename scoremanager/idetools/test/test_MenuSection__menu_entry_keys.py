# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
session = scoremanager.idetools.Session()


def test_MenuSection__menu_entry_keys_01():
    r'''Menu entry keys equal none when menu entry menu_entries are strings.
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
    assert section._menu_entry_keys == [None, None, None]

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
    assert section._menu_entry_keys == [None, None, None]


def test_MenuSection__menu_entry_keys_02():
    r'''Menu entry keys equal index 0 of menu entry
    menu_entries when menu entry menu_entries are tuples.
    True whether section is numbered or not.
    '''

    menu = scoremanager.idetools.Menu(session=session)
    commands = []
    commands.append(('something - add', 'add'))
    commands.append(('something - delete', 'rm'))
    commands.append(('something - modify', 'mod'))
    section = menu._make_section(
        menu_entries=commands,
        name='test', 
        title='section title',
        )
    assert not section.is_numbered
    assert section._menu_entry_keys == ['add', 'rm', 'mod']
    assert section._menu_entry_keys == [_.key for _ in section.menu_entries]

    menu = scoremanager.idetools.Menu(session=session)
    commands = []
    commands.append(('something - add', 'add'))
    commands.append(('something - delete', 'rm'))
    commands.append(('something - modify', 'mod'))
    section = menu._make_section(
        is_numbered=True,
        menu_entries=commands,
        name='test',
        title='section title',
        )
    assert section.is_numbered
    keys = ['add', 'rm', 'mod']
    assert section._menu_entry_keys == keys
    keys = [_.key for _ in section.menu_entries]
    assert section._menu_entry_keys == keys