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
        '_human_readable',
        '_include_extensions',
        )

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import managers
        superclass = super(StylesheetWrangler, self)
        superclass.__init__(session=session)
        self._abjad_storehouse_path = \
            self._configuration.abjad_stylesheets_directory_path
        self._asset_identifier = 'stylesheet'
        self._basic_breadcrumb = 'stylesheets'
        self._human_readable = False
        self._include_extensions = True
        self._score_storehouse_path_infix_parts = ('stylesheets',)
        self._user_storehouse_path = \
            self._configuration.user_library_stylesheets_directory_path

    ### PRIVATE PROPERTIES ###

    @property
    def _input_to_action(self):
        superclass = super(StylesheetWrangler, self)
        result = superclass._input_to_action
        result = result.copy()
        result.update({
            'cp': self.copy_stylesheet,
            'new': self.make_stylesheet,
            'ren': self.rename_stylesheet,
            'rm': self.remove_stylesheets,
            })
        return result

    ### PRIVATE METHODS ###

    def _enter_run(self):
        self._session._is_navigating_to_score_stylesheets = False

    @staticmethod
    def _file_name_callback(file_name):
        file_name = file_name.replace(' ', '-')
        file_name = file_name.replace('_', '-')
        return file_name

    def _handle_main_menu_result(self, result):
        if result in self._input_to_action:
            self._input_to_action[result]()
        elif result == 'user entered lone return':
            pass
        else:
            self.edit_stylesheet(result)

    def _is_valid_directory_entry(self, directory_entry):
        superclass = super(StylesheetWrangler, self)
        if superclass._is_valid_directory_entry(directory_entry):
            if directory_entry.endswith('.ily'):
                return True
        return False

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

    def copy_stylesheet(self):
        r'''Copies stylesheet.

        Returns none.
        '''
        self._copy_asset(
            extension='.ily',
            file_name_callback=self._file_name_callback,
            )

    def edit_stylesheet(self, path):
        r'''Edits stylesheet.

        Returns none.
        '''
        self._io_manager.edit(path)

    def make_stylesheet(self):
        r'''Makes stylesheet.

        Returns none.
        '''
        self._make_file(
            extension='.ily',
            file_name_callback=self._file_name_callback,
            prompt_string='stylesheet name', 
            )

    def remove_stylesheets(self):
        r'''Removes one or more stylesheets.

        Returns none.
        '''
        self._remove_assets()

    def rename_stylesheet(self):
        r'''Renames stylesheet.

        Returns none.
        '''
        self._rename_asset()