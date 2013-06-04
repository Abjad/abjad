from experimental import *


def test_MenuSection_menu_token_bodies_01():
    '''Menu entry bodies equal menu entry tokens when menu entry tokens are strings.
    True whether section is numbered or not.
    '''

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    tokens = ['apple', 'banana', 'cherry']
    section = menu.make_section(tokens=tokens)
    section.title = 'section'
    assert not section.is_numbered
    assert section.menu_token_bodies == ['apple', 'banana', 'cherry']

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    tokens = ['apple', 'banana', 'cherry']
    section = menu.make_section(is_numbered=True, tokens=tokens)
    section.title = 'section'
    assert section.is_numbered
    assert section.menu_token_bodies == ['apple', 'banana', 'cherry']


def test_MenuSection_menu_token_bodies_02():
    '''Menu entry bodies equal index 1 of menu entry tokens when menu entry tokens are tuples.
    True whether section is numbered or not.
    '''

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    tokens = [
        ('add', 'add something'),
        ('rm', 'delete something'),
        ('mod', 'modify something'),
        ]
    section = menu.make_section(tokens=tokens)
    section.title = 'section title'
    assert not section.is_numbered
    assert section.menu_token_bodies == ['add something', 'delete something', 'modify something']
    assert section.menu_token_bodies == [x[1] for x in section.tokens]

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    tokens = [
        ('add', 'add something'),
        ('rm', 'delete something'),
        ('mod', 'modify something'),
        ]
    section = menu.make_section(is_numbered=True, tokens=tokens)
    section.title = 'section title'
    assert section.is_numbered
    assert section.menu_token_bodies == ['add something', 'delete something', 'modify something']
    assert section.menu_token_bodies == [x[1] for x in section.tokens]
