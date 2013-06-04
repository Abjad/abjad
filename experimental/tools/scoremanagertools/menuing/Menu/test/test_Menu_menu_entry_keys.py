from experimental import *


def test_Menu_menu_entry_keys_01():

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    tokens = ['apple', 'banana', 'cherry']
    section_1 = menu.make_section(tokens=tokens)
    section_1.title = 'section'
    tokens = [
        ('add', 'add something'),
        ('rm', 'delete something'),
        ('mod', 'modify something'),
        ]
    section_2 = menu.make_section(tokens=tokens)
    assert menu.menu_entry_keys[-6:] == section_1.menu_entry_keys + section_2.menu_entry_keys
