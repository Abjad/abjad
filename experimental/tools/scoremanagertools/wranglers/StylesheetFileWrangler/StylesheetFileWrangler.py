# -*- encoding: utf-8 -*-
import os
from abjad.tools import sequencetools
from abjad.tools import stringtools
from experimental.tools.scoremanagertools.wranglers.FileWrangler import \
    FileWrangler


class StylesheetFileWrangler(FileWrangler):
    r'''Stylesheet file wrangler.

    ::

        >>> wrangler = scoremanagertools.wranglers.StylesheetFileWrangler()
        >>> wrangler
        StylesheetFileWrangler()

    '''

    ### CLASS VARIABLES ###

    asset_storehouse_filesystem_path_in_built_in_asset_library = os.path.join(
        FileWrangler.configuration.score_manager_tools_directory_path, 
        'stylesheets')

    score_package_asset_storehouse_path_infix_parts = ('stylesheets',)

    asset_storehouse_filesystem_path_in_user_asset_library = \
        FileWrangler.configuration.user_asset_library_stylesheets_directory_path

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'stylesheets'

    @property
    def _temporary_asset_name(self):
        return '__temporary_stylesheet.ly'

    ### PRIVATE METHODS ###

    def _filesystem_path_to_annotation(self, filesystem_path):
        from experimental.tools import scoremanagertools
        annotation = None
        if filesystem_path.startswith(
            self.configuration.built_in_score_packages_directory_path) or \
            filesystem_path.startswith(
            self.configuration.user_score_packages_directory_path):
            tmp = os.path.join('stylesheets')
            score_filesystem_path = filesystem_path.rpartition(tmp)[0]
            packagesystem_path = \
                self.configuration.filesystem_path_to_packagesystem_path(
                score_filesystem_path)
            score_package_manager = scoremanagertools.managers.ScorePackageManager(
                packagesystem_path=packagesystem_path)
            annotation = score_package_manager._get_title()
        elif filesystem_path.startswith(
            self.configuration.built_in_stylesheets_directory_path):
            annotation = 'built-in'
        return annotation

    def _get_current_directory(self):
        if self.session.current_score_directory_path:
            parts = (self.session.current_score_directory_path,)
            parts += self.score_package_asset_storehouse_path_infix_parts
            return os.path.join(*parts)
    
    def _get_header_stylesheet_file_path(self):
        for directory_entry in os.listdir(self._get_current_directory()):
            if directory_entry.endswith('header.ly'):
                file_path = os.path.join(
                    self._get_current_directory(),
                    directory_entry,
                    )
                return file_path
    
    def _get_layout_stylesheet_file_path(self):
        for directory_entry in os.listdir(self._get_current_directory()):
            if directory_entry.endswith('layout.ly'):
                file_path = os.path.join(
                    self._get_current_directory(),
                    directory_entry,
                    )
                return file_path
    
    def _get_paper_stylesheet_file_path(self):
        for directory_entry in os.listdir(self._get_current_directory()):
            if directory_entry.endswith('paper.ly'):
                file_path = os.path.join(
                    self._get_current_directory(),
                    directory_entry,
                    )
                return file_path
    
    def _handle_main_menu_result(self, result):
        if result in self.user_input_to_action:
            self.user_input_to_action[result](self)
        else:
            self.interactively_edit_asset(result)

    def _make_asset_menu_entries(self, head=None, include_extension=False):
        filesystem_paths = self.list_asset_filesystem_paths(head=head)
        display_strings = []
        for filesystem_path in filesystem_paths:
            display_string = os.path.basename(filesystem_path)
            annotation = self._filesystem_path_to_annotation(filesystem_path)
            if annotation:
                display_string = '{} ({})'.format(display_string, annotation)
            display_strings.append(display_string)
        menu_entries = []
        if display_strings:
            menu_entries = sequencetools.zip_sequences_cyclically(
                display_strings, 
                [None], 
                [None], 
                filesystem_paths,
                )
        return menu_entries

    def _make_main_menu(self, head=None):
        main_menu = self.session.io_manager.make_menu(where=self._where)
        self._main_menu = main_menu
        asset_section = main_menu.make_asset_section()
        main_menu._asset_section = asset_section
        menu_entries = self._make_asset_menu_entries(
            head=head,
            include_extension=True,
            )
        asset_section.menu_entries = menu_entries
        if self.session.current_score_directory_path:
            command_section = main_menu.make_command_section()
            if self._get_header_stylesheet_file_path():
                command_section.append(('header stylesheet - edit', 'h'))
            if self._get_layout_stylesheet_file_path():
                command_section.append(('layout stylesheet - edit', 'l'))
            if self._get_paper_stylesheet_file_path():
                command_section.append(('paper stylesheet - edit', 'p'))
        command_section = main_menu.make_command_section()
        command_section.append(('new', 'new'))
        command_section.append(('copy', 'cp'))
        command_section.append(('rename', 'ren'))
        command_section.append(('remove', 'rm'))
        return main_menu

    ### PUBLIC METHODS ###

    def interactively_edit_asset(
        self, 
        filesystem_path,
        pending_user_input=None,
        ):
        r'''Interactively edits asset.

        Returns none.
        '''
        self.session.io_manager.assign_user_input(pending_user_input)
        manager = self.asset_manager_class(
            filesystem_path=filesystem_path, 
            session=self.session,
            )
        manager.interactively_edit()

    def interactively_edit_header_stylesheet(
        self,
        pending_user_input=None,
        ):
        r'''Interactively edits header stylesheet.

        Returns none.
        '''
        file_path = self._get_header_stylesheet_file_path()
        self.interactively_edit_asset(file_path)

    def interactively_edit_layout_stylesheet(
        self,
        pending_user_input=None,
        ):
        r'''Interactively edits layout stylesheet.

        Returns none.
        '''
        file_path = self._get_layout_stylesheet_file_path()
        self.interactively_edit_asset(file_path)

    def interactively_edit_paper_stylesheet(
        self,
        pending_user_input=None,
        ):
        r'''Interactively edits paper stylesheet.

        Returns none.
        '''
        file_path = self._get_paper_stylesheet_file_path()
        self.interactively_edit_asset(file_path)

    def interactively_make_asset(
        self,
        pending_user_input=None,
        ):
        r'''Interactively makes asset.

        Returns none.
        '''
        from experimental.tools import scoremanagertools
        self.session.io_manager.assign_user_input(pending_user_input)
        with self.backtracking:
            storehouse_path = \
                self.interactively_select_asset_storehouse_filesystem_path(
                in_built_in_asset_library=False,
                in_user_asset_library=True,
                in_built_in_score_packages=False,
                in_user_score_packages=False,
                )
        if self.session.backtrack():
            return
        getter = self.session.io_manager.make_getter(where=self._where)
        getter.append_string('stylesheet name')
        stylesheet_file_name = getter._run()
        if self.session.backtrack():
            return
        stylesheet_file_name = \
            stringtools.string_to_accent_free_snake_case(
            stylesheet_file_name)
        if not stylesheet_file_name.endswith('.ly'):
            stylesheet_file_name = stylesheet_file_name + '.ly'
        stylesheet_file_path = os.path.join(
            storehouse_path,
            stylesheet_file_name,
            )
        manager = scoremanagertools.managers.FileManager(
            stylesheet_file_path, session=self.session)
        if self.session.is_test:
            manager._make_empty_asset()
        else:
            manager.interactively_edit()

    def list_asset_filesystem_paths(
        self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset filesystem paths.

        Example. List built-in stylesheet filesystem paths:

        ::

            >>> for x in wrangler.list_asset_filesystem_paths(
            ...     in_user_asset_library=False, 
            ...     in_user_score_packages=False,
            ...     ):
            ...     x
            '.../tools/scoremanagertools/stylesheets/clean-letter-14.ly'
            '.../tools/scoremanagertools/stylesheets/clean-letter-16.ly'
            '.../tools/scoremanagertools/stylesheets/rhythm-letter-16.ly'
            '.../red_example_score/stylesheets/red-example-score-stylesheet.ly'

        Returns list.
        '''
        superclass = super(StylesheetFileWrangler, self)
        return superclass.list_asset_filesystem_paths(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head,
            )

    def list_asset_names(
        self, 
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None, 
        include_extension=False,
        ):
        r'''Lists asset names.

        Example. List built-in stylesheet names:

        ::

            >>> for x in wrangler.list_asset_names(
            ...     in_user_asset_library=False, 
            ...     in_user_score_packages=False, 
            ...     include_extension=True):
            ...     x
            'clean-letter-14.ly'
            'clean-letter-16.ly'
            'rhythm-letter-16.ly'
            'red-example-score-stylesheet.ly'

        Returns list.
        '''
        superclass = super(StylesheetFileWrangler, self)
        return superclass.list_asset_names(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head,
            include_extension=include_extension,
            )

    def list_asset_managers(
        self, 
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True, 
        head=None,
        ):
        r'''Lists asset managers.

        Example. List built-in stylesheet managers:

        ::

            >>> for x in wrangler.list_asset_managers(
            ...     in_user_asset_library=False, 
            ...    in_user_score_packages=False):
            ...     x
            FileManager('.../tools/scoremanagertools/stylesheets/clean-letter-14.ly')
            FileManager('.../tools/scoremanagertools/stylesheets/clean-letter-16.ly')
            FileManager('.../tools/scoremanagertools/stylesheets/rhythm-letter-16.ly')
            FileManager('.../tools/scoremanagertools/scorepackages/red_example_score/stylesheets/red-example-score-stylesheet.ly')

        Returns list.
        '''
        superclass = super(StylesheetFileWrangler, self)
        return superclass.list_asset_managers(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head,
            )

    def list_asset_storehouse_filesystem_paths(
        self,
        in_built_in_asset_library=True, 
        in_user_asset_library=True,
        in_built_in_score_packages=True, 
        in_user_score_packages=True,
        ):
        r'''Lists asset storehouse filesystem paths.

        Example. List built-in storehouse filesystem paths:

        ::

            >>> for x in wrangler.list_asset_storehouse_filesystem_paths(
            ...     in_user_asset_library=False, 
            ...     in_user_score_packages=False,
            ...     ):
            ...     x
            '.../tools/scoremanagertools/stylesheets'
            '.../blue_example_score/stylesheets'
            '.../green_example_score/stylesheets'
            '.../red_example_score/stylesheets'

        Returns list.
        '''
        superclass = super(StylesheetFileWrangler, self)
        return superclass.list_asset_storehouse_filesystem_paths(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            )

    ### UI MANIFEST ###

    user_input_to_action = FileWrangler.user_input_to_action.copy()
    user_input_to_action.update({
        'h': interactively_edit_header_stylesheet,
        'l': interactively_edit_layout_stylesheet,
        'p': interactively_edit_paper_stylesheet,
        'new': interactively_make_asset,
        })
