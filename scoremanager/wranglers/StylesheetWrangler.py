# -*- encoding: utf-8 -*-
import os
from abjad.tools import sequencetools
from abjad.tools import stringtools
from scoremanager.wranglers.Wrangler import Wrangler


class StylesheetWrangler(Wrangler):
    r'''Stylesheet wrangler.

    ..  container:: example

        ::

            >>> session = scoremanager.core.Session()
            >>> wrangler = scoremanager.wranglers.StylesheetWrangler(
            ...     session=session,
            ...     )
            >>> wrangler
            StylesheetWrangler()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_include_extensions',
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        superclass = super(StylesheetWrangler, self)
        superclass.__init__(session=session)
        self._abjad_storehouse_path = \
            self._configuration.abjad_stylesheets_directory_path
        self._user_storehouse_path = \
            self._configuration.user_library_stylesheets_directory_path
        self._score_storehouse_path_infix_parts = ('stylesheets',)
        self._include_extensions = True

    ### PRIVATE PROPERTIES ###

    @property
    def _asset_manager_class(self):
        from scoremanager import managers
        return managers.FileManager

    @property
    def _breadcrumb(self):
        if self._session.is_in_score:
            return 'stylesheets'
        else:
            return 'stylesheet library'

    @property
    def _user_input_to_action(self):
        superclass = super(StylesheetWrangler, self)
        result = superclass._user_input_to_action
        result = result.copy()
        result.update({
            'new': self.make_stylesheet,
            })
        return result

    ### PRIVATE METHODS ###

    def _edit_stylesheet(self):
        manager = self._asset_manager_class(
            path=path,
            session=self._session,
            )
        manager.edit()

    def _enter_run(self):
        self._session._is_navigating_to_score_stylesheets = False

    def _handle_main_menu_result(self, result):
        if result in self._user_input_to_action:
            self._user_input_to_action[result]()
        elif result == 'user entered lone return':
            pass
        else:
            self._edit_stylesheet(result)

    def _is_valid_directory_entry(self, directory_entry):
        superclass = super(StylesheetWrangler, self)
        if superclass._is_valid_directory_entry(directory_entry):
            if directory_entry.endswith('.ily'):
                return True
        return False

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
        menu._asset_section = section

    def _make_main_menu(self, name='stylesheet wrangler'):
        menu = self._io_manager.make_menu(name=name)
        self._main_menu = menu
        self._make_asset_menu_section(menu)
        self._make_stylesheets_menu_section(menu)
        return menu

    def _make_stylesheets_menu_section(self, menu):
        commands = []
        commands.append(('stylesheets - copy', 'cp'))
        commands.append(('stylesheets - new', 'new'))
        commands.append(('stylesheets - rename', 'ren'))
        commands.append(('stylesheets - remove', 'rm'))
        section = menu.make_command_section(
            menu_entries=commands,
            name='stylesheets',
            )

    ### PUBLIC METHODS ###

    def make_stylesheet(self):
        r'''Makes stylesheet.

        Returns none.
        '''
        from scoremanager import managers
        with self._controller_context:
            # TODO: extend to allow creation in current score
            storehouse_path = self._select_storehouse_path(
                abjad_library=False,
                user_library=True,
                abjad_score_packages=False,
                user_score_packages=False,
                )
            if self._should_backtrack():
                return
        getter = self._io_manager.make_getter()
        getter.append_string('stylesheet name')
        file_path = getter._run()
        if self._should_backtrack():
            return
        file_path = stringtools.string_to_accent_free_snake_case(file_path)
        if not file_path.endswith('.ily'):
            file_path = file_path + '.ily'
        file_path = os.path.join(storehouse_path, file_path)
        manager = managers.FileManager(
            file_path,
            session=self._session,
            )
        if self._session.is_test:
            manager._make_empty_asset()
        else:
            manager.edit()