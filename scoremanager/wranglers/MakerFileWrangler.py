# -*- encoding: utf-8 -*-
import os
from abjad.tools import sequencetools
from abjad.tools import stringtools
from scoremanager.wranglers.Wrangler import Wrangler


class MakerFileWrangler(Wrangler):
    r'''Maker module wrangler.

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
        self._asset_identifier = 'maker module'
        self._basic_breadcrumb = 'maker modules'
        self._human_readable = False
        self._include_extensions = True
        self._score_storehouse_path_infix_parts = ('makers',)
        self._user_storehouse_path = \
            self._configuration.user_library_makers_directory_path

    ### PRIVATE PROPERTIES ###

    @property
    def _input_to_action(self):
        superclass = super(MakerFileWrangler, self)
        result = superclass._input_to_action
        result = result.copy()
        result.update({
            'cp': self.copy_file,
            'new': self.make_py,
            'ren': self.rename_file,
            'rm': self.remove_files,
            })
        return result

    ### PRIVATE METHODS ###

    def _edit_maker_file(self, path):
        self._io_manager.edit(path)

    def _enter_run(self):
        self._session._is_navigating_to_score_maker_files = False

    def _handle_main_menu_result(self, result):
        if result in self._input_to_action:
            self._input_to_action[result]()
        elif result == 'user entered lone return':
            pass
        else:
            self._edit_maker_file(result)

    def _make_main_menu(self, name='make module wrangler'):
        superclass = super(MakerFileWrangler, self)
        menu = superclass._make_main_menu(name=name)
        self._make_pys_menu_section(menu)
        return menu

    def _make_pys_menu_section(self, menu):
        commands = []
        commands.append(('maker modules - copy', 'cp'))
        commands.append(('maker modules - new', 'new'))
        commands.append(('maker modules - rename', 'ren'))
        commands.append(('maker modules - remove', 'rm'))
        menu.make_command_section(
            commands=commands,
            name='maker modules',
            )

    ### PUBLIC METHODS ###

    def copy_file(self):
        r'''Copies maker module.

        Returns none.
        '''
        self._copy_asset(extension='.py', force_lowercase=False)

    def make_py(self):
        r'''Makes maker module.

        Returns none.
        '''
        self._make_file(
            extension='.py',
            force_lowercase=False,
            prompt_string='maker name', 
            )

    def remove_files(self):
        r'''Removes one or more maker modules.

        Returns none.
        '''
        self._remove_assets()

    def rename_file(self):
        r'''Renames make module.

        Returns none.
        '''
        self._rename_asset(
            extension='.py', 
            force_lowercase=False,
            )