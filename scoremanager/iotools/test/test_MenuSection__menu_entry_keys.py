# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MenuSection__menu_entry_keys_01():
    r'''Menu entry keys equal none when menu entry menu_entries are strings.
    True whether section is numbered or not.
    '''

    menu = scoremanager.iotools.Menu()
    menu._session._push_breadcrumb('location')
    section = menu._make_section(name='test', title='section')
    section.append('apple')
    section.append('banana')
    section.append('cherry')
    assert not section.is_numbered
    assert section._menu_entry_keys == [None, None, None]

    menu = scoremanager.iotools.Menu()
    menu._session._push_breadcrumb('location')
    section = menu._make_section(
        name='test', 
        is_numbered=True, 
        title='section',
        )
    section.append('apple')
    section.append('banana')
    section.append('cherry')
    assert section.is_numbered
    assert section._menu_entry_keys == [None, None, None]


def test_MenuSection__menu_entry_keys_02():
    r'''Menu entry keys equal index 0 of menu entry 
    menu_entries when menu entry menu_entries are tuples.
    True whether section is numbered or not.
    '''

    menu = scoremanager.iotools.Menu()
    menu._session._push_breadcrumb('location')
    section = menu._make_section(name='test', title='section title')
    section.append(('something - add', 'add'))
    section.append(('something - delete', 'rm'))
    section.append(('something - modify', 'mod'))
    assert not section.is_numbered
    assert section._menu_entry_keys == \
        ['add', 'rm', 'mod']
    assert section._menu_entry_keys == \
        [x.key for x in section.menu_entries]

    menu = scoremanager.iotools.Menu()
    menu._session._push_breadcrumb('location')
    section = menu._make_section(
        name='test', 
        is_numbered=True, 
        title='section title',
        )
    section.append(('something - add', 'add'))
    section.append(('something - delete', 'rm'))
    section.append(('something - modify', 'mod'))
    assert section.is_numbered
    assert section._menu_entry_keys == \
        ['add', 'rm', 'mod']
    assert section._menu_entry_keys == \
        [x.key for x in section.menu_entries]
