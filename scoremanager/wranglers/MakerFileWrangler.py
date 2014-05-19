# -*- encoding: utf-8 -*-
import os
from abjad.tools import sequencetools
from abjad.tools import stringtools
from scoremanager.wranglers.Wrangler import Wrangler


class MakerFileWrangler(Wrangler):
    r'''Maker file wrangler.

    ..  container:: example

        ::

            >>> session = scoremanager.core.Session()
            >>> wrangler = scoremanager.wranglers.MakerFileWrangler(
            ...     session=session,
            ...     )
            >>> wrangler
            MakerFileWrangler()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import managers
        superclass = super(MakerFileWrangler, self)
        superclass.__init__(session=session)
        self._abjad_storehouse_path = None
        self._asset_identifier = 'maker file'
        self._basic_breadcrumb = 'maker files'
        self._human_readable = False
        self._include_extensions = True
        self._score_storehouse_path_infix_parts = ('makers',)
        self._user_storehouse_path = \
            self._configuration.user_library_makers_directory_path

    ### PRIVATE PROPERTIES ###

    @property
    def _input_to_method(self):
        superclass = super(MakerFileWrangler, self)
        result = superclass._input_to_method
        result = result.copy()
        result.update({
            'cp': self.copy_file,
            'new': self.make_py,
            'ren': self.rename_file,
            'rm': self.remove_files,
            })
        return result

    ### PRIVATE METHODS ###

    def _enter_run(self):
        self._session._is_navigating_to_score_maker_files = False

    def _handle_main_menu_result(self, result):
        superclass = super(MakerFileWrangler, self)
        if superclass._handle_main_menu_result(result):
            return True
        elif result in self._input_to_method:
            self._input_to_method[result]()
        else:
            self._io_manager.open_file(result)

    def _make_main_menu(self, name='make py wrangler'):
        superclass = super(MakerFileWrangler, self)
        menu = superclass._make_main_menu(name=name)
        self._make_pys_menu_section(menu)
        return menu

    def _make_pys_menu_section(self, menu):
        commands = []
        commands.append(('maker files - copy', 'cp'))
        commands.append(('maker files - new', 'new'))
        commands.append(('maker files - rename', 'ren'))
        commands.append(('maker files - remove', 'rm'))
        menu.make_command_section(
            commands=commands,
            name='maker files',
            )

    ### PUBLIC METHODS ###

    def copy_file(self):
        r'''Copies maker file.

        Returns none.
        '''
        self._copy_asset(extension='.py', force_lowercase=False)

    def make_py(self):
        r'''Makes maker file.

        Returns none.
        '''
        self._make_file(
            extension='.py',
            force_lowercase=False,
            prompt_string='maker name', 
            )

    def remove_files(self):
        r'''Removes one or more maker files.

        Returns none.
        '''
        self._remove_assets()

    def rename_file(self):
        r'''Renames make py.

        Returns none.
        '''
        self._rename_asset(
            extension='.py', 
            force_lowercase=False,
            )