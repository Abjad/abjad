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
    def _manager_class(self):
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
            'ren': self.rename_stylesheet,
            'rm': self.remove_stylesheet,
            })
        return result

    ### PRIVATE METHODS ###

    def _edit_stylesheet(self):
        manager = self._manager_class(
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

    def _make_asset_menu_entries(
        self,
        apply_view=True,
        include_annotation=True,
        include_extensions=True,
        include_asset_name=True,
        include_year=False,
        human_readable=False,
        packages_instead_of_paths=False,
        sort_by_annotation=True,
        ):
        superclass = super(StylesheetWrangler, self)
        menu_entries = superclass._make_asset_menu_entries(
            apply_view=apply_view,
            include_annotation=include_annotation,
            include_extensions=include_extensions,
            include_asset_name=include_asset_name,
            include_year=include_year,
            human_readable=human_readable,
            packages_instead_of_paths=packages_instead_of_paths,
            sort_by_annotation=sort_by_annotation,
            )
        return menu_entries

    def _make_asset_menu_section(self, menu):
        include_annotation = not self._session.is_in_score
        menu_entries = self._make_asset_menu_entries(
            include_annotation=include_annotation,
            )
        if not menu_entries:
            return
        section = menu.make_asset_section(
            menu_entries=menu_entries,
            )
        menu._asset_section = section

    def _make_main_menu(self, name='stylesheet wrangler'):
        superclass = super(StylesheetWrangler, self)
        menu = superclass._make_main_menu(name=name)
        self._make_stylesheets_menu_section(menu)
        return menu

    def _make_stylesheets_menu_section(self, menu):
        commands = []
        commands.append(('stylesheets - copy', 'cp'))
        commands.append(('stylesheets - new', 'new'))
        commands.append(('stylesheets - rename', 'ren'))
        commands.append(('stylesheets - remove', 'rm'))
        menu.make_command_section(
            commands=commands,
            name='stylesheets',
            )

    ### PUBLIC METHODS ###

    def make_stylesheet(self):
        r'''Makes stylesheet.

        Returns none.
        '''
        def callback(file_name):
            file_name = file_name.replace(' ', '-')
            file_name = file_name.replace('_', '-')
            return file_name
        self._make_file(
            extension='.ily',
            file_name_callback=callback,
            prompt_string='stylesheet name', 
            )

    def remove_stylesheet(self):
        r'''Removes one or more stylesheets.

        Returns none.
        '''
        self._remove_asset(
            item_identifier='stylesheet', 
            )

    def rename_stylesheet(self):
        r'''Renames stylesheet.

        Returns none.
        '''
        self._rename_asset(
            item_identifier='stylesheet',
            )