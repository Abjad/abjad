# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MenuSection__menu_entry_return_values_01():

    menu = scoremanager.iotools.Menu()
    menu.session._push_breadcrumb('location')
    menu_section = menu._make_section(is_numbered=True)
    menu_section.append('apple')
    menu_section.append('banana')
    menu_section.append('cherry')
    menu_section.title = 'section'
    assert menu_section.is_numbered
    assert menu_section._menu_entry_return_values == \
        ['apple', 'banana', 'cherry']
    assert menu_section._menu_entry_return_values == \
        menu_section._menu_entry_display_strings

    menu = scoremanager.iotools.Menu()
    menu.session._push_breadcrumb('location')
    menu_section = menu._make_section()
    menu_section.append('apple')
    menu_section.append('banana')
    menu_section.append('cherry')
    menu_section.title = 'section'
    assert not menu_section.is_numbered
    assert menu_section._menu_entry_return_values == \
        ['apple', 'banana', 'cherry']
    assert menu_section._menu_entry_return_values == \
        menu_section._menu_entry_display_strings

    menu = scoremanager.iotools.Menu()
    menu.session._push_breadcrumb('location')
    menu_section = menu._make_section()
    menu_section.return_value_attribute = 'display_string'
    menu_section.is_numbered = True
    menu_section.append('apple')
    menu_section.append('banana')
    menu_section.append('cherry')
    menu_section.title = 'section'
    assert menu_section.is_numbered
    assert menu_section._menu_entry_return_values == \
        ['apple', 'banana', 'cherry']
    assert menu_section._menu_entry_return_values == \
        menu_section._menu_entry_display_strings

    menu = scoremanager.iotools.Menu()
    menu.session._push_breadcrumb('location')
    menu_section = menu._make_section()
    menu_section.append('apple')
    menu_section.append('banana')
    menu_section.append('cherry')
    menu_section.title = 'section'
    assert not menu_section.is_numbered
    assert menu_section._menu_entry_return_values == \
        ['apple', 'banana', 'cherry']
    assert menu_section._menu_entry_return_values == \
        menu_section._menu_entry_display_strings


def test_MenuSection__menu_entry_return_values_02():
    r'''Menu entry return values vary when menu entry 
    menu_entries are tuples.
    You can explicitly demand a return value equal 
    either to the menu entry key or display_string.
    Note that menu_section numbering plays no role in this.
    '''

    menu = scoremanager.iotools.Menu()
    menu.session._push_breadcrumb('location')
    menu_section = menu._make_section()
    menu_section.return_value_attribute = 'key'
    menu_section.is_numbered = True
    menu_section.append(('add something', 'add'))
    menu_section.append(('delete something', 'rm'))
    menu_section.append(('modify something', 'mod'))
    menu_section.title = 'section'
    assert menu_section.is_numbered
    assert menu_section._menu_entry_return_values == ['add', 'rm', 'mod']
    assert menu_section._menu_entry_return_values == \
        menu_section._menu_entry_keys

    menu = scoremanager.iotools.Menu()
    menu.session._push_breadcrumb('location')
    menu_section = menu._make_section()
    menu_section.return_value_attribute = 'key'
    menu_section.append(('add something', 'add'))
    menu_section.append(('delete something', 'rm'))
    menu_section.append(('modify something', 'mod'))
    menu_section.title = 'section'
    assert not menu_section.is_numbered
    assert menu_section._menu_entry_return_values == \
        ['add', 'rm', 'mod']
    assert menu_section._menu_entry_return_values == \
        menu_section._menu_entry_keys

    menu = scoremanager.iotools.Menu()
    menu.session._push_breadcrumb('location')
    menu_section = menu._make_section(is_numbered=True)
    menu_section.append(('add something', 'add'))
    menu_section.append(('delete something', 'rm'))
    menu_section.append(('modify something', 'mod'))
    menu_section.title = 'section'
    assert menu_section.is_numbered
    assert menu_section._menu_entry_return_values == \
        ['add something', 'delete something', 'modify something']
    assert menu_section._menu_entry_return_values == \
        menu_section._menu_entry_display_strings

    menu = scoremanager.iotools.Menu()
    menu.session._push_breadcrumb('location')
    menu_section = menu._make_section()
    menu_section.append(('add something', 'add'))
    menu_section.append(('delete something', 'rm'))
    menu_section.append(('modify something', 'mod'))
    menu_section.title = 'section'
    assert not menu_section.is_numbered
    assert menu_section._menu_entry_return_values == \
        ['add something', 'delete something', 'modify something']
    assert menu_section._menu_entry_return_values == \
        menu_section._menu_entry_display_strings


def test_MenuSection__menu_entry_return_values_03():
    r'''Length-4 tuples include prepopulated return values.
    You must still set return_value_attribute to 'explicit'.
    '''

    menu = scoremanager.iotools.Menu()
    menu.session._push_breadcrumb('location')
    menu_section = menu._make_section()
    menu_section.return_value_attribute = 'explicit'
    menu_section.append(('add something', 'add', None, 'return value A'))
    menu_section.append(('delete something', 'rm', None, 'return value B'))
    menu_section.append(('modify something', 'mod', None, 'return value C'))
    menu_section.title = 'section'
    assert not menu_section.is_numbered
    assert menu_section._menu_entry_return_values == \
        ['return value A', 'return value B', 'return value C']
