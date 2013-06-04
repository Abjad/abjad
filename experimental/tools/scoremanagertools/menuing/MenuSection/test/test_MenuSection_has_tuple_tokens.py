from experimental import *


def test_MenuSection_has_tuple_tokens_01():

    menu = scoremanagertools.menuing.Menu()
    section = menu.make_section()
    assert not section.has_tuple_tokens

    tokens = ['apple', 'banana', 'cherry']
    section = menu.make_section(tokens=tokens)
    assert not section.has_tuple_tokens

    tokens = [
        ('add', 'add something'),
        ('rm', 'delete something'),
        ('mod', 'modify something'),
        ]
    section = menu.make_section(tokens=tokens)
    assert section.has_tuple_tokens
