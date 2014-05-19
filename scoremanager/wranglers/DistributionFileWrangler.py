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
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import managers
        superclass = super(DistributionFileWrangler, self)
        superclass.__init__(session=session)
        self._abjad_storehouse_path = None
        self._asset_identifier = 'file'
        self._basic_breadcrumb = 'distribution files'
        self._include_extensions = True
        self._score_storehouse_path_infix_parts = ('distribution',)
        self._user_storehouse_path = None

    ### PRIVATE PROPERTIES ###

    @property
    def _input_to_method(self):
        superclass = super(DistributionFileWrangler, self)
        result = superclass._input_to_method
        result = result.copy()
        result.update({
            'cp': self.copy_file,
            'new': self.make_file,
            'ren': self.rename_file,
            'rm': self.remove_files,
            })
        return result

    ### PRIVATE METHODS ###

    def _edit_file(self, path):
        self._io_manager.edit(path)

    def _enter_run(self):
        self._session._is_navigating_to_score_distribution_files = False

    def _handle_main_menu_result(self, result):
        superclass = super(DistributionFileWrangler, self)
        if superclass._handle_main_menu_result(result):
            return True
        elif result in self._input_to_method:
            self._input_to_method[result]()
        elif result == 'user entered lone return':
            pass
        else:
            self._edit_file(result)

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

    def copy_file(self):
        r'''Copies distribution file.

        Returns none.
        '''
        self._copy_asset(force_lowercase=False)

    def make_file(self):
        r'''Makes empty file in distribution directory.

        Returns none.
        '''
        self._make_file(
            prompt_string='file name', 
            )

    def remove_files(self):
        r'''Removes one or more distribution files.
        
        Returns none.
        '''
        self._remove_assets()

    def rename_file(self):
        r'''Renames distribution file.

        Returns none.
        '''
        self._rename_asset()