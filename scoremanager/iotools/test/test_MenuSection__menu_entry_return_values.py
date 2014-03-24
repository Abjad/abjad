# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MenuSection__menu_entry_return_values_01():

    menu = scoremanager.iotools.Menu()
    section = menu._make_section(
        name='test', 
        is_numbered=True, 
        title='section',
        )
    section.append('apple')
    section.append('banana')
    section.append('cherry')
    assert section.is_numbered
    assert section._menu_entry_return_values == \
        ['apple', 'banana', 'cherry']
    assert section._menu_entry_return_values == \
        section._menu_entry_display_strings

    menu = scoremanager.iotools.Menu()
    section = menu._make_section(name='test', title='section')
    section.append('apple')
    section.append('banana')
    section.append('cherry')
    assert not section.is_numbered
    assert section._menu_entry_return_values == \
        ['apple', 'banana', 'cherry']
    assert section._menu_entry_return_values == \
        section._menu_entry_display_strings

    menu = scoremanager.iotools.Menu()
    section = menu._make_section(
        name='test', 
        title='section',
        return_value_attribute='display_string',
        is_numbered=True,
        )
    section.append('apple')
    section.append('banana')
    section.append('cherry')
    assert section.is_numbered
    assert section._menu_entry_return_values == \
        ['apple', 'banana', 'cherry']
    assert section._menu_entry_return_values == \
        section._menu_entry_display_strings

    menu = scoremanager.iotools.Menu()
    section = menu._make_section(name='test', title='section')
    section.append('apple')
    section.append('banana')
    section.append('cherry')
    assert not section.is_numbered
    assert section._menu_entry_return_values == \
        ['apple', 'banana', 'cherry']
    assert section._menu_entry_return_values == \
        section._menu_entry_display_strings


def test_MenuSection__menu_entry_return_values_02():
    r'''Menu entry return values vary when menu entry 
    menu_entries are tuples.
    You can explicitly demand a return value equal 
    either to the menu entry key or display_string.
    Note that section numbering plays no role in this.
    '''

    menu = scoremanager.iotools.Menu()
    section = menu._make_section(
        name='test', 
        title='section',
        return_value_attribute='key',
        is_numbered=True,
        )
    section.append(('something - add', 'add'))
    section.append(('something - delete', 'rm'))
    section.append(('something - modify', 'mod'))
    assert section.is_numbered
    assert section._menu_entry_return_values == ['add', 'rm', 'mod']
    assert section._menu_entry_return_values == \
        section._menu_entry_keys

    menu = scoremanager.iotools.Menu()
    section = menu._make_section(
        name='test', 
        title='section',
        return_value_attribute='key',
        )
    section.append(('something - add', 'add'))
    section.append(('something - delete', 'rm'))
    section.append(('something - modify', 'mod'))
    assert not section.is_numbered
    assert section._menu_entry_return_values == \
        ['add', 'rm', 'mod']
    assert section._menu_entry_return_values == \
        section._menu_entry_keys

    menu = scoremanager.iotools.Menu()
    section = menu._make_section(
        name='test', 
        is_numbered=True, 
        title='section',
        )
    section.append(('something - add', 'add'))
    section.append(('something - delete', 'rm'))
    section.append(('something - modify', 'mod'))
    assert section.is_numbered
    assert section._menu_entry_return_values == \
        ['something - add', 'something - delete', 'something - modify']
    assert section._menu_entry_return_values == \
        section._menu_entry_display_strings

    menu = scoremanager.iotools.Menu()
    section = menu._make_section(name='test', title='section')
    section.append(('something - add', 'add'))
    section.append(('something - delete', 'rm'))
    section.append(('something - modify', 'mod'))
    assert not section.is_numbered
    assert section._menu_entry_return_values == \
        ['something - add', 'something - delete', 'something - modify']
    assert section._menu_entry_return_values == \
        section._menu_entry_display_strings


def test_MenuSection__menu_entry_return_values_03():
    r'''Length-4 tuples include prepopulated return values.
    You must still set return_value_attribute to 'explicit'.
    '''

    menu = scoremanager.iotools.Menu()
    section = menu._make_section(
        name='test', 
        title='section',
        return_value_attribute='explicit',
        )
    section.append(('something - add', 'add', None, 'return value A'))
    section.append(('something - delete', 'rm', None, 'return value B'))
    section.append(('something - modify', 'mod', None, 'return value C'))
    assert not section.is_numbered
    assert section._menu_entry_return_values == \
        ['return value A', 'return value B', 'return value C']