from experimental import *


def test_MenuSection_has_string_tokens_01():

    menu = scoremanagementtools.menuing.Menu()
    section = menu.make_section()
    assert not section.has_string_tokens

    section  = menu.make_section()
    section.extend(['apple', 'banana', 'cherry'])
    assert section.has_string_tokens

    section  = menu.make_section()
    section.append(('add', 'first command'))
    section.append(('rm', 'second command'))
    section.append(('mod', 'third command'))
    assert not section.has_string_tokens
