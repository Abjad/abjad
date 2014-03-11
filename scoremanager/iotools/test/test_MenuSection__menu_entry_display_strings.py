# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MenuSection__menu_entry_display_strings_01():
    r'''Menu entry display_strings equal menu entry menu_entries 
    when menu entry menu_entries are strings.
    True whether section is numbered or not.
    '''

    menu = scoremanager.iotools.Menu()
    menu._session._push_breadcrumb('location')
    section = menu._make_section(name='test')
    section.append('apple')
    section.append('banana')
    section.append('cherry')
    section.title = 'section'
    assert not section.is_numbered
    assert section._menu_entry_display_strings == \
        ['apple', 'banana', 'cherry']

    menu = scoremanager.iotools.Menu()
    menu._session._push_breadcrumb('location')
    section = menu._make_section(name='test', is_numbered=True)
    section.append('apple')
    section.append('banana')
    section.append('cherry')
    section.title = 'section'
    assert section.is_numbered
    assert section._menu_entry_display_strings == \
        ['apple', 'banana', 'cherry']


def test_MenuSection__menu_entry_display_strings_02():
    r'''Menu entry display_strings equal index 1 of menu entry 
    menu_entries when menu entry menu_entries are tuples.
    True whether section is numbered or not.
    '''

    menu = scoremanager.iotools.Menu()
    menu._session._push_breadcrumb('location')
    section = menu._make_section(name='test')
    section.append(('add something', 'add'))
    section.append(('delete something', 'rm'))
    section.append(('modify something', 'mod'))
    section.title = 'section title'
    assert not section.is_numbered
    assert section._menu_entry_display_strings == \
        ['add something', 'delete something', 'modify something']
    assert section._menu_entry_display_strings == \
        [x.display_string for x in section.menu_entries]

    menu = scoremanager.iotools.Menu()
    menu._session._push_breadcrumb('location')
    section = menu._make_section(name='test', is_numbered=True)
    section.append(('add something', 'add'))
    section.append(('delete something', 'rm'))
    section.append(('modify something', 'mod'))
    section.title = 'section title'
    assert section.is_numbered
    assert section._menu_entry_display_strings == \
        ['add something', 'delete something', 'modify something']
    assert section._menu_entry_display_strings == \
        [x.display_string for x in section.menu_entries]
