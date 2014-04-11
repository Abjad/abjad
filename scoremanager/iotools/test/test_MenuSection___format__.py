# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MenuSection___format___01():
    r'''Formats menu section without raising exception.
    '''

    menu = scoremanager.iotools.Menu(
        include_default_hidden_sections=False,
        )

    commands = []
    commands.append(('foo - add', 'add'))
    commands.append(('foo - delete', 'delete'))
    commands.append(('foo - modify', 'modify'))

    section = menu.make_command_section(
        menu_entries=commands,
        name='test',
        )

    string = format(section)

    assert 'is_numbered=False,' in string
    assert 'is_ranged=False,' in string
    assert 'display_prepopulated_values=False,' in string
    assert 'match_on_display_string=False,' in string