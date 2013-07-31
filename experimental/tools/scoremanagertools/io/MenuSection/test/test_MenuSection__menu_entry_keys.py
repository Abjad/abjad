# -*- encoding: utf-8 -*-
from experimental import *


def test_MenuSection__menu_entry_keys_01():
    r'''Menu entry keys equal none when menu entry menu_entries are strings.
    True whether menu_section is numbered or not.
    '''

    menu = scoremanagertools.io.Menu()
    menu.session.push_breadcrumb('location')
    menu_section = menu._make_section()
    menu_section.append('apple')
    menu_section.append('banana')
    menu_section.append('cherry')
    menu_section.title = 'section'
    assert not menu_section.is_numbered
    assert menu_section._menu_entry_keys == [None, None, None]

    menu = scoremanagertools.io.Menu()
    menu.session.push_breadcrumb('location')
    menu_section = menu._make_section(is_numbered=True)
    menu_section.append('apple')
    menu_section.append('banana')
    menu_section.append('cherry')
    menu_section.title = 'section'
    assert menu_section.is_numbered
    assert menu_section._menu_entry_keys == [None, None, None]


def test_MenuSection__menu_entry_keys_02():
    r'''Menu entry keys equal index 0 of menu entry 
    menu_entries when menu entry menu_entries are tuples.
    True whether menu_section is numbered or not.
    '''

    menu = scoremanagertools.io.Menu()
    menu.session.push_breadcrumb('location')
    menu_section = menu._make_section()
    menu_section.append(('add something', 'add'))
    menu_section.append(('delete something', 'rm'))
    menu_section.append(('modify something', 'mod'))
    menu_section.title = 'menu_section title'
    assert not menu_section.is_numbered
    assert menu_section._menu_entry_keys == \
        ['add', 'rm', 'mod']
    assert menu_section._menu_entry_keys == \
        [x.key for x in menu_section.menu_entries]

    menu = scoremanagertools.io.Menu()
    menu.session.push_breadcrumb('location')
    menu_section = menu._make_section(is_numbered=True)
    menu_section.append(('add something', 'add'))
    menu_section.append(('delete something', 'rm'))
    menu_section.append(('modify something', 'mod'))
    menu_section.title = 'menu_section title'
    assert menu_section.is_numbered
    assert menu_section._menu_entry_keys == \
        ['add', 'rm', 'mod']
    assert menu_section._menu_entry_keys == \
        [x.key for x in menu_section.menu_entries]
