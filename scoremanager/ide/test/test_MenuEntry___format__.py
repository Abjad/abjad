# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
session = scoremanager.ide.Session()


def test_MenuEntry___format___01():
    r'''Formats menu section without raising exception.
    '''

    menu = scoremanager.ide.Menu(session=session)

    commands = []
    commands.append(('foo - add', 'add'))
    commands.append(('foo - delete', 'delete'))
    commands.append(('foo - modify', 'modify'))

    section = menu.make_command_section(
        commands=commands,
        name='test',
        )

    assert systemtools.TestManager.compare(
        format(section[0]),
        r'''
        ide.MenuEntry(
            display_string='foo - add',
            key='add',
            )
        '''
        )