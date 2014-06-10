# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
session = scoremanager.idetools.Session()


def test_MenuSection__menu_entry_return_values_01():

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
    assert section._menu_entry_return_values == \
        ['apple', 'banana', 'cherry']
    assert section._menu_entry_return_values == \
        section._menu_entry_display_strings

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
    assert section._menu_entry_return_values == \
        ['apple', 'banana', 'cherry']
    assert section._menu_entry_return_values == \
        section._menu_entry_display_strings

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
        return_value_attribute='display_string',
        )
    assert section.is_numbered
    assert section._menu_entry_return_values == \
        ['apple', 'banana', 'cherry']
    assert section._menu_entry_return_values == \
        section._menu_entry_display_strings

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

    menu = scoremanager.idetools.Menu(session=session)
    commands = []
    commands.append(('something - add', 'add'))
    commands.append(('something - delete', 'rm'))
    commands.append(('something - modify', 'mod'))
    section = menu._make_section(
        is_numbered=True,
        menu_entries=commands,
        name='test',
        return_value_attribute='key',
        title='section',
        )
    assert section.is_numbered
    values = ['add', 'rm', 'mod']
    assert section._menu_entry_return_values == values
    keys = section._menu_entry_keys
    assert section._menu_entry_return_values == keys

    menu = scoremanager.idetools.Menu(session=session)
    commands = []
    commands.append(('something - add', 'add'))
    commands.append(('something - delete', 'rm'))
    commands.append(('something - modify', 'mod'))
    section = menu._make_section(
        menu_entries=commands,
        name='test',
        return_value_attribute='key',
        title='section',
        )
    assert not section.is_numbered
    values = ['add', 'rm', 'mod']
    assert section._menu_entry_return_values == values
    keys = section._menu_entry_keys
    assert section._menu_entry_return_values == keys

    menu = scoremanager.idetools.Menu(session=session)
    commands = []
    commands.append(('something - add', 'add'))
    commands.append(('something - delete', 'rm'))
    commands.append(('something - modify', 'mod'))
    section = menu._make_section(
        is_numbered=True,
        menu_entries=commands,
        name='test',
        title='section',
        )
    assert section.is_numbered
    values = ['something - add', 'something - delete', 'something - modify']
    assert section._menu_entry_return_values == values
    strings = section._menu_entry_display_strings
    assert section._menu_entry_return_values == strings

    menu = scoremanager.idetools.Menu(session=session)
    commands = []
    commands.append(('something - add', 'add'))
    commands.append(('something - delete', 'rm'))
    commands.append(('something - modify', 'mod'))
    section = menu._make_section(
        menu_entries=commands,
        name='test', 
        title='section',
        )
    assert not section.is_numbered
    values = ['something - add', 'something - delete', 'something - modify']
    assert section._menu_entry_return_values == values
    strings = section._menu_entry_display_strings
    assert section._menu_entry_return_values == strings


def test_MenuSection__menu_entry_return_values_03():
    r'''Length-4 tuples include prepopulated return values.
    You must still set return_value_attribute to 'explicit'.
    '''

    menu = scoremanager.idetools.Menu(session=session)
    commands = []
    commands.append(('something - add', 'add', None, 'return value A'))
    commands.append(('something - delete', 'rm', None, 'return value B'))
    commands.append(('something - modify', 'mod', None, 'return value C'))
    section = menu._make_section(
        menu_entries=commands,
        name='test',
        return_value_attribute='explicit',
        title='section',
        )
    assert not section.is_numbered
    return_values = ['return value A', 'return value B', 'return value C']
    assert section._menu_entry_return_values == return_values