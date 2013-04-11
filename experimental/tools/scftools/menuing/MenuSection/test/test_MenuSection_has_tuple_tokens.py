from experimental import *


def test_MenuSection_has_tuple_tokens_01():

    menu = scftools.menuing.Menu()
    section = menu.make_section()
    assert not section.has_tuple_tokens

    section  = menu.make_section()
    section.extend(['apple', 'banana', 'cherry'])
    assert not section.has_tuple_tokens

    section  = menu.make_section()
    section.append(('add', 'first command'))
    section.append(('rm', 'second command'))
    section.append(('mod', 'third command'))
    assert section.has_tuple_tokens
