# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
session = scoremanager.idetools.Session()


def test_MenuSection___format___01():
    r'''Formats menu section without raising exception.
    '''

    menu = scoremanager.idetools.Menu(session=session)

    commands = []
    commands.append(('foo - add', 'add'))
    commands.append(('foo - delete', 'delete'))
    commands.append(('foo - modify', 'modify'))

    section = menu.make_command_section(
        commands=commands,
        name='test',
        )

    assert systemtools.TestManager.compare(
        format(section),
        r'''
        idetools.MenuSection(
            display_prepopulated_values=False,
            group_by_annotation=False,
            indent_level=1,
            is_alphabetized=True,
            is_asset_section=False,
            is_attribute_section=False,
            is_command_section=True,
            is_hidden=False,
            is_information_section=False,
            is_material_summary_section=False,
            is_navigation_section=False,
            is_numbered=False,
            is_ranged=False,
            match_on_display_string=False,
            menu_entries=[
                idetools.MenuEntry(
                    display_string='foo - add',
                    key='add',
                    ),
                idetools.MenuEntry(
                    display_string='foo - delete',
                    key='delete',
                    ),
                idetools.MenuEntry(
                    display_string='foo - modify',
                    key='modify',
                    ),
                ],
            name='test',
            return_value_attribute='key',
            )
        '''
        )