import scf


def test_Menu_menu_entry_bodies_01():

    menu = scf.menuing.Menu()
    menu.push_breadcrumb('location')
    section_1 = menu.make_section()
    section_1.title = 'section'
    section_1.extend(['apple', 'banana', 'cherry'])
    section_2 = menu.make_section()
    section_2.append(('add', 'add something'))
    section_2.append(('rm', 'delete something'))
    section_2.append(('mod', 'modify something'))
    assert menu.menu_entry_bodies[-6:] == section_1.menu_entry_bodies + section_2.menu_entry_bodies
