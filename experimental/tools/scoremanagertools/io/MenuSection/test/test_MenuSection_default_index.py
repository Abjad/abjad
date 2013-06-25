from experimental import *
import py


def test_MenuSection_default_index_01():

    menu = scoremanagertools.io.Menu()
    menu._session.push_breadcrumb('location')
    menu_section = menu._make_section()
    menu_section.title = 'section'
    menu_section.append('apple')
    menu_section.append('banana')
    menu_section.append('cherry')

    assert menu_section.default_index is None
    assert py.test.raises(ValueError, 'menu_section.default_index = -1')
    assert py.test.raises(ValueError, 'menu_section.default_index = 99')

    menu_section.default_index = 2
    assert menu_section.default_index == 2
