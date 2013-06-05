from experimental import *


def test_Menu_menu_token_keys_01():

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    menu_tokens = ['apple', 'banana', 'cherry']
    section_1 = menu.make_section(menu_tokens=menu_tokens)
    section_1.title = 'section'
    menu_tokens = [
        ('add', 'add something'),
        ('rm', 'delete something'),
        ('mod', 'modify something'),
        ]
    section_2 = menu.make_section(menu_tokens=menu_tokens)
    assert menu.menu_token_keys[-6:] == section_1.menu_token_keys + section_2.menu_token_keys
