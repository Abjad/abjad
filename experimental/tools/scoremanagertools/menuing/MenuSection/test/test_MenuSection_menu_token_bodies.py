from experimental import *


def test_MenuSection_menu_token_bodies_01():
    '''Menu entry bodies equal menu entry menu_tokens when menu entry menu_tokens are strings.
    True whether menu_section is numbered or not.
    '''

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_tokens = ['apple', 'banana', 'cherry']
    menu_section = menu.make_section(menu_tokens=menu_tokens)
    menu_section.title = 'section'
    assert not menu_section.is_numbered
    assert menu_section.menu_token_bodies == ['apple', 'banana', 'cherry']

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_tokens = ['apple', 'banana', 'cherry']
    menu_section = menu.make_section(is_numbered=True, menu_tokens=menu_tokens)
    menu_section.title = 'section'
    assert menu_section.is_numbered
    assert menu_section.menu_token_bodies == ['apple', 'banana', 'cherry']


def test_MenuSection_menu_token_bodies_02():
    '''Menu entry bodies equal index 1 of menu entry menu_tokens when menu entry menu_tokens are tuples.
    True whether menu_section is numbered or not.
    '''

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_tokens = [
        ('add', 'add something'),
        ('rm', 'delete something'),
        ('mod', 'modify something'),
        ]
    menu_section = menu.make_section(menu_tokens=menu_tokens)
    menu_section.title = 'menu_section title'
    assert not menu_section.is_numbered
    assert menu_section.menu_token_bodies == ['add something', 'delete something', 'modify something']
    assert menu_section.menu_token_bodies == [x.display_string for x in menu_section.menu_tokens]

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_tokens = [
        ('add', 'add something'),
        ('rm', 'delete something'),
        ('mod', 'modify something'),
        ]
    menu_section = menu.make_section(is_numbered=True, menu_tokens=menu_tokens)
    menu_section.title = 'menu_section title'
    assert menu_section.is_numbered
    assert menu_section.menu_token_bodies == ['add something', 'delete something', 'modify something']
    assert menu_section.menu_token_bodies == [x.display_string for x in menu_section.menu_tokens]
