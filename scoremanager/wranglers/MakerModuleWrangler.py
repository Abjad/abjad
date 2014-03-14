# -*- encoding: utf-8 -*-
import os
from abjad.tools import sequencetools
from abjad.tools import stringtools
from scoremanager.wranglers.Wrangler import Wrangler


class MakerModuleWrangler(Wrangler):
    r'''Maker file wrangler.

    ..  container:: example

        ::

            >>> session = scoremanager.core.Session()
            >>> wrangler = scoremanager.wranglers.MakerModuleWrangler(
            ...     session=session,
            ...     )
            >>> wrangler
            MakerModuleWrangler()

    '''

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import managers
        superclass = super(MakerModuleWrangler, self)
        superclass.__init__(session=session)
        self._asset_manager_class = managers.FileManager
        self._abjad_storehouse_path = None
        self._user_storehouse_path = \
            self._configuration.user_library_makers_directory_path
        self._score_storehouse_path_infix_parts = ('makers',)
        self._include_extensions = True

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        if self._session.is_in_score:
            return 'makers'
        else:
            return 'maker library'

    @property
    def _temporary_asset_name(self):
        return '__temporary_maker.py'

    @property
    def _user_input_to_action(self):
        superclass = super(MakerModuleWrangler, self)
        result = superclass._user_input_to_action
        result = result.copy()
        result.update({
            })
        return result

    ### PRIVATE METHODS ###

    def _edit_maker_module(
        self, 
        path,
        pending_user_input=None,
        ):
        self._io_manager._assign_user_input(pending_user_input)
        manager = self._asset_manager_class(
            path=path, 
            session=self._session,
            )
        manager.edit()

    def _get_current_directory(self):
        if self._session.current_score_directory_path:
            parts = (self._session.current_score_directory_path,)
            parts += self._score_storehouse_path_infix_parts
            return os.path.join(*parts)
    
    def _handle_main_menu_result(self, result):
        if result in self._user_input_to_action:
            self._user_input_to_action[result]()
        elif result == 'user entered lone return':
            pass
        else:
            self._edit_maker_module(result)

    def _make_asset_menu_section(self, menu):
        section = menu.make_asset_section()
        menu._asset_section = section
        menu_entries = self._make_asset_menu_entries(
            human_readable=False,
            include_annotation=False,
            include_extensions=True,
            )
        for menu_entry in menu_entries:
            section.append(menu_entry)
        return section

    def _make_main_menu(self):
        menu = self._io_manager.make_menu(where=self._where)
        self._main_menu = menu
        self._make_asset_menu_section(menu)
        self._make_maker_modules_menu_section(menu)
        return menu

    def _make_maker_modules_menu_section(self, menu):
        section = menu.make_command_section(name='maker modules')
        section.append(('maker modules - copy', 'cp'))
        section.append(('maker modules - new', 'new'))
        section.append(('maker modules - rename', 'ren'))
        section.append(('maker modules - remove', 'rm'))
        return section

    ### PUBLIC METHODS ###

    def make_asset(
        self,
        pending_user_input=None,
        ):
        r'''Makes asset.

        Returns none.
        '''
        from scoremanager import managers
        self._io_manager._assign_user_input(pending_user_input)
        with self._backtracking:
            # TODO: extend to allow creation in current score
            storehouse_path = self._select_storehouse_path(
                abjad_library=False,
                user_library=True,
                abjad_score_packages=False,
                user_score_packages=False,
                )
        if self._session._backtrack():
            return
        getter = self._io_manager.make_getter(where=self._where)
        getter.append_string('maker name')
        file_path = getter._run()
        if self._session._backtrack():
            return
        file_path = stringtools.string_to_accent_free_snake_case(file_path)
        if not file_path.endswith('.py'):
            file_path = file_path + '.py'
        file_path = os.path.join(storehouse_path, file_path)
        manager = managers.FileManager(
            file_path, 
            session=self._session,
            )
        if self._session.is_test:
            manager._make_empty_asset()
        else:
            manager.edit()
