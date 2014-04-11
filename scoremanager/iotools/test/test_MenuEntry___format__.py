# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MenuEntry___format___01():
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

    assert systemtools.TestManager.compare(
        format(section[0]),
        r'''
        iotools.MenuEntry(
            'foo - add',
            key='add',
            )
        '''
        )