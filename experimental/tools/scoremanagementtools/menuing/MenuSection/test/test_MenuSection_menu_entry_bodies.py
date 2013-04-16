from experimental import *


def test_MenuSection_menu_entry_bodies_01():
    '''Menu entry bodies equal menu entry tokens when menu entry tokens are strings.
    True whether section is numbered or not.
    '''

    menu = scoremanagementtools.menuing.Menu()
    menu.push_breadcrumb('location')
    section = menu.make_section()
    section.title = 'section'
    section.extend(['apple', 'banana', 'cherry'])
    assert not section.is_numbered
    assert section.menu_entry_bodies == ['apple', 'banana', 'cherry']
    assert section.menu_entry_bodies == section.tokens

    menu = scoremanagementtools.menuing.Menu()
    menu.push_breadcrumb('location')
    section = menu.make_section(is_numbered=True)
    section.title = 'section'
    section.extend(['apple', 'banana', 'cherry'])
    assert section.is_numbered
    assert section.menu_entry_bodies == ['apple', 'banana', 'cherry']
    assert section.menu_entry_bodies == section.tokens


def test_MenuSection_menu_entry_bodies_02():
    '''Menu entry bodies equal index 1 of menu entry tokens when menu entry tokens are tuples.
    True whether section is numbered or not.
    '''

    menu = scoremanagementtools.menuing.Menu()
    menu.push_breadcrumb('location')
    section = menu.make_section()
    section.title = 'section title'
    section.append(('add', 'add something'))
    section.append(('rm', 'delete something'))
    section.append(('mod', 'modify something'))
    assert not section.is_numbered
    assert section.menu_entry_bodies == ['add something', 'delete something', 'modify something']
    assert section.menu_entry_bodies == [x[1] for x in section.tokens]

    menu = scoremanagementtools.menuing.Menu()
    menu.push_breadcrumb('location')
    section = menu.make_section(is_numbered=True)
    section.title = 'section title'
    section.append(('add', 'add something'))
    section.append(('rm', 'delete something'))
    section.append(('mod', 'modify something'))
    assert section.is_numbered
    assert section.menu_entry_bodies == ['add something', 'delete something', 'modify something']
    assert section.menu_entry_bodies == [x[1] for x in section.tokens]
