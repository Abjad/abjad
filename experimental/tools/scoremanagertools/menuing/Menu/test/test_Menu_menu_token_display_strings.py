from experimental import *


def test_Menu_menu_token_display_strings_01():

    menu = scoremanagertools.menuing.Menu()
    menu._session.push_breadcrumb('location')
    section_1 = menu.make_section()
    section_1.append('apple')
    section_1.append('banana')
    section_1.append('cherry')
    section_1.title = 'section'

    section_2 = menu.make_section()
    section_2.append(('add something', 'add'))
    section_2.append(('delete something', 'rm'))
    section_2.append(('modify something', 'mod'))
    assert menu.menu_entry_display_strings[-6:] == \
        section_1._menu_entry_display_strings + \
        section_2._menu_entry_display_strings
