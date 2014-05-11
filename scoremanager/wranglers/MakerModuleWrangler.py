# -*- encoding: utf-8 -*-
import os
from abjad.tools import sequencetools
from abjad.tools import stringtools
from scoremanager.wranglers.Wrangler import Wrangler


class MakerModuleWrangler(Wrangler):
    r'''Maker module wrangler.

    ..  container:: example

        ::

            >>> session = scoremanager.core.Session()
            >>> wrangler = scoremanager.wranglers.MakerModuleWrangler(
            ...     session=session,
            ...     )
            >>> wrangler
            MakerModuleWrangler()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_include_extensions',
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import managers
        superclass = super(MakerModuleWrangler, self)
        superclass.__init__(session=session)
        self._abjad_storehouse_path = None
        self._asset_identifier = 'maker module'
        self._basic_breadcrumb = 'maker modules'
        self._include_extensions = True
        self._score_storehouse_path_infix_parts = ('makers',)
        self._user_storehouse_path = \
            self._configuration.user_library_makers_directory_path

    ### PRIVATE PROPERTIES ###

    @property
    def _input_to_action(self):
        superclass = super(MakerModuleWrangler, self)
        result = superclass._input_to_action
        result = result.copy()
        result.update({
            'cp': self.copy_module,
            'new': self.make_module,
            'ren': self.rename_module,
            'rm': self.remove_modules,
            })
        return result

    ### PRIVATE METHODS ###

    def _edit_maker_module(self, path):
        self._io_manager.edit(path)

    def _enter_run(self):
        self._session._is_navigating_to_score_maker_modules = False

    def _handle_main_menu_result(self, result):
        if result in self._input_to_action:
            self._input_to_action[result]()
        elif result == 'user entered lone return':
            pass
        else:
            self._edit_maker_module(result)

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
            menu_entries=menu_entries,
            )

    def _make_main_menu(self, name='make module wrangler'):
        superclass = super(MakerModuleWrangler, self)
        menu = superclass._make_main_menu(name=name)
        self._make_modules_menu_section(menu)
        return menu

    def _make_modules_menu_section(self, menu):
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

    def copy_module(self):
        r'''Copies maker module.

        Returns none.
        '''
        self._copy_asset(extension='.py', force_lowercase=False)

    def make_module(self):
        r'''Makes maker module.

        Returns none.
        '''
        self._make_file(
            extension='.py',
            force_lowercase=False,
            prompt_string='maker name', 
            )

    def remove_modules(self):
        r'''Removes one or more maker modules.

        Returns none.
        '''
        self._remove_assets()

    def rename_module(self):
        r'''Renames make module.

        Returns none.
        '''
        self._rename_asset(
            extension='.py', 
            force_lowercase=False,
            )