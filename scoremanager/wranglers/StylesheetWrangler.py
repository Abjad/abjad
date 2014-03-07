# -*- encoding: utf-8 -*-
import os
from abjad.tools import sequencetools
from abjad.tools import stringtools
from scoremanager.wranglers.Wrangler import Wrangler


class StylesheetWrangler(Wrangler):
    r'''Stylesheet file wrangler.

    ..  container:: example

        ::

            >>> wrangler = scoremanager.wranglers.StylesheetWrangler()
            >>> wrangler
            StylesheetWrangler()

    '''

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import managers
        superclass = super(StylesheetWrangler, self)
        superclass.__init__(session=session)
        self._asset_manager_class = managers.FileManager
        self.abjad_storehouse_path = \
            self._configuration.abjad_stylesheets_directory_path
        self.user_storehouse_path = \
            self._configuration.user_library_stylesheets_directory_path
        self.score_storehouse_path_infix_parts = ('stylesheets',)

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        if self._session.is_in_score:
            return 'stylesheets'
        else:
            return 'stylesheet library'

    @property
    def _temporary_asset_name(self):
        return '__temporary_stylesheet.ily'

    @property
    def _user_input_to_action(self):
        superclass = super(StylesheetWrangler, self)
        _user_input_to_action = superclass._user_input_to_action
        _user_input_to_action = _user_input_to_action.copy()
        _user_input_to_action.update({
            'hse': self.edit_header_stylesheet,
            'lse': self.edit_layout_stylesheet,
            'pse': self.edit_paper_stylesheet,
            'new': self.make_asset,
            })
        return _user_input_to_action

    ### PRIVATE METHODS ###

    def _edit_stylesheet(
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

    def _path_to_annotation(self, path):
        from scoremanager import managers
        annotation = None
        if path.startswith(
            self._configuration.abjad_score_packages_directory_path) or \
            path.startswith(
            self._configuration.user_score_packages_directory_path):
            tmp = os.path.join('stylesheets')
            score_path = path.rpartition(tmp)[0]
            score_package_manager = managers.ScorePackageManager(
                path=score_path)
            annotation = score_package_manager._get_title()
        elif path.startswith(
            self._configuration.abjad_stylesheets_directory_path):
            annotation = 'Abjad'
        elif path.startswith(
            self._configuration.user_library_stylesheets_directory_path):
            annotation = self._configuration.composer_last_name
        return annotation

    def _get_current_directory(self):
        if self._session.current_score_directory_path:
            parts = (self._session.current_score_directory_path,)
            parts += self.score_storehouse_path_infix_parts
            return os.path.join(*parts)
    
    def _get_header_stylesheet_file_path(self):
        for directory_entry in sorted(os.listdir(
            self._get_current_directory())):
            if directory_entry.endswith('header.ily'):
                file_path = os.path.join(
                    self._get_current_directory(),
                    directory_entry,
                    )
                return file_path
    
    def _get_layout_stylesheet_file_path(self):
        for directory_entry in sorted(os.listdir(
            self._get_current_directory())):
            if directory_entry.endswith('layout.ily'):
                file_path = os.path.join(
                    self._get_current_directory(),
                    directory_entry,
                    )
                return file_path
    
    def _get_paper_stylesheet_file_path(self):
        for directory_entry in sorted(os.listdir(
            self._get_current_directory())):
            if directory_entry.endswith('paper.ily'):
                file_path = os.path.join(
                    self._get_current_directory(),
                    directory_entry,
                    )
                return file_path
    
    def _handle_main_menu_result(self, result):
        if result in self._user_input_to_action:
            self._user_input_to_action[result]()
        else:
            self._edit_stylesheet(result)

    def _is_valid_directory_entry(self, directory_entry):
        superclass = super(StylesheetWrangler, self)
        if superclass._is_valid_directory_entry(directory_entry):
            if directory_entry.endswith('.ily'):
                return True
        return False

    def _list_asset_paths(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset filesystem paths.

        Lists abjad stylesheet filesystem paths:

        ::

            >>> for x in wrangler._list_asset_paths(
            ...     user_library=False, 
            ...     user_score_packages=False,
            ...     ):
            ...     x
            '.../abjad/stylesheets/clean-letter-14.ily'
            '.../abjad/stylesheets/clean-letter-16.ily'
            '.../abjad/stylesheets/rhythm-letter-16.ily'
            '.../red_example_score/stylesheets/red-example-score-stylesheet.ily'

        Returns list.
        '''
        superclass = super(StylesheetWrangler, self)
        return superclass._list_asset_paths(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            head=head,
            )

    def _list_asset_managers(
        self, 
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset managers.

        Lists abjad stylesheet managers:

        ::

            >>> for x in wrangler._list_asset_managers(
            ...     user_library=False, 
            ...    user_score_packages=False):
            ...     x
            FileManager('.../abjad/stylesheets/clean-letter-14.ily')
            FileManager('.../abjad/stylesheets/clean-letter-16.ily')
            FileManager('.../abjad/stylesheets/rhythm-letter-16.ily')
            FileManager('.../scoremanager/scores/red_example_score/stylesheets/red-example-score-stylesheet.ily')

        Returns list.
        '''
        superclass = super(StylesheetWrangler, self)
        return superclass._list_asset_managers(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            head=head,
            )

    def _list_storehouse_paths(
        self,
        abjad_library=True, 
        user_library=True,
        abjad_score_packages=True, 
        user_score_packages=True,
        ):
        r'''Lists asset storehouse filesystem paths.

        Lists abjad storehouse filesystem paths:

        ::

            >>> for x in wrangler._list_storehouse_paths(
            ...     user_library=False, 
            ...     user_score_packages=False,
            ...     ):
            ...     x
            '.../abjad/stylesheets'
            '.../blue_example_score/stylesheets'
            '.../green_example_score/stylesheets'
            '.../red_example_score/stylesheets'

        Returns list.
        '''
        superclass = super(StylesheetWrangler, self)
        return superclass._list_storehouse_paths(
            abjad_library=abjad_library,
            user_library=user_library,
            abjad_score_packages=abjad_score_packages,
            user_score_packages=user_score_packages,
            )

    def _make_asset_menu_entries(self, head=None, include_extension=False):
        paths = self._list_asset_paths(head=head)
        display_strings = []
        for path in paths:
            display_string = os.path.basename(path)
            annotation = self._path_to_annotation(path)
            if annotation:
                display_string = '{} ({})'.format(display_string, annotation)
            display_strings.append(display_string)
        menu_entries = []
        if display_strings:
            sequences = (display_strings, [None], [None], paths)
            menu_entries = sequencetools.zip_sequences(sequences, cyclic=True)
        return menu_entries

    # TODO: remove head
    def _make_main_menu(self, head=None):
        menu = self._io_manager.make_menu(where=self._where)
        self._main_menu = menu
        asset_section = menu.make_asset_section()
        menu._asset_section = asset_section
        menu_entries = self._make_asset_menu_entries(
            head=head,
            include_extension=True,
            )
        asset_section.menu_entries = menu_entries
        if self._session.current_score_directory_path:
            section = menu.make_command_section()
            if self._get_header_stylesheet_file_path():
                section.append(('header stylesheet - edit', 'hse'))
            if self._get_layout_stylesheet_file_path():
                section.append(('layout stylesheet - edit', 'lse'))
            if self._get_paper_stylesheet_file_path():
                section.append(('paper stylesheet - edit', 'pse'))
        section = menu.make_command_section()
        section.append(('stylesheets - copy', 'cp'))
        section.append(('stylesheets - new', 'new'))
        section.append(('stylesheets - rename', 'ren'))
        section.append(('stylesheets - remove', 'rm'))
        return menu

    ### PUBLIC METHODS ###

    def edit_header_stylesheet(
        self,
        pending_user_input=None,
        ):
        r'''Edits header stylesheet.

        Returns none.
        '''
        file_path = self._get_header_stylesheet_file_path()
        self._edit_stylesheet(file_path)

    def edit_layout_stylesheet(
        self,
        pending_user_input=None,
        ):
        r'''Edits layout stylesheet.

        Returns none.
        '''
        file_path = self._get_layout_stylesheet_file_path()
        self._edit_stylesheet(file_path)

    def edit_paper_stylesheet(
        self,
        pending_user_input=None,
        ):
        r'''Edits paper stylesheet.

        Returns none.
        '''
        file_path = self._get_paper_stylesheet_file_path()
        self._edit_stylesheet(file_path)

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
            storehouse_path = self._select_storehouse_path(
                abjad_library=False,
                user_library=True,
                abjad_score_packages=False,
                user_score_packages=False,
                )
        if self._session._backtrack():
            return
        getter = self._io_manager.make_getter(where=self._where)
        getter.append_string('stylesheet name')
        stylesheet_file_path = getter._run()
        if self._session._backtrack():
            return
        stylesheet_file_path = \
            stringtools.string_to_accent_free_snake_case(
            stylesheet_file_path)
        if not stylesheet_file_path.endswith('.ily'):
            stylesheet_file_path = stylesheet_file_path + '.ily'
        stylesheet_file_path = os.path.join(
            storehouse_path,
            stylesheet_file_path,
            )
        manager = managers.FileManager(
            stylesheet_file_path, 
            session=self._session,
            )
        if self._session.is_test:
            manager._make_empty_asset()
        else:
            manager.edit()
