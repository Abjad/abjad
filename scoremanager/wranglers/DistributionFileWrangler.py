# -*- encoding: utf-8 -*-
import os
from abjad.tools import sequencetools
from abjad.tools import stringtools
from scoremanager.wranglers.Wrangler import Wrangler


class DistributionFileWrangler(Wrangler):
    r'''Distribution wrangler.

    ..  container:: example

        ::

            >>> session = scoremanager.core.Session()
            >>> wrangler = scoremanager.wranglers.DistributionFileWrangler(
            ...     session=session,
            ...     )
            >>> wrangler
            DistributionFileWrangler()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_include_extensions',
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import managers
        superclass = super(DistributionFileWrangler, self)
        superclass.__init__(session=session)
        self._abjad_storehouse_path = None
        self._user_storehouse_path = None
        self._score_storehouse_path_infix_parts = ('distribution',)
        self._include_extensions = True
        self._manager_class = managers.FileManager

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        if self._session.is_in_score:
            breadcrumb = 'distribution directory'
        else:
            breadcrumb = 'distribution file library'
        view_name = self._read_view_name()
        if view_name:
            breadcrumb = '{} ({} view)'.format(breadcrumb, view_name)
        return breadcrumb

    @property
    def _user_input_to_action(self):
        superclass = super(DistributionFileWrangler, self)
        result = superclass._user_input_to_action
        result = result.copy()
        result.update({
            })
        return result

    ### PRIVATE METHODS ###

    def _edit_file(self, path):
        manager = self._manager_class(
            path=path,
            session=self._session,
            )
        manager.edit()

    def _enter_run(self):
        self._session._is_navigating_to_score_distribution_files = False

    def _handle_main_menu_result(self, result):
        if result in self._user_input_to_action:
            self._user_input_to_action[result]()
        elif result == 'user entered lone return':
            pass
        else:
            self._edit_file(result)

    def _make_asset_menu_section(self, menu):
        include_annotation = not self._session.is_in_score
        menu_entries = self._make_asset_menu_entries(
            human_readable=False,
            include_annotation=include_annotation,
            include_extensions=True,
            )
        if not menu_entries:
            return
        section = menu.make_asset_section(
            menu_entries=menu_entries
            )
        menu._asset_section = section

    def _make_files_menu_section(self, menu):
        commands = []
        commands.append(('files - copy', 'cp'))
        commands.append(('files - new', 'new'))
        commands.append(('files - rename', 'ren'))
        commands.append(('files - remove', 'rm'))
        menu.make_command_section(
            commands=commands,
            name='files',
            )

    def _make_main_menu(self, name='distribution wrangler'):
        superclass = super(DistributionFileWrangler, self)
        menu = superclass._make_main_menu(name=name)
        self._make_files_menu_section(menu)
        return menu

    ### PUBLIC METHODS ###

    def remove_distribution_file(self):
        r'''Removes one or more distribution files.
        
        Returns none.
        '''
        self._remove_asset(
            item_identifier='distribution file',
            )

    def rename_distribution_file(self):
        r'''Renames distribution file.

        Returns none.
        '''
        self._rename_asset(
            item_identifier='distribution file',
            )