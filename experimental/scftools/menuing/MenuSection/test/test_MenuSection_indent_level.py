import scftools


def test_MenuSection_indent_level_01():

    menu = scftools.menuing.Menu()
    menu.push_breadcrumb('location')
    section = menu.make_section()
    section.title = 'section'
    section.extend(['apple', 'banana', 'cherry'])

    assert section.indent_level == 1
